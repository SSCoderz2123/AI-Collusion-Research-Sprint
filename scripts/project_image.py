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
from matplotlib.patches import Ellipse, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "Apart Research"
# Infographic style: cream page, rounded pastel cards, navy text, teal and terracotta accents
# (the same palette as the slides).
BG = "#f6f1e8"
INK = "#1e2a44"
MUTED = "#626b7f"
EDGE = "#e7dccb"
TEAL = "#1f6f8b"
TERRA = "#c8553d"
SAGE = "#5e8c61"
PLUM = "#6a5a9c"
BADGES = [TEAL, TERRA, SAGE]
PASTEL = ["#dcebf0", "#f8e1d7", "#e4eedf", "#e8e3f2"]
# Run-9 conditions shown, with the condition names used in the report (scripts/paper_figures.py).
SHOWN = [
    ("control", "Control (no replacement)", INK, "-"),
    ("same_inherit", "Same + history", TEAL, "-"),
    ("same_blank", "Same, no history", TERRA, "--"),
    ("other_inherit", "Other + history (Mistral-7B)", SAGE, "-"),
]
# Headline numbers, quoted from the report: Table 3 (H1-H3a verdicts and the H2 range over runs
# 4 and 6-10) and Table 5 (OLMo-2 price-hold rates 96.3-96.8%). Run 10 is not in results/ yet, so
# these cannot be recomputed here; check them against the report after any re-analysis.
STATS = [
    ("6 of 6", "runs: the same model with the\ninherited price history keeps\nthe cartel"),
    ("0.47–0.67", "profit-index loss without the\nhistory, by pricing above\nthe monopoly price"),
    ("96%", "of rounds the OLMo-2 entrant\nrepeats its last price and keeps\nthe cartel; Mistral-7B breaks it"),
]


def card(fig, x, y, w, h, color, edge=EDGE):
    fig.patches.append(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0,rounding_size=0.018",
            transform=fig.transFigure,
            facecolor=color,
            edgecolor=edge,
            linewidth=1.2,
            zorder=-2,
        )
    )


def main() -> None:
    data = json.loads((FOLDER / "figures" / "figure_data.json").read_text(encoding="utf-8"))
    run = data["fig_trajectories"]["run"]
    series = data["fig_trajectories"]["series"]
    config = json.loads((ROOT / "results" / run / "config.json").read_text(encoding="utf-8"))
    swap = config["phase1"]["rounds"]
    n = series["control"]["n"]
    plt.rcParams["font.family"] = ["Times New Roman", "Liberation Serif", "DejaVu Serif"]
    fig = plt.figure(figsize=(16, 9), dpi=100, facecolor=BG)

    fig.text(
        0.05,
        0.915,
        "AI COLLUSION RESEARCH SPRINT 2026  ·  TRACK 1: MARKETS AND COLLUSION  ·  Q1.2",
        color=TEAL,
        fontsize=13,
        fontweight="bold",
    )
    fig.text(0.05, 0.82, "Who Carries the Cartel?", color=INK, fontsize=46, fontweight="bold")
    fig.text(
        0.05,
        0.765,
        "LLM price collusion survives agent replacement through inherited price history",
        color=MUTED,
        fontsize=19,
        style="italic",
    )

    # How it works: three numbered steps.
    steps = [
        ("Form a cartel", "Two Qwen2.5-7B agents set\nprices for 100 rounds"),
        ("Replace one agent", "Copy each cartel into 8 paired\nconditions at round 100"),
        ("Measure", "Profit index in rounds 150–199\n(0 = competitive, 1 = monopoly)"),
    ]
    for i, (head, body) in enumerate(steps):
        x = 0.05 + i * 0.172
        card(fig, x, 0.52, 0.16, 0.19, PASTEL[i])
        fig.patches.append(
            Ellipse((x + 0.022, 0.675), 0.028 * 9 / 16, 0.028, transform=fig.transFigure, color=BADGES[i], zorder=-1)
        )
        fig.text(x + 0.022, 0.675, str(i + 1), color="white", fontsize=14, fontweight="bold", ha="center", va="center")
        fig.text(x + 0.044, 0.675, head, color=INK, fontsize=15, fontweight="bold", va="center")
        fig.text(x + 0.012, 0.6, body, color=INK, fontsize=12.5, va="center", linespacing=1.35)

    # Key findings.
    for i, (big, small) in enumerate(STATS):
        x = 0.05 + i * 0.172
        card(fig, x, 0.17, 0.16, 0.3, "#fffbf4")
        fig.text(x + 0.012, 0.405, big, color=[TEAL, TERRA, PLUM][i], fontsize=30, fontweight="bold", va="center")
        fig.text(x + 0.012, 0.305, small, color=INK, fontsize=12, va="center", linespacing=1.35)
    fig.text(0.05, 0.085, "Supratik Bhowal  ·  with Apart Research", color=MUTED, fontsize=14)

    card(fig, 0.6, 0.12, 0.355, 0.59, "#fffbf4")
    fig.text(0.62, 0.665, f"Run 9: mean of {n} cartel markets per condition", color=INK, fontsize=15, fontweight="bold")
    ax = fig.add_axes((0.655, 0.32, 0.28, 0.31), facecolor="#fffbf4", zorder=1)
    for key, label, color, style in SHOWN:
        s = series[key]
        ax.plot(s["rounds"], s["profit_index"], color=color, lw=2.8, ls=style, label=label)
    ax.axvline(swap, color=MUTED, lw=1.2, ls=":")
    ax.text(swap + 1.5, 1.07, "agent replaced", color=MUTED, fontsize=12, va="top")
    ax.axhline(1, color=EDGE, lw=1.2)
    ax.axhline(0, color=EDGE, lw=1.2)
    ax.text(197, 1.015, "monopoly profit", color=MUTED, fontsize=11, ha="right", va="bottom")
    ax.text(62, 0.015, "competitive profit", color=MUTED, fontsize=11, ha="left", va="bottom")
    ax.set_xlim(series["control"]["rounds"][0], series["control"]["rounds"][-1])
    ax.set_ylim(-0.2, 1.1)
    ax.set_xlabel("Round", color=INK, fontsize=13)
    ax.set_ylabel("Profit index", color=INK, fontsize=13)
    ax.tick_params(colors=MUTED, labelsize=11)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.legend(loc="upper left", frameon=False, fontsize=12, labelcolor=INK, ncol=2, bbox_to_anchor=(-0.12, -0.17))
    out = FOLDER / "project_image.png"
    fig.savefig(out, dpi=100, facecolor=BG)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
