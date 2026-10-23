"""Exploratory behavior-space figures (3D) from stored phase-2 sessions. No model calls.

Two figures per run, both in price-index units (0 = Nash price, 1 = monopoly price):

  price_paths_3d.png      mean price path per branch: round x incumbent (seat 0) x entrant (seat 1)
  price_path_pca_3d.png   one point per session: PCA of its post-swap price path (both seats)

The data behind each figure is saved as JSON next to it, so every plotted value can be read as a
table. These figures were defined after the runs had been seen: label them "exploratory".
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean

from succession.branches import BRANCHES
from succession.config import ExperimentConfig
from succession.market import Market
from succession.session import Session
from succession.store import RunStore

# Fixed categorical order (reference palette, colour-blind checked). The colour follows the branch,
# never its rank, so a branch has the same colour in every run and figure.
BRANCH_COLORS = dict(
    zip(
        BRANCHES,
        ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"],
        strict=True,
    )
)
# Second encoding, so that identity never depends on colour alone (3 colours have < 3:1 contrast).
BRANCH_STYLES = dict(zip(BRANCHES, ["-", "--", "-", "-.", ":", "-", "--", "-."], strict=True))
BRANCH_MARKERS = dict(zip(BRANCHES, ["o", "s", "^", "v", "D", "P", "X", "*"], strict=True))
INK, MUTED = "#0b0b0b", "#52514e"
FLOOR_COLOR = "#e4e3de"  # grey base plane under each 3D figure
SHADOW_ALPHA = 0.28  # projections onto the base plane: a faint copy of each mark in its own colour


def _price_index_rows(market: Market, s: Session, start: int, stop: int) -> list[list[float]]:
    return [[market.price_index(p) for p in r.prices] for r in s.records[start:stop]]


def mean_price_paths(cfg: ExperimentConfig, sessions: list[Session], before: int = 10) -> dict[str, dict]:
    """Per branch: mean price index of each seat per round, from `before` rounds before the swap."""
    market = Market(cfg.market)
    swap, end = cfg.phase1.rounds, cfg.phase1.rounds + cfg.phase2.rounds
    start = max(0, swap - before)
    groups: dict[str, list[list[list[float]]]] = defaultdict(list)
    for s in sessions:
        if len(s.records) >= end:
            groups[s.branch].append(_price_index_rows(market, s, start, end))
    out = {}
    for branch in cfg.phase2.branches:
        rows = groups.get(branch)
        if not rows:
            continue
        out[branch] = {
            "n": len(rows),
            "rounds": list(range(start, end)),
            "seat0": [mean(r[t][0] for r in rows) for t in range(end - start)],
            "seat1": [mean(r[t][1] for r in rows) for t in range(end - start)],
        }
    return out


def pca3(vectors: list[list[float]]) -> tuple[list[list[float]], list[float]]:
    """First 3 principal components (centred, no scaling) and their explained-variance ratios."""
    import numpy as np

    x = np.asarray(vectors, dtype=float)
    x = x - x.mean(axis=0)
    _, sing, vt = np.linalg.svd(x, full_matrices=False)
    k = min(3, vt.shape[0])
    coords = x @ vt[:k].T
    var = sing**2
    ratios = (var[:k] / var.sum()).tolist() if var.sum() > 0 else [0.0] * k
    if k < 3:  # fewer sessions than 3 components: pad, so plots and JSON keep 3 columns
        coords = np.hstack([coords, np.zeros((coords.shape[0], 3 - k))])
        ratios += [0.0] * (3 - k)
    return coords.tolist(), ratios


def path_pca(cfg: ExperimentConfig, sessions: list[Session]) -> dict:
    """One vector per session: seat-0 then seat-1 price index over the post-swap rounds."""
    market = Market(cfg.market)
    swap, end = cfg.phase1.rounds, cfg.phase1.rounds + cfg.phase2.rounds
    keep = [s for s in sessions if len(s.records) >= end and s.branch in cfg.phase2.branches]
    vectors = []
    for s in keep:
        rows = _price_index_rows(market, s, swap, end)
        vectors.append([r[0] for r in rows] + [r[1] for r in rows])
    if len(vectors) < 2:
        return {"explained": [], "points": []}
    coords, ratios = pca3(vectors)
    points = [
        {"branch": s.branch, "root_id": s.root_id, "pc1": c[0], "pc2": c[1], "pc3": c[2]}
        for s, c in zip(keep, coords, strict=True)
    ]
    return {"explained": ratios, "points": points}


def _floor(ax, xs: list[float], ys: list[float], z: float) -> None:
    """Draw a grey base plane at height z under the data, as a reference for the shadows."""
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    dx, dy = 0.04 * (x1 - x0 or 1.0), 0.04 * (y1 - y0 or 1.0)
    corners = [(x0 - dx, y0 - dy, z), (x1 + dx, y0 - dy, z), (x1 + dx, y1 + dy, z), (x0 - dx, y1 + dy, z)]
    ax.add_collection3d(Poly3DCollection([corners], facecolors=FLOOR_COLOR, edgecolors="#cfcec8", alpha=0.6))


def _floor_height(zs: list[float]) -> float:
    lo, hi = min(zs), max(zs)
    return lo - 0.15 * (hi - lo or 1.0)


def _label_centroids(ax, centroids: list[tuple[str, float, float, float]], min_gap: float = 0.08) -> None:
    """Direct label at each branch centroid, in text ink, skipping labels that would collide.

    Two centroids collide when they are closer than min_gap of the axis range in both PC1 and PC2.
    The legend still identifies every branch, so a skipped label loses no information."""
    if not centroids:
        return
    xs, ys = [c[1] for c in centroids], [c[2] for c in centroids]
    rx, ry = (max(xs) - min(xs)) or 1.0, (max(ys) - min(ys)) or 1.0
    placed: list[tuple[float, float]] = []
    for name, x, y, z in centroids:
        if any(abs(x - px) < min_gap * rx and abs(y - py) < min_gap * ry for px, py in placed):
            continue
        placed.append((x, y))
        ax.text(x, y, z, f" {name}", color=INK, fontsize=8)


def _style_axes(ax) -> None:
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor("#fcfcfb")
        axis.pane.set_edgecolor("#d9d8d4")
        axis._axinfo["grid"]["color"] = "#e6e5e1"  # recessive grid
        axis.label.set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)


def plot_price_paths_3d(paths: dict[str, dict], swap: int, title: str, path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(9, 6.5), facecolor="#fcfcfb")
    ax = fig.add_subplot(projection="3d")
    rounds = next(iter(paths.values()))["rounds"] if paths else []
    if rounds:
        all_y = [v for p in paths.values() for v in p["seat0"]] + [0.0, 1.0]
        all_z = [v for p in paths.values() for v in p["seat1"]] + [0.0, 1.0]
        zf = _floor_height(all_z)
        _floor(ax, rounds, all_y, zf)
        for branch, p in paths.items():  # shadow of each path on the base plane
            ax.plot(
                p["rounds"],
                p["seat0"],
                [zf] * len(p["rounds"]),
                color=BRANCH_COLORS[branch],
                lw=1.5,
                alpha=SHADOW_ALPHA,
            )
        ax.set_zlim(zf, max(all_z) + 0.05)
        for level, name in ((0.0, "Nash"), (1.0, "monopoly")):
            ax.plot(rounds, [level] * len(rounds), [level] * len(rounds), color="#9a9993", lw=1, ls=":")
            ax.text(rounds[-1], level, level, f" {name}", color=MUTED, fontsize=8)
    for branch, p in paths.items():
        ax.plot(
            p["rounds"],
            p["seat0"],
            p["seat1"],
            color=BRANCH_COLORS[branch],
            ls=BRANCH_STYLES[branch],
            lw=2,
            label=f"{branch} (n={p['n']})",
        )
    if rounds:
        ax.plot([swap, swap], [0, 0], [zf, 1], color=MUTED, lw=1, ls="--")
        ax.text(swap, 0, 1, " swap", color=MUTED, fontsize=8)
    ax.set_xlabel("Round")
    ax.set_ylabel("Incumbent price index")
    ax.set_zlabel("Entrant-seat price index")
    _style_axes(ax)
    ax.view_init(elev=22, azim=-60)
    ax.set_title(title, color=INK, fontsize=11)
    ax.legend(fontsize=8, loc="upper left", frameon=False, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_path_pca_3d(pca: dict, title: str, path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(9, 6.5), facecolor="#fcfcfb")
    ax = fig.add_subplot(projection="3d")
    by_branch: dict[str, list[dict]] = defaultdict(list)
    for pt in pca["points"]:
        by_branch[pt["branch"]].append(pt)
    if pca["points"]:
        zf = _floor_height([p["pc3"] for p in pca["points"]])
        _floor(ax, [p["pc1"] for p in pca["points"]], [p["pc2"] for p in pca["points"]], zf)
        for branch, pts in by_branch.items():  # shadow of each point on the base plane
            ax.scatter(
                [p["pc1"] for p in pts],
                [p["pc2"] for p in pts],
                [zf] * len(pts),
                color=BRANCH_COLORS[branch],
                marker=BRANCH_MARKERS[branch],
                s=14,
                alpha=SHADOW_ALPHA,
                linewidths=0,
                depthshade=False,
            )
    centroids: list[tuple[str, float, float, float]] = []
    for branch in BRANCHES:
        pts = by_branch.get(branch)
        if not pts:
            continue
        xs, ys, zs = ([p[k] for p in pts] for k in ("pc1", "pc2", "pc3"))
        ax.scatter(
            xs,
            ys,
            zs,
            color=BRANCH_COLORS[branch],
            marker=BRANCH_MARKERS[branch],
            s=28,
            alpha=0.75,
            edgecolors="#fcfcfb",
            linewidths=0.5,
            label=f"{branch} (n={len(pts)})",
        )
        centroids.append((branch, mean(xs), mean(ys), mean(zs)))
    _label_centroids(ax, centroids)
    ex = pca["explained"] or [0.0, 0.0, 0.0]
    ax.set_xlabel(f"PC1 ({100 * ex[0]:.0f}%)")
    ax.set_ylabel(f"PC2 ({100 * ex[1]:.0f}%)")
    ax.set_zlabel(f"PC3 ({100 * ex[2]:.0f}%)")
    _style_axes(ax)
    ax.view_init(elev=20, azim=-55)
    ax.set_title(title, color=INK, fontsize=11)
    ax.legend(fontsize=8, loc="upper left", frameon=False, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def behavior_figures(store: RunStore) -> list[str]:
    """Write both figures and their JSON data into <run>/analysis/. Returns the written paths."""
    cfg = ExperimentConfig.from_dict(store.load_json("config.json"))
    sessions = store.load_sessions("phase2/sessions.json")
    run = store.root.name
    (store.root / "analysis").mkdir(exist_ok=True)

    paths = mean_price_paths(cfg, sessions)
    store.save_json("analysis/behavior_price_paths.json", paths)
    f1 = str(store.path("analysis/price_paths_3d.png"))
    plot_price_paths_3d(paths, cfg.phase1.rounds, f"{run}: mean price path per branch (exploratory)", f1)

    pca = path_pca(cfg, sessions)
    store.save_json("analysis/behavior_pca.json", pca)
    f2 = str(store.path("analysis/price_path_pca_3d.png"))
    plot_path_pca_3d(pca, f"{run}: PCA of post-swap price paths, one point per session (exploratory)", f2)
    return [
        f1,
        f2,
        str(store.path("analysis/behavior_price_paths.json")),
        str(store.path("analysis/behavior_pca.json")),
    ]
