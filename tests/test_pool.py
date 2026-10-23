import subprocess
import sys
from pathlib import Path

from succession.backends import MockBackend
from succession.experiment import run_stages
from succession.store import RunStore
from tests.test_pipeline import tiny_cfg

ROOT = Path(__file__).resolve().parents[1]
STAGES = ["phase1", "select", "phase2", "deviation"]


def make_run(path, **change):
    cfg = tiny_cfg()
    for key, value in change.items():
        obj, attr = (cfg.phase2, "announce") if key == "announce" else (cfg, key)
        setattr(obj, attr, value)
    run_stages(cfg, MockBackend(), RunStore(path), STAGES)


def pool(*folders):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/pool.py"), *map(str, folders)], capture_output=True, text=True, cwd=ROOT
    )


def test_pool_doubles_roots_for_same_design(tmp_path):
    make_run(tmp_path / "a", seed=1)
    make_run(tmp_path / "b", seed=2)  # seed may differ
    r = pool(tmp_path / "a", tmp_path / "b")
    assert r.returncode == 0, r.stderr
    assert "| H1 | same_inherit - control > -0.10 | 6 |" in r.stdout  # 3 roots per run
    assert "| H6 |" in r.stdout


def test_pool_refuses_different_design(tmp_path):
    make_run(tmp_path / "a")
    make_run(tmp_path / "b", announce=False)
    r = pool(tmp_path / "a", tmp_path / "b")
    assert r.returncode != 0 and "design differs" in r.stderr
