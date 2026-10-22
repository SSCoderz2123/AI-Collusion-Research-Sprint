import pytest

from succession.parsing import parse_reply
from succession.prompts import HistoryRow, build_prompt


@pytest.mark.parametrize(
    "text, price",
    [
        ('{"notes": "hold", "price": 1.85}', 1.85),
        ('```json\n{"notes": "x", "price": "1.7"}\n```', 1.7),
        ('Thinking... {"notes": "a"} then {"notes": "b", "price": 1.6}', 1.6),
        ("I choose price: 1.75", 1.75),
    ],
)
def test_parse_ok(text, price):
    r = parse_reply(text, 0.0, 10.0)
    assert r.ok and r.price == pytest.approx(price)


@pytest.mark.parametrize("text", ["no number here", '{"price": 55}', '{"price": -1}', '{"price": "nan"}'])
def test_parse_fail(text):
    assert not parse_reply(text, 0.0, 10.0).ok


def test_default_prompt_is_neutral():
    p = build_prompt(variant="default", cost=1.0, history=[], notes="", current_round=0)
    lowered = p.lower()
    for word in ("collu", "cartel", "coordinat", "punish", "cooperat"):
        assert word not in lowered


def test_prompt_contains_history_notice_and_notes():
    rows = [HistoryRow(round=3, own_price=1.8, rival_price=1.9, own_quantity=0.4, own_profit=0.32)]
    p = build_prompt(variant="default", cost=1.0, history=rows, notes="keep high", current_round=4, notice="N1")
    assert "other firm's price 1.90" in p and "Notice: N1" in p and "keep high" in p and "period 4" in p


def test_trigger_requires_prices():
    with pytest.raises(ValueError):
        build_prompt(variant="trigger", cost=1.0, history=[], notes="", current_round=0)


def test_unknown_variant():
    with pytest.raises(ValueError):
        build_prompt(variant="nope", cost=1.0, history=[], notes="", current_round=0)
