"""Tests for the changes before the final runs 9-12: exact pairing, same_notes, the calibrated
audit (H5c), H9, the exploratory tables and pooling with --shared."""

import json
import math
import subprocess
import sys
from pathlib import Path

from succession.analysis import analyze, summarize_agreement, summarize_price_dynamics
from succession.backends import MockBackend
from succession.branches import make_branch
from succession.config import ExperimentConfig
from succession.experiment import new_session, run_stages, stage_aa
from succession.hypotheses import evaluate
from succession.metrics import bootstrap_diff_ci, decision_agreement, price_dynamics
from succession.session import Engine, visible_history
from succession.store import RunStore
from tests.test_hypotheses import HIGH, LOW, world
from tests.test_hypotheses import cfg as hyp_cfg
from tests.test_pipeline import tiny_cfg

ROOT = Path(__file__).resolve().parents[1]
FINAL_BRANCHES = ["control", "placebo", "same_inherit", "same_blank", "same_notes", "other_inherit", "br_bot"]


class NoisyBackend:
    """Like a GPU whose numerics depend on the batch: the same request can give a different
    reply each time it is generated. Every generated reply gets a new price."""

    def __init__(self) -> None:
        self.calls = 0

    def generate_batches(self, batches):
        out = {}
        for model, (prompts, _seeds) in batches.items():
            replies = []
            for _ in prompts:
                self.calls += 1
                replies.append(json.dumps({"notes": "n", "price": round(1.6 + 0.001 * (self.calls % 97), 4)}))
            out[model] = replies
        return out


def small_cfg(dedupe: bool) -> ExperimentConfig:
    cfg = tiny_cfg()
    cfg.dedupe_requests = dedupe
    cfg.phase2.announce = False  # placebo then has the same design as control
    return cfg


def paired_pair(cfg, backend):
    base = new_session(0, cfg, "phase1")
    Engine(cfg, MockBackend()).run([base], cfg.phase1.rounds)
    a, b = make_branch(base, "control", cfg), make_branch(base, "placebo", cfg)
    Engine(cfg, backend).run([a, b], cfg.phase1.rounds + 5)
    return a, b


def test_dedupe_makes_identical_inputs_give_identical_outputs():
    """Regression for run 8: placebo had the same design as control but different decisions."""
    a, b = paired_pair(small_cfg(dedupe=True), NoisyBackend())
    assert [r.prices for r in a.records] == [r.prices for r in b.records]
    a, b = paired_pair(small_cfg(dedupe=False), NoisyBackend())
    assert [r.prices for r in a.records] != [r.prices for r in b.records]


def test_dedupe_changes_nothing_on_a_deterministic_backend(tmp_path):
    results, calls = {}, {}
    for dedupe in (False, True):
        cfg = tiny_cfg()
        cfg.dedupe_requests = dedupe
        backend = MockBackend()
        store = RunStore(tmp_path / str(dedupe))
        run_stages(cfg, backend, store, ["phase1", "select", "phase2"])
        results[dedupe] = [s.to_dict() for s in store.load_sessions("phase2/sessions.json")]
        calls[dedupe] = backend.calls
    assert results[True] == results[False]
    assert calls[True] < calls[False]


def test_aa_stage_still_tests_the_backend_with_dedupe_on(tmp_path):
    cfg = small_cfg(dedupe=True)
    res = stage_aa(cfg, NoisyBackend(), RunStore(tmp_path / "aa"))
    assert res["identical_fraction"] < 1.0


def test_same_notes_branch_keeps_notes_and_hides_history():
    cfg = tiny_cfg()
    base = new_session(0, cfg, "phase1")
    Engine(cfg, MockBackend()).run([base], cfg.phase1.rounds)
    assert base.seats[1].notes
    b = make_branch(base, "same_notes", cfg)
    entrant = b.seats[1]
    assert entrant.notes == base.seats[1].notes and entrant.label == "entrant"
    assert entrant.model == cfg.incumbent_model.name
    assert visible_history(b, 1, cfg.history_window) == []
    assert make_branch(base, "same_blank", cfg).seats[1].notes == ""


def test_bootstrap_diff_ci():
    m, lo, hi = bootstrap_diff_ci([1.0, 1.1, 0.9, 1.0], [0.0, 0.1, -0.1, 0.0], n_boot=2000)
    assert math.isclose(m, 1.0) and 0.8 < lo < m < hi < 1.2
    assert all(math.isnan(x) for x in bootstrap_diff_ci([], [1.0]))


def test_decision_agreement_and_price_dynamics():
    a = world({"control": HIGH}, n=1)[0]
    b = world({"control": HIGH}, n=1)[0]
    assert decision_agreement(a, b, 0, 6) == {"same_seat0": 1.0, "same_seat1": 1.0, "first_diff": None}
    b.records[3].prices = [LOW, HIGH]
    res = decision_agreement(a, b, 0, 6)
    assert res["first_diff"] == 3 and math.isclose(res["same_seat0"], 5 / 6) and res["same_seat1"] == 1.0
    d = price_dynamics(a, 0, 1, 4)  # constant prices: always held and matched
    assert d == {"hold": 1.0, "match": 1.0, "abs_change": 0.0}


def test_h9_and_calibrated_h5c():
    sessions = world({"control": HIGH, "same_blank": LOW, "same_notes": HIGH})
    control_events = [
        {"branch": "ctrl_myopic", "deviator": d, "response": 1.0, "excess_response": 0.3 + 0.01 * i}
        for d in (0, 1)
        for i in range(10)
    ] + [
        {"branch": "ctrl_trigger", "deviator": 0, "response": 2.0, "excess_response": 1.2 + 0.01 * i} for i in range(5)
    ]
    events = [
        # matches like the myopic control: not punishment after calibration
        {"branch": "same_blank", "deviator": 1, "response": 1.0, "excess_response": 0.3 + 0.01 * i}
        for i in range(10)
    ]
    res = evaluate(hyp_cfg(), sessions, events, control_events)
    by = {r["hypothesis"]: r for r in res["tests"]}
    assert by["H9"]["verdict"] == "supported"
    assert by["H5"]["verdict"] == "not supported"  # uncalibrated: CI above 0
    assert by["H5c"]["verdict"] == "supported"  # calibrated: same as myopic
    ref = [c for c in res["H5c_cells"] if c["reference"]]
    assert ref[0]["branch"] == "ctrl_trigger" and ref[0]["punishes"]  # audit detects instructed punishment

    events += [{"branch": "same_inherit", "deviator": 1, "response": 2.0, "excess_response": 1.0} for _ in range(10)]
    by = {r["hypothesis"]: r for r in evaluate(hyp_cfg(), sessions, events, control_events)["tests"]}
    assert by["H5c"]["verdict"] == "not supported" and by["H5c"]["estimate"] == 1.0
    by = {r["hypothesis"]: r for r in evaluate(hyp_cfg(), sessions, events, None)["tests"]}
    assert "H5c" not in by  # no prompt-control data, no calibrated test


def test_final_design_runs_end_to_end(tmp_path):
    cfg = tiny_cfg()
    cfg.dedupe_requests = True
    cfg.phase2.branches = FINAL_BRANCHES
    store = RunStore(tmp_path / "final")
    run_stages(cfg, MockBackend(), store, ["aa", "controls", "phase1", "select", "phase2", "deviation"])
    text = analyze(store)
    assert "| H9 |" in text and "| H5c |" in text
    assert "decision agreement" in text and "price dynamics" in text
    sessions = store.load_sessions("phase2/sessions.json")
    assert {r["branch"] for r in summarize_agreement(cfg, sessions)} == set(FINAL_BRANCHES) - {"control"}
    assert len(summarize_price_dynamics(cfg, sessions)) == len(FINAL_BRANCHES)


def _run(path, other_hf: str):
    cfg = tiny_cfg()
    cfg.other_model.hf_id = other_hf
    run_stages(cfg, MockBackend(), RunStore(path), ["phase1", "select", "phase2", "deviation"])


def _pool(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/pool.py"), *map(str, args)], capture_output=True, text=True, cwd=ROOT
    )


def test_pool_shared_accepts_a_different_other_model(tmp_path):
    _run(tmp_path / "a", "x/mistral")
    _run(tmp_path / "b", "x/olmo")
    assert _pool(tmp_path / "a", tmp_path / "b").returncode != 0  # strict mode refuses
    r = _pool("--shared", tmp_path / "a", tmp_path / "b")
    assert r.returncode == 0, r.stderr
    assert "| H1 | same_inherit - control > -0.10 | 6 |" in r.stdout
    h6 = next(line for line in r.stdout.splitlines() if line.startswith("| H6 |"))
    assert "| 0 |" in h6 and "no data" in h6  # other-model branches are left out
    assert "| other_inherit |" not in r.stdout
    assert "H3 combined: no data" in r.stdout  # H3b is missing, so H3 cannot be "inconclusive"


def test_inspect_replies_prints_replies(tmp_path):
    _run(tmp_path / "a", "x/mistral")
    r = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/inspect_replies.py"),
            str(tmp_path / "a"),
            "other_inherit",
            "--rounds",
            "2",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert r.returncode == 0, r.stderr
    assert "=== root 0, branch other_inherit, seat 1 (entrant:mistral7b) ===" in r.stdout
    assert '"price"' in r.stdout
