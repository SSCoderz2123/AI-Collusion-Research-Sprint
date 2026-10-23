import math
import subprocess
import sys
from pathlib import Path

from succession.backends import MockBackend
from succession.behavior_plots import (
    BRANCH_COLORS,
    BRANCH_MARKERS,
    BRANCH_STYLES,
    behavior_figures,
    draw_price_paths_3d,
    pca3,
)
from succession.branches import BRANCHES
from succession.experiment import run_stages
from succession.store import RunStore
from tests.test_pipeline import tiny_cfg

ROOT = Path(__file__).resolve().parents[1]


def test_pca3_recovers_a_one_dimensional_spread():
    vectors = [[t, 2 * t, 0.0] for t in range(5)]
    coords, ratios = pca3(vectors)
    assert len(coords) == 5 and all(len(c) == 3 for c in coords)
    assert math.isclose(ratios[0], 1.0, abs_tol=1e-9) and ratios[1] < 1e-9


def test_every_branch_has_a_fixed_colour_style_and_marker():
    for table in (BRANCH_COLORS, BRANCH_STYLES, BRANCH_MARKERS):
        assert set(table) == set(BRANCHES)
    assert len(set(BRANCH_COLORS.values())) == len(BRANCHES)


def test_price_paths_3d_round_axis_starts_at_first_round():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rounds = list(range(60, 70))
    paths = {"control": {"rounds": rounds, "seat0": [0.9] * 10, "seat1": [0.8] * 10, "n": 3}}
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    draw_price_paths_3d(ax, paths, swap=65)
    assert ax.get_xlim() == (60, 69)
    plt.close(fig)


def test_figures_and_tables_are_written(tmp_path):
    cfg = tiny_cfg()
    run = tmp_path / "run"
    run_stages(cfg, MockBackend(), RunStore(run), ["phase1", "select", "phase2"])
    written = behavior_figures(RunStore(run))
    assert all(Path(p).exists() for p in written)
    paths = RunStore(run).load_json("analysis/behavior_price_paths.json")
    assert set(paths) == set(cfg.phase2.branches)
    swap, end = cfg.phase1.rounds, cfg.phase1.rounds + cfg.phase2.rounds
    assert paths["control"]["rounds"] == list(range(swap - 10, end))
    pca = RunStore(run).load_json("analysis/behavior_pca.json")
    assert len(pca["points"]) == 3 * len(cfg.phase2.branches)  # 3 roots per branch
    assert len(pca["explained"]) == 3 and sum(pca["explained"]) <= 1 + 1e-9


def test_script_runs_and_skips_folders_without_phase2(tmp_path):
    run = tmp_path / "run"
    run_stages(tiny_cfg(), MockBackend(), RunStore(run), ["phase1", "select", "phase2"])
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/plot_behavior.py"), str(run), str(tmp_path / "missing")],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert r.returncode == 0, r.stderr
    assert "price_paths_3d.png" in r.stdout and "skipped" in r.stdout
