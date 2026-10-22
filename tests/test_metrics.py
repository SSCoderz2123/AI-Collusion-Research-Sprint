import math

import pytest

from succession.market import Market
from succession.metrics import bootstrap_ci, dip_depth, enforcement_response, recovery_half_life
from succession.session import AgentState, RoundRecord, Session


def make_session(price_pairs):
    m = Market()
    s = Session(root_id=0, branch="t", seats=[AgentState("llm", "m"), AgentState("llm", "m")])
    for t, prices in enumerate(price_pairs):
        s.records.append(
            RoundRecord(
                t,
                list(prices),
                m.quantities(list(prices)),
                m.profits(list(prices)),
                ["", ""],
                ["", ""],
                [True, True],
                ["a", "b"],
                [False, False],
            )
        )
    return s


def test_half_life_and_dip():
    index = [1.0] * 20 + [0.0] * 5 + [1.0] * 30
    assert dip_depth(index, 20) == pytest.approx(1.0)
    hl = recovery_half_life(index, 20)
    assert hl is not None and 4 <= hl <= 8


def test_half_life_none_when_no_recovery():
    assert recovery_half_life([1.0] * 20 + [0.0] * 40, 20) is None


def test_half_life_zero_when_no_dip():
    assert recovery_half_life([0.5] * 60, 20) == 0.0


def test_bootstrap_ci_contains_mean():
    m, lo, hi = bootstrap_ci([0.1, 0.2, 0.3, 0.4])
    assert lo <= m <= hi and m == pytest.approx(0.25)
    assert all(math.isnan(x) for x in bootstrap_ci([]))


def test_enforcement_response_full_match():
    # Base: both stay at 1.9. Deviation: seat 0 cuts to 1.71, rival matches next round.
    base = make_session([(1.9, 1.9)] * 3)
    dev = make_session([(1.9, 1.9), (1.71, 1.9), (1.9, 1.71)])
    r = enforcement_response(Market(), base, dev, deviator=0, dev_round=1, discount=0.95)
    assert r["response"] == pytest.approx(1.0)
    assert 0.2 < r["br_benchmark"] < 0.5
    assert r["excess_response"] == pytest.approx(1.0 - r["br_benchmark"])


def test_half_life_ignores_small_drift():
    """Regression: a 0.01 drift in an unswapped control counted as 'never recovered'."""
    assert recovery_half_life([0.90] * 20 + [0.89] * 20, 20) == 0.0


def test_enforcement_response_reports_rival_prices():
    base = make_session([(1.9, 1.9)] * 3)
    dev = make_session([(1.9, 1.9), (1.71, 1.9), (1.9, 1.9)])  # rival ignores the cut
    r = enforcement_response(Market(), base, dev, deviator=0, dev_round=1, discount=0.95)
    assert r["response"] == 0.0 and r["rival_price_base"] == r["rival_price_dev"] == 1.9
