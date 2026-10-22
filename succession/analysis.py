"""Turn stored runs into tables (JSON + Markdown) and figures (PNG).

Unit of analysis: the root session. Branches of one root share the same
round-100 market, so branch-minus-control differences are paired.
"""

from __future__ import annotations

import math
from collections import defaultdict
from statistics import mean, median

from succession.config import ExperimentConfig
from succession.market import Market
from succession.metrics import (
    bootstrap_ci,
    dip_depth,
    paired_differences,
    parse_failure_rate,
    recovery_half_life,
    round_index,
    window_mean,
)
from succession.session import Session
from succession.store import RunStore


def price_index_series(market: Market, session: Session) -> list[float]:
    """Mean price index of the two firms per round: 0 at the Nash price, 1 at the monopoly price."""
    return [mean(market.price_index(p) for p in r.prices) for r in session.records]


def _fmt(x: float | None, nd: int = 3) -> str:
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}"


def summarize_phase2(cfg: ExperimentConfig, sessions: list[Session]) -> list[dict]:
    market = Market(cfg.market)
    swap = cfg.phase1.rounds
    end = swap + cfg.phase2.rounds
    post_start = swap + cfg.phase2.rounds // 2  # second half of phase 2
    by_branch: dict[str, dict[int, Session]] = defaultdict(dict)
    for s in sessions:
        by_branch[s.branch][s.root_id] = s
    control = by_branch.get("control", {})

    rows = []
    for branch in cfg.phase2.branches:
        group = by_branch.get(branch, {})
        if not group:
            continue
        idx = {root: round_index(market, s) for root, s in group.items()}
        diffs = paired_differences(market, group, control, post_start, end)
        d_mean, d_lo, d_hi = bootstrap_ci(list(diffs.values()))
        lives = [recovery_half_life(v, swap) for v in idx.values()]
        recovered = [x for x in lives if x is not None]
        rows.append(
            {
                "branch": branch,
                "n": len(group),
                "pre_index": mean(window_mean(v, swap - 20, swap) for v in idx.values()),
                "post_index": mean(window_mean(v, post_start, end) for v in idx.values()),
                # Price index too: prices above the monopoly price give a negative profit index,
                # which alone would read as "competitive".
                "post_price_index": mean(
                    window_mean(price_index_series(market, s), post_start, end) for s in group.values()
                ),
                "diff_vs_control": d_mean,
                "diff_ci_low": d_lo,
                "diff_ci_high": d_hi,
                "dip_depth": mean(dip_depth(v, swap) for v in idx.values()),
                "half_life_median": median(recovered) if recovered else None,
                "never_recovered": sum(x is None for x in lives),
                "parse_failure_rate": parse_failure_rate(list(group.values())),
            }
        )
    return rows


def summarize_audit(events: list[dict]) -> list[dict]:
    """An event is invalid when the deviator's base-copy price was already below the
    forced price (no real cut). Invalid events are counted, not used."""
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    invalid: dict[tuple[str, str], int] = defaultdict(int)
    for e in events:
        key = (e["branch"], e["deviator_label"])
        if "excess_response" in e and not math.isnan(e["response"]):
            groups[key].append(e)
        else:
            invalid[key] += 1
    rows = []
    for (branch, label), evs in sorted(groups.items()):
        m, lo, hi = bootstrap_ci([e["excess_response"] for e in evs])
        rows.append(
            {
                "branch": branch,
                "deviator": label,
                "n": len(evs),
                "n_invalid": invalid[(branch, label)],
                "response": mean(e["response"] for e in evs),
                "br_benchmark": mean(e["br_benchmark"] for e in evs),
                "excess_response": m,
                "excess_ci_low": lo,
                "excess_ci_high": hi,
                "deviator_gain": mean(e["gain"] for e in evs),
            }
        )
    return rows


def markdown_table(rows: list[dict], cols: list[str]) -> str:
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    body = "".join(
        "| " + " | ".join(_fmt(r[c]) if isinstance(r[c], float) or r[c] is None else str(r[c]) for c in cols) + " |\n"
        for r in rows
    )
    return head + body


def plot_trajectories(cfg: ExperimentConfig, sessions: list[Session], path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    market = Market(cfg.market)
    by_branch: dict[str, list[list[float]]] = defaultdict(list)
    for s in sessions:
        by_branch[s.branch].append(round_index(market, s))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for branch in cfg.phase2.branches:
        series = by_branch.get(branch)
        if not series:
            continue
        length = min(len(x) for x in series)
        avg = [mean(x[t] for x in series) for t in range(length)]
        ax.plot(range(length), avg, label=f"{branch} (n={len(series)})", linewidth=1.4)
    ax.axvline(cfg.phase1.rounds, color="grey", linestyle="--", linewidth=1)
    ax.axhline(0, color="black", linewidth=0.6)
    ax.axhline(1, color="black", linewidth=0.6, linestyle=":")
    ax.set_xlabel("Round")
    ax.set_ylabel("Profit index (0 = Nash, 1 = monopoly)")
    ax.set_title("Mean profit index by branch; dashed line = swap")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_differences(rows: list[dict], path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = [r for r in rows if r["branch"] != "control"]
    fig, ax = plt.subplots(figsize=(7, 4))
    xs = range(len(rows))
    means = [r["diff_vs_control"] for r in rows]
    err = [
        [m - r["diff_ci_low"] for m, r in zip(means, rows, strict=True)],
        [r["diff_ci_high"] - m for m, r in zip(means, rows, strict=True)],
    ]
    ax.bar(xs, means, yerr=err, capsize=4, color="#4C72B0")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(list(xs), [r["branch"] for r in rows], rotation=30, ha="right")
    ax.set_ylabel("Paired difference vs control (index)")
    ax.set_title("Second half of phase 2, 95% bootstrap CI")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def summarize_phase1(cfg: ExperimentConfig, sessions: list[Session], kept: set[int]) -> list[dict]:
    """One row per root session: the inclusion-rule index and what produced it."""
    market = Market(cfg.market)
    rows = []
    for s in sessions:
        idx = round_index(market, s)
        last = s.records[-10:]
        rows.append(
            {
                "root_id": s.root_id,
                "rounds": len(s.records),
                "index_select_window": window_mean(idx, cfg.phase1.select_from, cfg.phase1.rounds),
                "index_last10": window_mean(idx, len(idx) - 10, len(idx)),
                "price_index_last10": window_mean(price_index_series(market, s), len(idx) - 10, len(idx)),
                "price_seat0_last10": mean(r.prices[0] for r in last) if last else math.nan,
                "price_seat1_last10": mean(r.prices[1] for r in last) if last else math.nan,
                "parse_failure_rate": parse_failure_rate([s]),
                "kept": s.root_id in kept,
            }
        )
    return rows


def plot_phase1(cfg: ExperimentConfig, sessions: list[Session], path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    market = Market(cfg.market)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for s in sessions:
        ax.plot(round_index(market, s), linewidth=1.2, label=f"session {s.root_id}")
    ax.axhline(0, color="black", linewidth=0.6)
    ax.axhline(1, color="black", linewidth=0.6, linestyle=":")
    ax.axhline(cfg.phase1.select_threshold, color="grey", linewidth=0.8, linestyle="--")
    ax.axvspan(cfg.phase1.select_from, cfg.phase1.rounds, color="grey", alpha=0.1)
    ax.set_xlabel("Round")
    ax.set_ylabel("Profit index (0 = Nash, 1 = monopoly)")
    ax.set_title("Phase 1 profit index; shaded = selection window, dashed = threshold")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def analyze(store: RunStore) -> str:
    cfg = ExperimentConfig.from_dict(store.load_json("config.json"))
    out = ["# Run summary\n"]
    if store.exists("aa/result.json"):
        out.append(f"A/A determinism: {store.load_json('aa/result.json')}\n")
    if store.exists("phase1/selection.json"):
        sel = store.load_json("phase1/selection.json")
        out.append(f"Inclusion rule: {sel['rule']}. Kept {len(sel['kept'])} of {len(sel['sessions'])} sessions.\n")
    if store.exists("phase1/sessions.json"):
        p1 = store.load_sessions("phase1/sessions.json")
        kept = set(store.load_json("phase1/selection.json")["kept"]) if store.exists("phase1/selection.json") else set()
        rows = summarize_phase1(cfg, p1, kept)
        store.save_json("analysis/phase1_summary.json", rows)
        out.append("## Phase 1\n")
        out.append(markdown_table(rows, list(rows[0].keys())) if rows else "No data.\n")
        plot_phase1(cfg, p1, str(store.path("analysis/phase1_trajectories.png")))
    if store.exists("phase2/sessions.json"):
        sessions = store.load_sessions("phase2/sessions.json")
        rows = summarize_phase2(cfg, sessions)
        store.save_json("analysis/phase2_summary.json", rows)
        out.append("## Phase 2\n")
        out.append(markdown_table(rows, list(rows[0].keys())) if rows else "No data.\n")
        (store.root / "analysis").mkdir(exist_ok=True)
        plot_trajectories(cfg, sessions, str(store.path("analysis/trajectories.png")))
        if rows:
            plot_differences(rows, str(store.path("analysis/differences.png")))
    for folder in ("controls", "deviation"):
        name = f"{folder}/audit_events.json"
        if store.exists(name):
            rows = summarize_audit(store.load_json(name))
            store.save_json(f"analysis/{folder}_audit_summary.json", rows)
            out.append(f"## Audit: {folder}\n")
            out.append(markdown_table(rows, list(rows[0].keys())) if rows else "No data.\n")
    if store.exists("timings.json"):
        out.append("## Stage timings\n")
        out.append(markdown_table(store.load_json("timings.json"), ["stage", "started_utc", "seconds"]))
    text = "\n".join(out)
    (store.root / "analysis").mkdir(exist_ok=True)
    store.path("analysis/summary.md").write_text(text, encoding="utf-8")
    return text
