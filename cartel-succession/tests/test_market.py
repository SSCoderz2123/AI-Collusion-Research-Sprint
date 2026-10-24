import pytest

from succession.market import Market


@pytest.fixture(scope="module")
def market():
    return Market()


def test_benchmarks_match_calvano_calibration(market):
    # Published values: Nash 1.473, monopoly 1.925 (Calvano et al. 2020; Tran & Yu 2026, App. G).
    assert market.nash_price == pytest.approx(1.4729, abs=1e-3)
    assert market.monopoly_price == pytest.approx(1.9250, abs=1e-3)


def test_nash_is_fixed_point_of_best_response(market):
    assert market.best_response([market.nash_price]) == pytest.approx(market.nash_price, abs=1e-9)


def test_monopoly_maximises_joint_profit(market):
    joint = sum(market.profits([market.monopoly_price] * 2))
    for delta in (-0.05, 0.05):
        assert sum(market.profits([market.monopoly_price + delta] * 2)) < joint


def test_indices(market):
    assert market.profit_index(market.nash_profit) == pytest.approx(0.0)
    assert market.profit_index(market.monopoly_profit) == pytest.approx(1.0)
    assert market.price_index(market.monopoly_price) == pytest.approx(1.0)


def test_quantities_are_stable_for_extreme_prices(market):
    qs = market.quantities([0.0, 100.0])
    assert 0 <= qs[1] < 1e-6 and 0 < qs[0] < 1


def test_best_response_rises_with_rival_price(market):
    assert market.best_response([1.9]) > market.best_response([1.5])
