"""Exploratory 3D behavior-space figures for one or more run folders. No GPU, no model calls.

  python scripts/plot_behavior.py results/final_main results/final_olmo results/main_r2

For each run, writes into <run>/analysis/:
  price_paths_3d.png, price_path_pca_3d.png, behavior_price_paths.json, behavior_pca.json
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Windows consoles and `>` redirects default to cp1252, which cannot encode all characters
# in summaries (model replies, Unicode minus). Always write UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

from succession.behavior_plots import behavior_figures  # noqa: E402
from succession.store import RunStore  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python scripts/plot_behavior.py <run folder> [<run folder> ...]")
    for folder in sys.argv[1:]:
        if not (Path(folder) / "phase2" / "sessions.json").exists():
            print(f"{folder}: no phase2/sessions.json, skipped")
            continue
        for written in behavior_figures(RunStore(folder)):
            print(written)
