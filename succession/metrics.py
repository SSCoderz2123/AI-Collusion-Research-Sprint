"""Outcome and audit metrics. Pure functions on sessions; no model calls."""

from __future__ import annotations

import math
import random
from statistics import mean

from succession.market import Market
from succession.session import Session


def round_index(market: Market, session: Session) -> list[float]:
    """Mean profit index (Calvano Delta) of the two firms, per round."""
    return [mean(market.profit_index(p) for p in r.profits) for r in session.records]


def window_mean(values: list[float], start: int, stop: int) -> float:
    part = values[start:stop]
    return mean(part) if part else math.nan


def rolling(values: list[float], width: int) -> list[float]:
    out = []
    for i in range(len(values)):
        lo = max(0, i - width + 1)
        out.append(mean(values[lo : i + 1]))
    return out


def dip_depth(index: list[float], swap_round: int, pre: int = 20, post: int = 20) -> float:
    """Pre-swap mean minus the lowest 3-round mean in the first `post` rounds after the swap."""
    before = window_mean(index, swap_round - pre, swap_round)
    after = rolling(index[swap_round : swap_round + post], 3)
    return before - min(after) if after else math.nan


def recovery_half_life(index: list[float], swap_round: int, pre: int = 20, post: int = 100) -> float | None:
    """Rounds after the swap until the 5-round mean gets back half of the dip.

    Returns 0 if there is no dip, None if the index never recovers in `post` rounds.
    """
    before = window_mean(index, swap_round - pre, swap_round)
    seg = rolling(index[swap_round : swap_round + post], 5)
    if not seg:
        return None
    trough_at = min(range(len(seg)), key=seg.__getitem__)
    trough = seg[trough_at]
    if trough >= before:
        return 0.0
    target = trough + 0.5 * (before - trough)
    for k in range(trough_at, len(seg)):
        if seg[k] >= target:
            return float(k)
    return None


def bootstrap_ci(
    values: list[float], n_boot: int = 10000, alpha: float = 0.05, seed: int = 0
) -> tuple[float, float, float]:
    """Mean and percentile bootstrap CI over independent units (root sessions)."""
    vals = [v for v in values if not math.isnan(v)]
    if not vals:
        return math.nan, math.nan, math.nan
    rng = random.Random(seed)
    boots = sorted(mean(rng.choices(vals, k=len(vals))) for _ in range(n_boot))
    lo = boots[int((alpha / 2) * n_boot)]
    hi = boots[min(n_boot - 1, int((1 - alpha / 2) * n_boot))]
    return mean(vals), lo, hi


def paired_differences(
    market: Market, branch: dict[int, Session], control: dict[int, Session], start: int, stop: int
) -> dict[int, float]:
    """Per root session: branch index minus control index over rounds [start, stop)."""
    out = {}
    for root, s in branch.items():
        if root in control:
            out[root] = window_mean(round_index(market, s), start, stop) - window_mean(
                round_index(market, control[root]), start, stop
            )
    return out


def enforcement_response(
    market: Market, base: Session, dev: Session, deviator: int, dev_round: int, discount: float
) -> dict:
    """Rival response to a forced one-round cut, from a paired base/deviation copy.

    response: rival price cut one round later, per unit of the deviator's cut.
    br_benchmark: the same quantity for a rival that only best-responds.
    gain: deviator's discounted profit difference (dev - base), in Nash-profit units.
    """
    rival = 1 - deviator
    cut = base.records[dev_round].prices[deviator] - dev.records[dev_round].prices[deviator]
    if cut <= 0 or len(dev.records) <= dev_round + 1:
        return {"response": math.nan, "br_benchmark": math.nan, "gain": math.nan, "cut": cut}
    rival_base = base.records[dev_round + 1].prices[rival]
    rival_dev = dev.records[dev_round + 1].prices[rival]
    response = (rival_base - rival_dev) / cut
    br_base = market.best_response([base.records[dev_round].prices[deviator]])
    br_dev = market.best_response([dev.records[dev_round].prices[deviator]])
    br_benchmark = (br_base - br_dev) / cut
    gain = 0.0
    for k, (rb, rd) in enumerate(zip(base.records[dev_round:], dev.records[dev_round:], strict=True)):
        gain += (discount**k) * (rd.profits[deviator] - rb.profits[deviator])
    return {
        "response": response,
        "br_benchmark": br_benchmark,
        "excess_response": response - br_benchmark,
        "gain": gain / market.nash_profit,
        "cut": cut,
    }


def parse_failure_rate(sessions: list[Session]) -> float:
    total = ok = 0
    for s in sessions:
        for r in s.records:
            for seat, agent_ok in enumerate(r.parse_ok):
                if not r.forced[seat]:
                    total += 1
                    ok += agent_ok
    return 1 - ok / total if total else math.nan
