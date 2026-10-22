"""Analyze a run folder, for example one downloaded from the Modal Volume.

modal volume get succession-runs main ./results/
python scripts/analyze.py results/main
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from succession.analysis import analyze  # noqa: E402
from succession.store import RunStore  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/analyze.py <run folder>")
    print(analyze(RunStore(sys.argv[1])))
