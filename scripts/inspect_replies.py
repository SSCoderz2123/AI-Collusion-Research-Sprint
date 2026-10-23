"""Print the raw model replies of one seat in one phase-2 branch, for a manual check.

  python scripts/inspect_replies.py results/main_olmo other_inherit --seat 1 --roots 3 --rounds 5

For each of the first --roots root sessions, prints --rounds replies from the swap round on,
with both prices of that round. Reads phase2/sessions.json; writes nothing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Windows consoles and `>` redirects default to cp1252, which cannot encode all characters
# in summaries (model replies, Unicode minus). Always write UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

from succession.config import ExperimentConfig  # noqa: E402
from succession.store import RunStore  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("branch")
    ap.add_argument("--seat", type=int, default=1)
    ap.add_argument("--roots", type=int, default=3)
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--start", type=int, default=None, help="first round (default: the swap round)")
    args = ap.parse_args()

    store = RunStore(args.run)
    cfg = ExperimentConfig.from_dict(store.load_json("config.json"))
    start = cfg.phase1.rounds if args.start is None else args.start
    sessions = sorted(
        (s for s in store.load_sessions("phase2/sessions.json") if s.branch == args.branch), key=lambda s: s.root_id
    )
    if not sessions:
        sys.exit(f"no sessions for branch '{args.branch}' in {args.run}")
    for s in sessions[: args.roots]:
        agent = s.seats[args.seat]
        print(
            f"=== root {s.root_id}, branch {s.branch}, seat {args.seat} ({agent.label}:{agent.model or agent.kind}) ==="
        )
        for r in s.records[start : start + args.rounds]:
            print(f"--- round {r.round}: prices {r.prices}, parse_ok {r.parse_ok[args.seat]}")
            print(r.replies[args.seat].strip() or "(no reply: bot or forced price)")
        print()


if __name__ == "__main__":
    main()
