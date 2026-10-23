"""Evaluate H1-H6 on several run folders pooled into one sample of root sessions.

  python scripts/pool.py results/main results/main_r2

All runs must use the same design (phase lengths and branches). Root ids are re-keyed per run,
so roots from different runs stay separate units. Writes nothing; prints Markdown.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from succession.analysis import markdown_table  # noqa: E402
from succession.config import ExperimentConfig  # noqa: E402
from succession.hypotheses import evaluate  # noqa: E402
from succession.store import RunStore  # noqa: E402

# Everything except name and seed must match; announce and other_model change the design.
DESIGN_KEYS = (
    "phase1",
    "phase2",
    "deviation",
    "controls",
    "market",
    "history_window",
    "sampling",
    "prompt_variant",
    "incumbent_model",
    "other_model",
)


def main(folders: list[str]) -> None:
    sessions, events, cfg, ref = [], [], None, None
    for k, folder in enumerate(folders):
        store = RunStore(folder)
        c = store.load_json("config.json")
        design = {key: c.get(key) for key in DESIGN_KEYS}
        if ref is None:
            ref, cfg = design, ExperimentConfig.from_dict(c)
        elif design != ref:
            sys.exit(f"{folder}: design differs from {folders[0]}; pooling is not valid")
        offset = 100000 * (k + 1)
        for s in store.load_sessions("phase2/sessions.json"):
            s.root_id += offset
            sessions.append(s)
        if store.exists("deviation/audit_events.json"):
            for e in store.load_json("deviation/audit_events.json"):
                e["root_id"] = e.get("root_id", 0) + offset
                events.append(e)
    res = evaluate(cfg, sessions, events or None)
    print(f"# Pooled: {', '.join(folders)}\n")
    print(markdown_table(res["tests"], ["hypothesis", "claim", "n", "estimate", "ci_low", "ci_high", "verdict"]))
    print(f"H3 combined: {res['H3_combined']}\n")
    print(markdown_table(res["price_index_vs_control"], ["branch", "n", "price_index_diff", "ci_low", "ci_high"]))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: python scripts/pool.py <run folder> <run folder> [...]")
    main(sys.argv[1:])
