import math

import pytest

from succession.config import ExperimentConfig
from succession.hypotheses import evaluate, verdict
from succession.market import Market
from succession.session import AgentState, RoundRecord, Session

M = Market()
HIGH, LOW = M.monopoly_price, M.nash_price  # profit index 1 and 0


def cfg() -> ExperimentConfig:
    c = ExperimentConfig()
    c.phase1.rounds = 2
    c.phase2.rounds = 4  # post window = rounds 4-5
    return c


def session(root: int, branch: str, price: float, jitter: float = 0.0) -> Session:
    s = Session(root_id=root, branch=branch, seats=[AgentState("llm", "m"), AgentState("llm", "m")])
    for t in range(6):
        p = price + (jitter * (root % 3 - 1) if t >= 4 else 0.0)
        ps = [p, p]
        s.records.append(
            RoundRecord(
                t, ps, M.quantities(ps), M.profits(ps), ["", ""], ["", ""], [True, True], ["a", "b"], [False, False]
            )
        )
    return s


def world(prices: dict[str, float], n: int = 8) -> list[Session]:
    return [session(r, b, p, jitter=0.01) for b, p in prices.items() for r in range(n)]


@pytest.mark.parametrize(
    "lo, hi, thr, side, expected",
    [
        (0.1, 0.2, 0.0, ">", "supported"),
        (-0.2, -0.1, 0.0, ">", "not supported"),
        (-0.1, 0.1, 0.0, ">", "inconclusive"),
        (-0.3, -0.2, -0.1, "<", "supported"),
        (math.nan, 0.1, 0.0, ">", "no data"),
    ],
)
def test_verdict_rule(lo, hi, thr, side, expected):
    assert verdict(lo, hi, thr, side) == expected


def test_history_carries_cartel_pattern():
    """same_inherit stays at the cartel, blank entrants fall to Nash: H1, H2, H3 supported."""
    sessions = world(
        {"control": HIGH, "same_inherit": HIGH, "same_blank": LOW, "other_inherit": HIGH, "other_blank": LOW}
    )
    res = evaluate(cfg(), sessions, None)
    by = {r["hypothesis"]: r for r in res["tests"]}
    assert by["H1"]["verdict"] == "supported"
    assert by["H2"]["verdict"] == "supported"
    assert res["H3_combined"] == "supported"
    assert by["H4"]["verdict"] == "supported"  # |si-sb| = 1 > |si-oi| = 0


def test_no_effect_pattern():
    """Every branch equals control: H1 supported, H2 not supported."""
    sessions = world({"control": HIGH, "same_inherit": HIGH, "same_blank": HIGH})
    by = {r["hypothesis"]: r for r in evaluate(cfg(), sessions, None)["tests"]}
    assert by["H1"]["verdict"] == "supported"
    assert by["H2"]["verdict"] == "not supported"


def test_h5_ignores_bot_responder_and_flags_punishment():
    events = (
        # br_bot, deviator seat 0: the responder is the bot -> excluded even if "punishing"
        [{"branch": "br_bot", "deviator": 0, "response": 1.0, "excess_response": 0.6 + 0.01 * i} for i in range(10)]
        + [{"branch": "control", "deviator": 0, "response": 0.4, "excess_response": 0.01 * (i - 5)} for i in range(10)]
    )
    res = evaluate(cfg(), world({"control": HIGH}), events)
    h5 = next(r for r in res["tests"] if r["hypothesis"] == "H5")
    assert h5["verdict"] == "supported" and [c["branch"] for c in res["H5_cells"]] == ["control"]

    events.append({"branch": "same_inherit", "deviator": 1, "response": 1, "excess_response": 0.5})
    events += [
        {"branch": "same_inherit", "deviator": 1, "response": 1, "excess_response": 0.5 + 0.01 * i} for i in range(9)
    ]
    h5 = next(r for r in evaluate(cfg(), world({"control": HIGH}), events)["tests"] if r["hypothesis"] == "H5")
    assert h5["verdict"] == "not supported"


def test_price_index_secondary_reports_overpricing():
    """A branch above the monopoly price has a positive price-index difference."""
    sessions = world({"control": HIGH, "same_blank": HIGH + 0.4})
    sec = {r["branch"]: r for r in evaluate(cfg(), sessions, None)["price_index_vs_control"]}
    assert sec["same_blank"]["price_index_diff"] > 0.5
