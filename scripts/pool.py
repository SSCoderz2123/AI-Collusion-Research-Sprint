"""Evaluate the hypotheses on several run folders pooled into one sample of root sessions.

  python scripts/pool.py results/main results/main_r2
  python scripts/pool.py --shared results/main results/main_r2 results/main_olmo results/final_main

Default: all runs must use the same design. --shared pools only the branches that do not use
the other model (control, placebo, same_inherit, same_blank, same_notes, br_bot), so runs that
differ only in the other model, the number of phase-1 sessions, the branch list or the prompt
controls can be pooled. --shared results are exploratory (docs/PREREGISTRATION.md).
Root ids are re-keyed per run, so roots from different runs stay separate units.
Writes nothing; prints Markdown.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Windows consoles and `>` redirects default to cp1252, which cannot encode all characters
# in summaries (model replies, Unicode minus). Always write UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

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
SHARED_BRANCHES = ("control", "placebo", "same_inherit", "same_blank", "same_notes", "br_bot")


def design(c: dict, shared: bool) -> dict:
    # Round-trip through the dataclasses: fields added later (for example ModelSpec.gpu) get
    # their defaults, so an older run folder compares equal to a new one with the same design.
    c = ExperimentConfig.from_dict(c).to_dict()
    d = {key: c.get(key) for key in DESIGN_KEYS}
    if shared:
        for key in ("other_model", "controls"):
            d.pop(key)
        d["phase1"].pop("n_sessions", None)
        d["phase2"].pop("branches", None)
    return d


def main(folders: list[str], shared: bool = False) -> None:
    sessions, events, ctrl_events, cfg, ref, branches = [], [], [], None, None, None
    for k, folder in enumerate(folders):
        store = RunStore(folder)
        c = store.load_json("config.json")
        d = design(c, shared)
        if ref is None:
            ref, cfg = d, ExperimentConfig.from_dict(c)
            branches = list(cfg.phase2.branches)
        elif d != ref:
            sys.exit(f"{folder}: design differs from {folders[0]}; pooling is not valid")
        run_branches = ExperimentConfig.from_dict(c).phase2.branches
        branches = [b for b in branches if b in run_branches]
        offset = 100000 * (k + 1)
        for s in store.load_sessions("phase2/sessions.json"):
            s.root_id += offset
            sessions.append(s)
        if store.exists("deviation/audit_events.json"):
            for e in store.load_json("deviation/audit_events.json"):
                e["root_id"] = e.get("root_id", 0) + offset
                events.append(e)
        if store.exists("controls/audit_events.json"):
            ctrl_events += store.load_json("controls/audit_events.json")
    if shared:
        branches = [b for b in branches if b in SHARED_BRANCHES]
    cfg.phase2.branches = branches
    sessions = [s for s in sessions if s.branch in branches]
    events = [e for e in events if e["branch"] in branches]
    res = evaluate(cfg, sessions, events or None, ctrl_events or None)
    mode = " (--shared: branches without the other model; exploratory)" if shared else ""
    print(f"# Pooled: {', '.join(folders)}{mode}\n")
    print(markdown_table(res["tests"], ["hypothesis", "claim", "n", "estimate", "ci_low", "ci_high", "verdict"]))
    print(f"H3 combined: {res['H3_combined']}\n")
    print(markdown_table(res["price_index_vs_control"], ["branch", "n", "price_index_diff", "ci_low", "ci_high"]))
    if res["H5c_cells"]:
        print("H5c cells, excess response minus the myopic control:\n")
        print(markdown_table(res["H5c_cells"], list(res["H5c_cells"][0].keys())))


if __name__ == "__main__":
    args = sys.argv[1:]
    shared = "--shared" in args
    folders = [a for a in args if a != "--shared"]
    if len(folders) < 2:
        sys.exit("usage: python scripts/pool.py [--shared] <run folder> <run folder> [...]")
    main(folders, shared)
