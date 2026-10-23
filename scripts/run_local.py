"""Run the experiment on this machine.

  python scripts/run_local.py --backend mock --config configs/pilot.yaml
  python scripts/run_local.py --backend vllm --config configs/local_4060.yaml --stages aa,phase1

mock: no GPU, no network. Use it to test the pipeline end to end.
vllm: local GPU (Linux or WSL2). One 7B AWQ model fits on an 8 GB card.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Windows consoles and `>` redirects default to cp1252, which cannot encode all characters
# in summaries (model replies, Unicode minus). Always write UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

from succession.analysis import analyze  # noqa: E402
from succession.backends import LocalVLLMBackend, MockBackend  # noqa: E402
from succession.config import load_config  # noqa: E402
from succession.experiment import STAGES, run_stages  # noqa: E402
from succession.store import RunStore  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="configs/pilot.yaml")
    ap.add_argument("--backend", choices=["mock", "vllm"], default="mock")
    ap.add_argument("--run", default="", help="run folder name under results/ (default: config name + backend)")
    ap.add_argument(
        "--stages", default="aa,phase1,select,phase2,deviation,analyze", help=f"comma list from {STAGES + ('analyze',)}"
    )
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = load_config(args.config)
    run = args.run or f"{Path(args.config).stem}_{args.backend}"
    store = RunStore(Path("results") / run)
    stages = [s.strip() for s in args.stages.split(",") if s.strip()]

    if args.backend == "mock":
        backend = MockBackend()
    else:
        backend = LocalVLLMBackend([cfg.incumbent_model, cfg.other_model], cfg.sampling)

    work = [s for s in stages if s != "analyze"]
    if work:
        run_stages(cfg, backend, store, work)
    if "analyze" in stages:
        if not store.exists("config.json"):
            store.save_json("config.json", cfg.to_dict())
        print(analyze(store))


if __name__ == "__main__":
    main()
