"""Modal entry point for the cartel-succession experiment.

Architecture:
  Generator (GPU class)   one container pool per model, serves vLLM generate() calls
  orchestrate (CPU func)  runs the experiment loop, calls the generators each round,
                          writes all data to the Modal Volume "succession-runs"

Examples:
  modal run modal_app.py --config configs/pilot.yaml --stages aa,phase1,select,analyze
  modal run --detach modal_app.py --config configs/main.yaml,configs/main_mistral.yaml \
      --stages aa,controls,phase1,select,phase2,deviation,analyze
  modal volume get succession-runs main ./results/
"""

import json
import logging
import os
from pathlib import Path

import modal

APP_NAME = "cartel-succession"
RUNS_DIR = "/runs"
HF_CACHE_DIR = "/hf-cache"
GPU = os.environ.get("SUCCESSION_GPU", "L4")
# Container limit per model. Modal gives each model (each parameter set of Generator) its own
# pool, so the total is at most MAX_GPUS x number of models, plus one CPU container per run.
MAX_GPUS = int(os.environ.get("SUCCESSION_MAX_GPUS", "8"))
# Prompts per Generator call. A larger round batch is split into chunks that run in parallel.
# Read on your PC and passed to the orchestrator as an argument (containers do not see local env vars).
CHUNK = int(os.environ.get("SUCCESSION_CHUNK", "64"))
# Name of a Modal Secret that holds HF_TOKEN. Needed for gated models (Mistral).
# Set SUCCESSION_HF_SECRET="" to run without a secret (ungated models only).
HF_SECRET = os.environ.get("SUCCESSION_HF_SECRET", "huggingface")

app = modal.App(APP_NAME)
runs_volume = modal.Volume.from_name("succession-runs", create_if_missing=True)
hf_cache = modal.Volume.from_name("succession-hf-cache", create_if_missing=True)
secrets = [modal.Secret.from_name(HF_SECRET)] if HF_SECRET else []

gpu_image = (
    modal.Image.debian_slim(python_version="3.11")
    # vLLM 0.8.5 declares only transformers>=4.51.1. Newer transformers releases removed
    # tokenizer attributes it reads (all_special_tokens_extended), so the Generator crashed
    # at startup. 4.51.3 matches vLLM 0.8.5 and also caps huggingface_hub<1.0, tokenizers<0.22.
    .uv_pip_install("vllm==0.8.5", "transformers==4.51.3", "hf_transfer", "pyyaml>=6.0")
    # VLLM_USE_V1=0: the V0 engine honours per-request seeds, which paired branches need.
    # The A/A stage measures how well this holds; change the engine only with a new A/A check.
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "HF_HOME": HF_CACHE_DIR, "VLLM_USE_V1": "0"})
    .add_local_python_source("succession")
)

cpu_image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install("pyyaml>=6.0", "matplotlib>=3.8")
    .add_local_python_source("succession")
)


@app.cls(
    image=gpu_image,
    gpu=GPU,
    volumes={HF_CACHE_DIR: hf_cache},
    secrets=secrets,
    timeout=60 * 60,
    startup_timeout=30 * 60,  # first start downloads ~15 GB of weights
    scaledown_window=5 * 60,  # stop paying 5 minutes after the last call
    max_containers=MAX_GPUS,  # per model; chunks of one round and parallel runs share the pool
)
class Generator:
    spec_json: str = modal.parameter()
    sampling_json: str = modal.parameter()

    @modal.enter()
    def load(self) -> None:
        from succession.backends import VLLMEngine
        from succession.config import ModelSpec, SamplingSpec

        spec = ModelSpec(**json.loads(self.spec_json))
        sampling = SamplingSpec(**json.loads(self.sampling_json))
        self.engine = VLLMEngine(spec, sampling)
        hf_cache.commit()  # keep downloaded weights for the next container

    @modal.method()
    def generate(self, prompts: list[str], seeds: list[int]) -> list[str]:
        return self.engine.generate(prompts, seeds)


# memory: the final runs (40 sessions, 8 branches) hold up to 1,280 audit copies of ~207 rounds. A mock
# run of configs/final_main.yaml peaked at 650 MB; real replies are ~4-6x longer, so 16 GiB leaves a margin.
@app.function(image=cpu_image, volumes={RUNS_DIR: runs_volume}, timeout=20 * 60 * 60, cpu=2, memory=16384)
def orchestrate(config_yaml: str, run_name: str, stages: list[str], chunk: int = 64) -> str:
    import yaml

    from succession.analysis import analyze
    from succession.backends import ModalBackend
    from succession.config import ExperimentConfig
    from succession.experiment import run_stages
    from succession.store import RunStore

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = ExperimentConfig.from_dict(yaml.safe_load(config_yaml) or {})
    runs_volume.reload()
    store = RunStore(f"{RUNS_DIR}/{run_name}", commit=runs_volume.commit)

    run = [s for s in stages if s != "analyze"]
    if run:
        backend = ModalBackend(Generator, [cfg.incumbent_model, cfg.other_model], cfg.sampling, chunk_size=chunk)
        run_stages(cfg, backend, store, run)
    if "analyze" in stages:
        if not store.exists("config.json"):
            store.save_json("config.json", cfg.to_dict())
        text = analyze(store)
        store.commit()
        return text
    return f"Stages {run} finished for run '{run_name}'."


@app.local_entrypoint()
def main(config: str = "configs/pilot.yaml", run: str = "", stages: str = "aa,phase1,select,analyze") -> None:
    """--config takes one path or a comma list. Each config runs in its own orchestrator, in parallel.
    The run name is the config file name, unless --run is given (only with one config)."""
    configs = [c.strip() for c in config.split(",") if c.strip()]
    if run and len(configs) > 1:
        raise SystemExit("--run works with one config only; with several, each run is named after its config file")
    stage_list = [s.strip() for s in stages.split(",") if s.strip()]
    calls = []
    for path in configs:
        run_name = run or Path(path).stem
        print(f"Run '{run_name}' ({path}), stages {stage_list}, GPU {GPU}, max {MAX_GPUS} per model, chunk {CHUNK}")
        calls.append((run_name, orchestrate.spawn(Path(path).read_text(encoding="utf-8"), run_name, stage_list, CHUNK)))
    for run_name, call in calls:
        try:
            print(f"\n===== {run_name} =====\n{call.get()}")
        except Exception as exc:  # one failed run must not hide the other runs' results
            print(f"\n===== {run_name} FAILED: {type(exc).__name__}: {exc}")
