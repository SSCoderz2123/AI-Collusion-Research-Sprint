import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _module():
    spec = importlib.util.spec_from_file_location("paper_figures", ROOT / "scripts" / "paper_figures.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _event(drop: float, br_benchmark: float, cut: float = 0.17) -> dict:
    return {"rival_price_base": 1.92, "rival_price_dev": 1.92 - drop, "br_benchmark": br_benchmark, "cut": cut}


def test_punished_needs_a_drop_beyond_the_best_response():
    punished = _module().punished
    assert punished(_event(0.45, 0.4))  # trigger punishment: 0.45 - 0.068 >= 0.2
    assert not punished(_event(0.0, 0.4))  # no reaction
    # A myopic best responder that drops by 0.247 is not punishment, although 0.247 > 0.2.
    assert not punished(_event(0.247, 0.247 / 0.6, cut=0.6))
