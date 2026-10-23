"""Draw the project image for the sprint submission form (PNG, 1600 x 900 px).

  python scripts/project_image.py

Reads "Apart Research/figures/figure_data.json" (written by scripts/paper_figures.py), so every
plotted value comes from stored run data (run 9). Writes "Apart Research/project_image.png".
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "Apart Research"
INK = "#16202b"
PAPER = "#ffffff"
MUTED = "#9aa7b4"
SOFT = "#c9d3dc"
CARTEL = "#e8912d"  # high prices
COMPETE = "#2bb3a3"  # competitive prices
# Run-9 conditions shown, with the condition names used in the report (scripts/paper_figures.py).
SHOWN = [
    ("control", "Control (no replacement)", "#f2f4f7", "-"),
    ("same_inherit", "Same + history", CARTEL, "-"),
    ("same_blank", "Same, no history", "#e45b6b", "--"),
    ("other_inherit", "Other + history (Mistral-7B)", COMPETE, "-"),
]
# Headline numbers, quoted from the report: Table 3 (H1-H3a verdicts and the H2 range over runs
# 4 and 6-10) and Table 5 (OLMo-2 price-hold rates 96.3-96.8%). Run 10 is not in results/ yet, so
# these cannot be recomputed here; check them against the report after any re-analysis.
STATS = [
    ("6 of 6", "runs: a new instance of the same model\nthat inherits the price history keeps the cartel"),
    ("0.47–0.67", "profit-index loss without the history,\nby pricing above the monopoly price"),
    ("96%", "of rounds: the OLMo-2 entrant repeats its\nlast price and keeps the cartel; Mistral-7B breaks it"),
]


def main() -> None:
    data = json.loads((FOLDER / "figures" / "figure_data.json").read_text(encoding="utf-8"))
    run = data["fig_trajectories"]["run"]
    series = data["fig_trajectories"]["series"]
    config = json.loads((ROOT / "results" / run / "config.json").read_text(encoding="utf-8"))
    swap = config["phase1"]["rounds"]
    n = series["control"]["n"]
    plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
    fig = plt.figure(figsize=(16, 9), dpi=100, facecolor=INK)

    fig.text(
        0.05,
        0.9,
        "AI COLLUSION RESEARCH SPRINT 2026  ·  TRACK 1: MARKETS AND COLLUSION  ·  Q1.2",
        color=MUTED,
        fontsize=13,
        fontweight="semibold",
    )
    fig.text(0.05, 0.77, "Who Carries the Cartel?", color=PAPER, fontsize=50, fontweight="bold")
    fig.text(
        0.05,
        0.655,
        "LLM price collusion survives agent replacement\nthrough the inherited price history",
        color=SOFT,
        fontsize=22,
        linespacing=1.35,
    )

    for i, (big, small) in enumerate(STATS):
        y = 0.5 - i * 0.135
        fig.text(0.05, y, big, color=CARTEL, fontsize=30, fontweight="bold", va="center")
        fig.text(0.205, y, small, color=SOFT, fontsize=13.5, linespacing=1.3, va="center")
    fig.text(0.05, 0.07, "Supratik Bhowal  ·  IEM Kolkata  ·  with Apart Research", color=MUTED, fontsize=13)

    ax = fig.add_axes((0.585, 0.29, 0.37, 0.44), facecolor="#1d2a37")
    for key, label, color, style in SHOWN:
        s = series[key]
        ax.plot(s["rounds"], s["profit_index"], color=color, lw=3.2, ls=style, label=label)
    ax.axvline(swap, color=MUTED, lw=1.2, ls=":")
    ax.text(swap + 1.5, 1.07, "agent replaced", color=MUTED, fontsize=12, va="top")
    ax.axhline(1, color="#55626f", lw=1)
    ax.axhline(0, color="#55626f", lw=1)
    ax.text(197, 1.015, "monopoly profit", color=MUTED, fontsize=11, ha="right", va="bottom")
    ax.text(62, 0.015, "competitive profit", color=MUTED, fontsize=11, ha="left", va="bottom")
    ax.set_xlim(series["control"]["rounds"][0], series["control"]["rounds"][-1])
    ax.set_ylim(-0.2, 1.1)
    ax.set_xlabel("Round", color=SOFT, fontsize=13)
    ax.set_ylabel("Profit index", color=SOFT, fontsize=13)
    ax.tick_params(colors=MUTED, labelsize=11)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#55626f")
    ax.legend(loc="upper left", frameon=False, fontsize=12, labelcolor=PAPER, ncol=2, bbox_to_anchor=(-0.02, -0.2))
    fig.text(
        0.585, 0.765, f"Run 9: mean of {n} cartel markets per condition", color=SOFT, fontsize=14, fontweight="semibold"
    )
    fig.text(
        0.585, 0.07, "Profit index: 0 = competitive (Nash) profit, 1 = monopoly profit.", color=MUTED, fontsize=11.5
    )
    out = FOLDER / "project_image.png"
    fig.savefig(out, dpi=100, facecolor=INK)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
