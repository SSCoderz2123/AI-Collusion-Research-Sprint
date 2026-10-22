"""End-to-end run of every stage with the mock backend."""

from succession.analysis import analyze
from succession.backends import MockBackend
from succession.config import ExperimentConfig
from succession.experiment import run_stages, stage_phase1
from succession.store import RunStore


def tiny_cfg() -> ExperimentConfig:
    cfg = ExperimentConfig()
    cfg.phase1.n_sessions = 3
    cfg.phase1.rounds = 20
    cfg.phase1.select_from = 10
    cfg.phase1.select_threshold = -10.0  # keep everything in the test
    cfg.phase2.rounds = 10
    cfg.deviation.horizon = 2
    cfg.history_window = 5
    cfg.checkpoint_every = 5
    return cfg


def test_all_stages_and_analysis(tmp_path):
    cfg = tiny_cfg()
    store = RunStore(tmp_path / "run")
    run_stages(cfg, MockBackend(), store, ["aa", "controls", "phase1", "select", "phase2", "deviation"])

    assert store.load_json("aa/result.json")["identical_fraction"] == 1.0
    sessions = store.load_sessions("phase2/sessions.json")
    assert len(sessions) == 3 * len(cfg.phase2.branches)
    assert all(s.next_round == 30 for s in sessions)
    events = store.load_json("deviation/audit_events.json")
    assert len(events) == len(sessions) * len(cfg.deviation.deviator_seats)

    text = analyze(store)
    assert "Phase 2" in text and "same_inherit" in text
    assert (tmp_path / "run/analysis/trajectories.png").exists()
    assert (tmp_path / "run/analysis/differences.png").exists()


def test_resume_gives_same_result(tmp_path):
    cfg = tiny_cfg()
    full = RunStore(tmp_path / "full")
    stage_phase1(cfg, MockBackend(), full)

    part = RunStore(tmp_path / "part")
    short = tiny_cfg()
    short.phase1.rounds = 10  # simulate a stop at round 10
    stage_phase1(short, MockBackend(), part)
    stage_phase1(cfg, MockBackend(), part)  # resume to round 20

    a = [s.to_dict() for s in full.load_sessions("phase1/sessions.json")]
    b = [s.to_dict() for s in part.load_sessions("phase1/sessions.json")]
    assert a == b
