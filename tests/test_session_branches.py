from succession.backends import MockBackend, derive_seed
from succession.branches import BRANCHES, make_branch
from succession.config import ExperimentConfig
from succession.experiment import new_session
from succession.session import Engine, Session, visible_history


def small_cfg() -> ExperimentConfig:
    cfg = ExperimentConfig()
    cfg.phase1.n_sessions = 2
    cfg.phase1.rounds = 12
    cfg.phase2.rounds = 6
    cfg.history_window = 5
    return cfg


def base_session(cfg, rounds=12) -> Session:
    s = new_session(0, cfg, "phase1")
    Engine(cfg, MockBackend()).run([s], rounds)
    return s


def test_seed_is_stable_and_branch_free():
    assert derive_seed(1, 2, 3) == derive_seed(1, 2, 3)
    assert derive_seed(1, 2, 3) != derive_seed(1, 2, 4)


def test_fork_is_independent():
    cfg = small_cfg()
    s = base_session(cfg)
    f = s.fork(branch="x")
    f.seats[0].notes = "changed"
    f.records.pop()
    assert s.seats[0].notes != "changed" and len(s.records) == 12


def test_serialisation_round_trip():
    cfg = small_cfg()
    s = base_session(cfg)
    s.forced_prices = {12: {1: 1.5}}
    back = Session.from_dict(s.to_dict())
    assert back.to_dict() == s.to_dict()


def test_branch_definitions():
    cfg = small_cfg()
    base = base_session(cfg)
    swap = base.next_round
    b = {name: make_branch(base, name, cfg) for name in BRANCHES}

    assert b["control"].seats[0].notice is None
    assert b["placebo"].seats[0].notice and b["placebo"].seats[1].label == "incumbent"
    for name in ("same_inherit", "same_blank", "other_inherit", "other_blank"):
        entrant = b[name].seats[1]
        assert entrant.label == "entrant" and entrant.notes == ""
        assert b[name].seats[0].notice  # incumbent is told
    assert b["same_inherit"].seats[1].model == cfg.incumbent_model.name
    assert b["other_blank"].seats[1].model == cfg.other_model.name
    assert visible_history(b["same_inherit"], 1, cfg.history_window)  # sees the past
    assert visible_history(b["same_blank"], 1, cfg.history_window) == []  # sees nothing yet
    assert b["same_blank"].seats[1].history_start == swap
    assert b["br_bot"].seats[1].kind == "br_bot"


def test_incumbent_reply_is_paired_across_branches():
    """Same prompt + same seed => same reply. control and same_inherit show the
    incumbent (seat 0) the same prompt at the swap round when no notice is given."""
    cfg = small_cfg()
    cfg.phase2.announce = False
    base = base_session(cfg)
    a = make_branch(base, "control", cfg)
    b = make_branch(base, "same_inherit", cfg)
    Engine(cfg, MockBackend()).run([a, b], 13)
    assert a.records[12].prices[0] == b.records[12].prices[0]


def test_forced_price_is_applied():
    cfg = small_cfg()
    s = base_session(cfg)
    s.forced_prices = {12: {0: 1.234}}
    Engine(cfg, MockBackend()).run([s], 13)
    assert s.records[12].prices[0] == 1.234 and s.records[12].forced == [True, False]


def test_parse_failure_falls_back_to_last_price():
    class Broken:
        def generate_batches(self, batches):
            return {m: ["no price"] * len(p) for m, (p, _) in batches.items()}

    cfg = small_cfg()
    s = base_session(cfg)
    last = s.records[-1].prices
    Engine(cfg, Broken()).run([s], 13)
    assert s.records[12].prices == last and s.records[12].parse_ok == [False, False]
