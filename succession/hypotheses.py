"""Pre-registered hypothesis tests H1-H5 (docs/PREREGISTRATION.md).

Every difference is paired per root session and uses the post window (second half of
phase 2). CIs are 95% percentile bootstrap over root sessions (H1-H4) or over audit
events (H5), with 10,000 resamples. Verdict rule from the pre-registration:

  supported      the whole CI is on the stated side of the threshold
  not supported  the whole CI is on the other side
  inconclusive   the CI includes the threshold
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from statistics import mean

from succession.config import ExperimentConfig
from succession.market import Market
from succession.metrics import bootstrap_ci, round_index, window_mean
from succession.session import Session

N_BOOT = 10000


def verdict(lo: float, hi: float, threshold: float, side: str) -> str:
    """side '>' means the hypothesis claims value > threshold; '<' claims value < threshold."""
    if math.isnan(lo) or math.isnan(hi):
        return "no data"
    above, below = lo > threshold, hi < threshold
    if side == ">":
        return "supported" if above else "not supported" if below else "inconclusive"
    return "supported" if below else "not supported" if above else "inconclusive"


def _post_means(cfg: ExperimentConfig, sessions: list[Session], price: bool = False) -> dict[str, dict[int, float]]:
    """Post-window mean per branch and root: profit index, or price index when price=True."""
    market = Market(cfg.market)
    swap = cfg.phase1.rounds
    end = swap + cfg.phase2.rounds
    start = swap + cfg.phase2.rounds // 2
    out: dict[str, dict[int, float]] = defaultdict(dict)
    for s in sessions:
        if price:
            series = [mean(market.price_index(p) for p in r.prices) for r in s.records]
        else:
            series = round_index(market, s)
        out[s.branch][s.root_id] = window_mean(series, start, end)
    return out


def _paired(post: dict[str, dict[int, float]], a: str, b: str) -> dict[int, float]:
    return {r: post[a][r] - post[b][r] for r in post.get(a, {}) if r in post.get(b, {})}


def _row(name: str, claim: str, values: list[float], threshold: float, side: str) -> dict:
    m, lo, hi = bootstrap_ci(values, n_boot=N_BOOT)
    return {
        "hypothesis": name,
        "claim": claim,
        "n": len(values),
        "estimate": m,
        "ci_low": lo,
        "ci_high": hi,
        "verdict": verdict(lo, hi, threshold, side),
    }


def _h4(post: dict[str, dict[int, float]]) -> dict:
    """|si - oi| < |si - sb|: bootstrap of |mean(si - sb)| - |mean(si - oi)| over roots, claim > 0."""
    si_sb = _paired(post, "same_inherit", "same_blank")
    si_oi = _paired(post, "same_inherit", "other_inherit")
    roots = sorted(set(si_sb) & set(si_oi))
    if not roots:
        return _row("H4", "|si-sb| - |si-oi| > 0", [], 0.0, ">")
    rng = random.Random(0)
    stats = []
    for _ in range(N_BOOT):
        pick = rng.choices(roots, k=len(roots))
        stats.append(abs(mean(si_sb[r] for r in pick)) - abs(mean(si_oi[r] for r in pick)))
    stats.sort()
    est = abs(mean(si_sb[r] for r in roots)) - abs(mean(si_oi[r] for r in roots))
    lo, hi = stats[int(0.025 * N_BOOT)], stats[min(N_BOOT - 1, int(0.975 * N_BOOT))]  # same rule as bootstrap_ci
    return {
        "hypothesis": "H4",
        "claim": "|si-sb| - |si-oi| > 0",
        "n": len(roots),
        "estimate": est,
        "ci_low": lo,
        "ci_high": hi,
        "verdict": verdict(lo, hi, 0.0, ">"),
    }


def _h5(events: list[dict]) -> tuple[dict, list[dict]]:
    """No cell (branch x deviator seat) with an LLM responder has a CI entirely above 0."""
    cells: dict[tuple[str, int], list[float]] = defaultdict(list)
    for e in events:
        if "excess_response" not in e or math.isnan(e.get("response", math.nan)):
            continue
        # The responder is the other seat. In br_bot the entrant seat (1) is the bot.
        responder_is_bot = e["branch"] == "br_bot" and e["deviator"] == 0
        if not responder_is_bot:
            cells[(e["branch"], e["deviator"])].append(e["excess_response"])
    rows = []
    for (branch, dev), vals in sorted(cells.items()):
        m, lo, hi = bootstrap_ci(vals, n_boot=N_BOOT)
        rows.append(
            {
                "branch": branch,
                "deviator_seat": dev,
                "n": len(vals),
                "excess_response": m,
                "ci_low": lo,
                "ci_high": hi,
                "punishes": lo > 0,
            }
        )
    violations = [r for r in rows if r["punishes"]]
    summary = {
        "hypothesis": "H5",
        "claim": "no LLM responder has excess response CI > 0 (estimate = cells with CI > 0)",
        "n": len(rows),
        "estimate": float(len(violations)),
        "ci_low": math.nan,
        "ci_high": math.nan,
        "verdict": "no data" if not rows else ("supported" if not violations else "not supported"),
    }
    return summary, rows


def evaluate(cfg: ExperimentConfig, sessions: list[Session], events: list[dict] | None) -> dict:
    post = _post_means(cfg, sessions)
    rows = [
        _row(
            "H1", "same_inherit - control > -0.10", list(_paired(post, "same_inherit", "control").values()), -0.10, ">"
        ),
        _row("H2", "same_blank - control < -0.10", list(_paired(post, "same_blank", "control").values()), -0.10, "<"),
        _row(
            "H3a", "same_inherit - same_blank > 0", list(_paired(post, "same_inherit", "same_blank").values()), 0.0, ">"
        ),
        _row(
            "H3b",
            "other_inherit - other_blank > 0",
            list(_paired(post, "other_inherit", "other_blank").values()),
            0.0,
            ">",
        ),
        _h4(post),
    ]
    h3 = [r for r in rows if r["hypothesis"] in ("H3a", "H3b")]
    h3_verdict = (
        "supported"
        if all(r["verdict"] == "supported" for r in h3)
        else "not supported"
        if any(r["verdict"] == "not supported" for r in h3)
        else "inconclusive"
    )
    h5_cells: list[dict] = []
    if events is not None:
        h5, h5_cells = _h5(events)
        rows.append(h5)
    # Secondary outcome (pre-registered): paired post-window price index, branch - control.
    price_post = _post_means(cfg, sessions, price=True)
    secondary = []
    for branch in cfg.phase2.branches:
        if branch == "control":
            continue
        vals = list(_paired(price_post, branch, "control").values())
        m, lo, hi = bootstrap_ci(vals, n_boot=N_BOOT)
        secondary.append({"branch": branch, "n": len(vals), "price_index_diff": m, "ci_low": lo, "ci_high": hi})
    return {"tests": rows, "H3_combined": h3_verdict, "H5_cells": h5_cells, "price_index_vs_control": secondary}
