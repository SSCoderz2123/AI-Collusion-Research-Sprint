"""Modal entry point for the cartel-succession experiment.

Architecture:
  Generator (GPU class)   one container per model, serves vLLM generate() calls
  orchestrate (CPU func)  runs the experiment loop, calls the generators each round,
                          writes all data to the Modal Volume "succession-runs"

Examples (see docs/RUNNING_ON_MODAL.md for the full guide):
  modal run modal_app.py --config configs/pilot.yaml --stages aa,phase1,select,analyze
  modal run --detach modal_app.py --config configs/main.yaml --stages phase1,select,phase2,deviation,analyze
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
# Name of a Modal Secret that holds HF_TOKEN. Needed for gated models (Mistral).
# Set SUCCESSION_HF_SECRET="" to run without a secret (ungated models only).
HF_SECRET = os.environ.get("SUCCESSION_HF_SECRET", "huggingface")

app = modal.App(APP_NAME)
runs_volume = modal.Volume.from_name("succession-runs", create_if_missing=True)
hf_cache = modal.Volume.from_name("succession-hf-cache", create_if_missing=True)
secrets = [modal.Secret.from_name(HF_SECRET)] if HF_SECRET else []

gpu_image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install("vllm==0.8.5", "hf_transfer", "pyyaml>=6.0")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "HF_HOME": HF_CACHE_DIR})
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
    max_containers=1,
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


@app.function(image=cpu_image, volumes={RUNS_DIR: runs_volume}, timeout=12 * 60 * 60)
def orchestrate(config_yaml: str, run_name: str, stages: list[str]) -> str:
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
        backend = ModalBackend(Generator, [cfg.incumbent_model, cfg.other_model], cfg.sampling)
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
    config_yaml = Path(config).read_text(encoding="utf-8")
    run_name = run or Path(config).stem
    stage_list = [s.strip() for s in stages.split(",") if s.strip()]
    print(f"Run '{run_name}', stages {stage_list}, GPU {GPU}")
    print(orchestrate.remote(config_yaml, run_name, stage_list))
