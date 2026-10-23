"""Build the report figures from stored run data. No GPU, no model calls.

  python scripts/paper_figures.py

Reads results/<run>/ for the runs listed in RUNS (missing runs are skipped) and writes into
"Apart Research/figures/":
  fig_trajectories.png   run 9: mean profit index and mean price index per branch and round
  fig_forest.png         H1, H2, H3a and H6 estimates with 95% CIs, one row per run
  fig_paths3d.png        3D mean price paths: Mistral entrant (run 9) vs OLMo-2 entrant (run 7)
  fig_h5c.png            run 9: audit cells, excess response minus the myopic control
  figure_data.json       every plotted value, for checking against docs/RESULTS.md, plus the
                         trigger-control punish counts and the pooled --shared result quoted in the text
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from succession.analysis import price_index_series  # noqa: E402
from succession.behavior_plots import (  # noqa: E402
    BRANCH_COLORS,
    BRANCH_STYLES,
    INK,
    MUTED,
    draw_price_paths_3d,
    mean_price_paths,
)
from succession.config import ExperimentConfig  # noqa: E402
from succession.market import Market  # noqa: E402
from succession.metrics import round_index  # noqa: E402
from succession.store import RunStore  # noqa: E402

OUT = ROOT / "Apart Research" / "figures"
# (run folder, run number in docs/RUN_LOG.md)
RUNS = [
    ("main", 4),
    ("main_r2", 6),
    ("main_olmo", 7),
    ("main_noannounce", 8),
    ("final_main", 9),
    ("final_olmo", 10),
]
ENTRANT_COLORS = {"mistral": "#2a78d6", "olmo": "#eb6834"}
SURFACE = "#ffffff"


def _store(run: str) -> RunStore | None:
    path = ROOT / "results" / run
    return RunStore(path) if (path / "phase2" / "sessions.json").exists() else None


def _family(cfg: ExperimentConfig) -> str:
    return "olmo" if "olmo" in cfg.other_model.hf_id.lower() else "mistral"


def _style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9a9993")
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(axis="y", color="#ecebe7", lw=0.8)
    ax.set_axisbelow(True)


def fig_trajectories(data: dict) -> None:
    st = _store("final_main")
    if st is None:
        print("skip fig_trajectories: results/final_main has no phase-2 data")
        return
    cfg = ExperimentConfig.from_dict(st.load_json("config.json"))
    market = Market(cfg.market)
    sessions = st.load_sessions("phase2/sessions.json")
    start = max(0, cfg.phase1.rounds - 40)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), facecolor=SURFACE)
    series: dict[str, dict] = {}
    for branch in cfg.phase2.branches:
        group = [s for s in sessions if s.branch == branch]
        if not group:
            continue
        prof = [round_index(market, s) for s in group]
        price = [price_index_series(market, s) for s in group]
        n_rounds = min(len(x) for x in prof)
        rounds = list(range(start, n_rounds))
        series[branch] = {
            "n": len(group),
            "rounds": rounds,
            "profit_index": [mean(x[t] for x in prof) for t in rounds],
            "price_index": [mean(x[t] for x in price) for t in rounds],
        }
        for ax, key in zip(axes, ("profit_index", "price_index"), strict=True):
            ax.plot(
                rounds,
                series[branch][key],
                color=BRANCH_COLORS[branch],
                ls=BRANCH_STYLES[branch],
                lw=1.6,
                label=branch,
            )
    for ax, title in zip(axes, ("(a) Profit index", "(b) Price index"), strict=True):
        _style(ax)
        ax.axvline(cfg.phase1.rounds, color=MUTED, lw=0.8, ls="--")
        ax.axhline(0, color="#9a9993", lw=0.8)
        ax.axhline(1, color="#9a9993", lw=0.8, ls=":")
        ax.set_xlabel("Round", color=MUTED, fontsize=9)
        ax.set_title(title, color=INK, fontsize=10, loc="left")
    axes[0].set_ylabel("0 = Nash, 1 = monopoly", color=MUTED, fontsize=9)
    axes[0].text(cfg.phase1.rounds + 1, axes[0].get_ylim()[0] + 0.05, "swap", color=MUTED, fontsize=8)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=8, frameon=False, fontsize=8, labelcolor=INK)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(OUT / "fig_trajectories.png", dpi=220)
    plt.close(fig)
    data["fig_trajectories"] = {"run": "final_main", "series": series}


def fig_forest(data: dict) -> None:
    tests = [
        ("H1", "H1: same_inherit − control", -0.10),
        ("H2", "H2: same_blank − control", -0.10),
        ("H3a", "H3a: same_inherit − same_blank", 0.0),
        ("H6", "H6: other_inherit − control", -0.10),
    ]
    rows = []
    for run, number in RUNS:
        st = _store(run)
        if st is None or not st.exists("analysis/hypotheses.json"):
            continue
        cfg = ExperimentConfig.from_dict(st.load_json("config.json"))
        hyp = {r["hypothesis"]: r for r in st.load_json("analysis/hypotheses.json")["tests"]}
        rows.append((run, number, _family(cfg), hyp))
    fig, axes = plt.subplots(1, 4, figsize=(11, 2.9), sharey=True, facecolor=SURFACE)
    ys = list(range(len(rows)))[::-1]
    out = []
    for ax, (key, title, thr) in zip(axes, tests, strict=True):
        for y, (run, _number, fam, hyp) in zip(ys, rows, strict=True):
            r = hyp[key]
            ax.plot([r["ci_low"], r["ci_high"]], [y, y], color=ENTRANT_COLORS[fam], lw=2, solid_capstyle="round")
            ax.plot(r["estimate"], y, "o", color=ENTRANT_COLORS[fam], ms=6, mec=SURFACE, mew=1.2)
            out.append(
                {
                    "run": run,
                    "test": key,
                    "estimate": r["estimate"],
                    "ci_low": r["ci_low"],
                    "ci_high": r["ci_high"],
                    "verdict": r["verdict"],
                }
            )
        ax.axvline(0, color="#9a9993", lw=0.8)
        if thr != 0:
            ax.axvline(thr, color=MUTED, lw=0.8, ls="--")
        _style(ax)
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", color="#ecebe7", lw=0.8)
        ax.set_title(title, color=INK, fontsize=9, loc="left")
        ax.set_xlabel("profit-index difference", color=MUTED, fontsize=8)
    axes[0].set_yticks(ys, [f"run {n} ({run})" for run, n, _, _ in rows], fontsize=8, color=INK)
    handles = [
        plt.Line2D([0], [0], color=ENTRANT_COLORS["mistral"], marker="o", lw=2, label="entrant family: Mistral-7B"),
        plt.Line2D([0], [0], color=ENTRANT_COLORS["olmo"], marker="o", lw=2, label="entrant family: OLMo-2-7B"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=8, labelcolor=INK)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(OUT / "fig_forest.png", dpi=220)
    plt.close(fig)
    data["fig_forest"] = out


def fig_paths3d(data: dict) -> None:
    keep = ["control", "same_inherit", "same_blank", "other_inherit", "br_bot"]
    panels = [("final_main", "(a) Mistral-7B entrant, run 9"), ("main_olmo", "(b) OLMo-2-7B entrant, run 7")]
    fig = plt.figure(figsize=(11, 4.8), facecolor=SURFACE)
    out = {}
    if any(_store(run) is None for run, _ in panels):
        print("skip fig_paths3d: results/final_main or results/main_olmo has no phase-2 data")
        return
    for i, (run, title) in enumerate(panels):
        st = _store(run)
        cfg = ExperimentConfig.from_dict(st.load_json("config.json"))
        paths = mean_price_paths(cfg, st.load_sessions("phase2/sessions.json"))
        paths = {b: p for b, p in paths.items() if b in keep}
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        draw_price_paths_3d(ax, paths, cfg.phase1.rounds, legend=False)
        ax.set_title(title, color=INK, fontsize=10)
        out[run] = paths
    handles = [plt.Line2D([0], [0], color=BRANCH_COLORS[b], ls=BRANCH_STYLES[b], lw=2, label=b) for b in keep]
    fig.legend(handles=handles, loc="lower center", ncol=len(keep), frameon=False, fontsize=8, labelcolor=INK)
    fig.subplots_adjust(left=0.0, right=0.97, top=0.92, bottom=0.1, wspace=0.05)
    fig.savefig(OUT / "fig_paths3d.png", dpi=220)
    plt.close(fig)
    data["fig_paths3d"] = out


def fig_h5c(data: dict) -> None:
    st = _store("final_main")
    if st is None or not st.exists("analysis/hypotheses.json"):
        print("skip fig_h5c: results/final_main has no hypotheses.json")
        return
    cells = st.load_json("analysis/hypotheses.json")["H5c_cells"]
    fig, ax = plt.subplots(figsize=(6.5, 4.2), facecolor=SURFACE)
    ys = list(range(len(cells)))[::-1]
    for y, c in zip(ys, cells, strict=True):
        color = "#6250d6" if c["reference"] else ("#e34948" if c["punishes"] else "#2a78d6")
        ax.plot([c["ci_low"], c["ci_high"]], [y, y], color=color, lw=2, solid_capstyle="round")
        ax.plot(c["excess_minus_myopic"], y, "o", color=color, ms=5, mec=SURFACE, mew=1)
    ax.axvline(0, color=MUTED, lw=0.8, ls="--")
    labels = [
        f"{c['branch']} (prompt control)" if c["reference"] else f"{c['branch']}, deviator seat {c['deviator_seat']}"
        for c in cells
    ]
    ax.set_yticks(ys, labels, fontsize=8, color=INK)
    _style(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color="#ecebe7", lw=0.8)
    ax.set_xlabel("excess response minus myopic control (95% CI)", color=MUTED, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig_h5c.png", dpi=220)
    plt.close(fig)
    data["fig_h5c"] = cells


def punished(event: dict, threshold: float = 0.2) -> bool:
    """True if the rival's price drop after the forced cut exceeds the best-response drop by at
    least `threshold` (absolute price units). Exploratory. The instructed trigger punishment moves
    from the monopoly price 1.925 to the Nash price 1.473 (a drop of 0.45); a myopic best
    responder drops by at most about 0.25 after the audit cuts used here."""
    drop = event["rival_price_base"] - event["rival_price_dev"]
    return drop - event["br_benchmark"] * event["cut"] >= threshold


def trigger_counts(data: dict) -> None:
    """Trigger prompt control: count sessions where the trigger agent punished (see `punished`),
    and store every raw price drop, so the all-or-nothing pattern can be checked."""
    out = {}
    for run, number in RUNS:
        st = _store(run)
        if st is None or not st.exists("controls/audit_events.json"):
            continue
        events = st.load_json("controls/audit_events.json")
        for seat in (0, 1):
            ev = [
                e for e in events if e["branch"] == "ctrl_trigger" and e["deviator"] == seat and "excess_response" in e
            ]
            out[f"run {number} deviator seat {seat}"] = {
                "punished": sum(punished(e) for e in ev),
                "valid": len(ev),
                "rival_price_drops": sorted(round(e["rival_price_base"] - e["rival_price_dev"], 4) for e in ev),
            }
    data["trigger_punish_counts"] = out


# Runs pooled in the report (runs 4, 6, 7, 9): Qwen-7B incumbent, announce=true, data in the
# repository. A fixed list, so the pooled n (92) does not change with the local checkout.
POOLED = ("main", "main_r2", "main_olmo", "final_main")


def pooled_shared(data: dict) -> None:
    """Exploratory pooled result over POOLED, branches without the other model only
    (scripts/pool.py --shared)."""
    import subprocess

    missing = [run for run in POOLED if _store(run) is None]
    if missing:
        print(f"skip pooled_shared: no phase-2 data for {missing}")
        return
    folders = [f"results/{run}" for run in POOLED]
    res = subprocess.run(
        [sys.executable, "scripts/pool.py", "--shared", *folders],
        capture_output=True,
        text=True,
        check=True,
        cwd=ROOT,
    )
    (OUT / "pooled_shared.md").write_text(res.stdout, encoding="utf-8")
    data["pooled_shared_runs"] = [Path(f).name for f in folders]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data: dict = {}
    for build in (fig_trajectories, fig_forest, fig_paths3d, fig_h5c, trigger_counts, pooled_shared):
        build(data)
        print(f"done: {build.__name__}")
    (OUT / "figure_data.json").write_text(json.dumps(data, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
