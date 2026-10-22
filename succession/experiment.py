"""Experiment stages. Each stage reads and writes through a RunStore, so a
stage that stops (timeout, preemption) continues from its last checkpoint.

Stages, in order:
  aa         determinism check: two identical copies must give the same replies
  controls   prompt controls for the audit: default, myopic placebo, trigger positive control
  phase1     cartel formation: n_sessions x phase1.rounds
  select     apply the pre-registered inclusion rule to phase 1
  phase2     fork kept sessions into the branches and play phase2.rounds more
  deviation  forced-cut audit at the end of every phase-2 branch
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from statistics import mean

from succession.backends import Backend
from succession.branches import make_branch
from succession.config import ExperimentConfig
from succession.market import Market
from succession.metrics import enforcement_response, round_index, window_mean
from succession.session import AgentState, Engine, Session
from succession.store import RunStore

log = logging.getLogger("succession")

STAGES = ("aa", "controls", "phase1", "select", "phase2", "deviation")


def new_session(root_id: int, cfg: ExperimentConfig, branch: str, variant: str | None = None) -> Session:
    variant = variant or cfg.prompt_variant
    seats = [
        AgentState(kind="llm", model=cfg.incumbent_model.name, prompt_variant=variant, label="incumbent")
        for _ in range(cfg.market.n_firms)
    ]
    return Session(root_id=root_id, branch=branch, seats=seats)


def _run_checkpointed(engine: Engine, sessions: list[Session], until: int, store: RunStore, name: str) -> None:
    every = max(1, engine.cfg.checkpoint_every)

    def on_round(rnd: int) -> None:
        if rnd % every == 0:
            store.save_sessions(name, sessions)
            log.info("%s: round %d checkpoint saved", name, rnd)

    engine.run(sessions, until, on_round=on_round)
    store.save_sessions(name, sessions)


def _load_or(store: RunStore, name: str, make) -> list[Session]:
    if store.exists(name):
        log.info("resuming %s", name)
        return store.load_sessions(name)
    return make()


# ------------------------------------------------------------------- stages
def stage_aa(
    cfg: ExperimentConfig, backend: Backend, store: RunStore, n: int = 4, warmup: int = 10, span: int = 10
) -> dict:
    """Fork each session at `warmup`, play both copies `span` rounds, count identical prices."""
    engine = Engine(cfg, backend)
    sessions = [new_session(9000 + i, cfg, "aa") for i in range(n)]
    engine.run(sessions, warmup)
    copies = [s.fork(tag="copy") for s in sessions]
    engine.run(sessions + copies, warmup + span)
    same = total = 0
    for a, b in zip(sessions, copies, strict=True):
        for ra, rb in zip(a.records[warmup:], b.records[warmup:], strict=True):
            for pa, pb in zip(ra.prices, rb.prices, strict=True):
                total += 1
                same += abs(pa - pb) < 1e-9
    result = {"identical_fraction": same / total if total else None, "decisions": total}
    store.save_json("aa/result.json", result)
    store.save_sessions("aa/sessions.json", sessions + copies)
    return result


def stage_controls(cfg: ExperimentConfig, backend: Backend, store: RunStore) -> None:
    n_per_variant, rounds = cfg.controls.n_per_variant, cfg.controls.rounds
    engine = Engine(cfg, backend)
    name = "controls/sessions.json"

    def make():
        out = []
        for k, variant in enumerate(("default", "myopic", "trigger")):
            out += [new_session(5000 + 100 * k + i, cfg, f"ctrl_{variant}", variant) for i in range(n_per_variant)]
        return out

    sessions = _load_or(store, name, make)
    _run_checkpointed(engine, sessions, rounds, store, name)
    _audit(cfg, backend, store, sessions, "controls")


def stage_phase1(cfg: ExperimentConfig, backend: Backend, store: RunStore) -> None:
    engine = Engine(cfg, backend)
    name = "phase1/sessions.json"
    sessions = _load_or(store, name, lambda: [new_session(i, cfg, "phase1") for i in range(cfg.phase1.n_sessions)])
    _run_checkpointed(engine, sessions, cfg.phase1.rounds, store, name)


def stage_select(cfg: ExperimentConfig, store: RunStore) -> dict:
    """Apply the inclusion rule from docs/PREREGISTRATION.md. Do not change it after seeing data."""
    market = Market(cfg.market)
    sessions = store.load_sessions("phase1/sessions.json")
    rows = []
    for s in sessions:
        idx = round_index(market, s)
        value = window_mean(idx, cfg.phase1.select_from, cfg.phase1.rounds)
        rows.append({"root_id": s.root_id, "index": value, "kept": value > cfg.phase1.select_threshold})
    result = {
        "rule": (
            f"mean profit index over rounds [{cfg.phase1.select_from}, {cfg.phase1.rounds})"
            f" > {cfg.phase1.select_threshold}"
        ),
        "sessions": rows,
        "kept": [r["root_id"] for r in rows if r["kept"]],
    }
    store.save_json("phase1/selection.json", result)
    log.info("kept %d of %d sessions", len(result["kept"]), len(rows))
    return result


def stage_phase2(cfg: ExperimentConfig, backend: Backend, store: RunStore) -> None:
    engine = Engine(cfg, backend)
    name = "phase2/sessions.json"

    def make():
        kept = set(store.load_json("phase1/selection.json")["kept"])
        bases = [s for s in store.load_sessions("phase1/sessions.json") if s.root_id in kept]
        return [make_branch(b, br, cfg) for b in bases for br in cfg.phase2.branches]

    sessions = _load_or(store, name, make)
    if not sessions:
        log.warning("no session passed the inclusion rule; phase 2 has nothing to run")
        return
    _run_checkpointed(engine, sessions, cfg.phase1.rounds + cfg.phase2.rounds, store, name)


def stage_deviation(cfg: ExperimentConfig, backend: Backend, store: RunStore) -> None:
    if not cfg.deviation.enabled:
        return
    sessions = store.load_sessions("phase2/sessions.json")
    _audit(cfg, backend, store, sessions, "deviation")


def _audit(cfg: ExperimentConfig, backend: Backend, store: RunStore, sessions: list[Session], folder: str) -> None:
    """Paired forced-cut test (method of Tran & Yu 2026, arXiv 2610.28787)."""
    engine = Engine(cfg, backend)
    name = f"{folder}/audit_sessions.json"

    def make():
        out = []
        for s in sessions:
            dev_round = s.next_round
            for seat in cfg.deviation.deviator_seats:
                base = s.fork(tag=f"dev{seat}_base")
                dev = s.fork(tag=f"dev{seat}_cut")
                last = s.records[-1].prices[seat]
                dev.forced_prices[dev_round] = {seat: round(last * (1 - cfg.deviation.cut), 4)}
                out += [base, dev]
        return out

    copies = _load_or(store, name, make)
    if not copies:
        return
    # The deviation round is stored in the "_cut" copy; its "_base" partner uses the same round.
    # Deriving it from stored data (not from next_round) keeps targets correct after a resume.
    by_key = {c.key: c for c in copies}

    def dev_round_of(c: Session) -> int:
        cut = c if c.forced_prices else by_key[c.key.replace("_base", "_cut")]
        return min(cut.forced_prices)

    targets = {c.key: dev_round_of(c) + 1 + cfg.deviation.horizon for c in copies}
    while True:
        active = [c for c in copies if c.next_round < targets[c.key]]
        if not active:
            break
        engine.step(active)
        store.save_sessions(name, copies)  # audit runs only ~7 rounds: checkpoint every round
    store.save_sessions(name, copies)

    events = []
    for c in copies:
        if not c.tag.endswith("_cut"):
            continue
        seat = int(c.tag[3])
        base = by_key[c.key.replace("_cut", "_base")]
        dev_round = min(c.forced_prices)
        res = enforcement_response(engine.market, base, c, seat, dev_round, cfg.deviation.discount)
        res.update(
            {
                "branch": c.branch,
                "root_id": c.root_id,
                "deviator": seat,
                "dev_round": dev_round,
                # Seat in the label: in control/placebo both seats are incumbents, and seat 1
                # there is the paired counterpart of the entrant in the swap branches.
                "deviator_label": f"seat{seat}:{c.seats[seat].label}",
            }
        )
        events.append(res)
    store.save_json(f"{folder}/audit_events.json", events)
    valid = [e["excess_response"] for e in events if "excess_response" in e]
    log.info(
        "%s audit: %d events, mean excess response %.3f", folder, len(events), mean(valid) if valid else float("nan")
    )


def check_config(cfg: ExperimentConfig, store: RunStore) -> None:
    """Save the config on first use. Refuse a different config for an existing run,
    because resumed stages would mix data from two designs."""
    current = json.loads(json.dumps(cfg.to_dict()))
    if store.exists("config.json"):
        # Fill fields that did not exist when the run started with their defaults, so a field
        # added later (at its default value) does not count as a design change.
        saved = json.loads(json.dumps(ExperimentConfig.from_dict(store.load_json("config.json")).to_dict()))
        if saved != current:
            changed = sorted(k for k in set(saved) | set(current) if saved.get(k) != current.get(k))
            raise ValueError(
                f"run folder {store.root} was made with a different config (changed: {changed}). "
                "Use a new run name, or delete the run folder."
            )
    else:
        store.save_json("config.json", current)


def run_stages(cfg: ExperimentConfig, backend: Backend, store: RunStore, stages: list[str]) -> None:
    check_config(cfg, store)
    for stage in stages:
        log.info("=== stage %s ===", stage)
        started = time.monotonic()
        started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        _run_one(cfg, backend, store, stage)
        _record_timing(store, stage, started_at, time.monotonic() - started)


def _record_timing(store: RunStore, stage: str, started_at: str, seconds: float) -> None:
    """Append one row to timings.json. A resumed stage adds a second row; both are kept."""
    rows = store.load_json("timings.json") if store.exists("timings.json") else []
    rows.append({"stage": stage, "started_utc": started_at, "seconds": round(seconds, 1)})
    store.save_json("timings.json", rows)
    log.info("stage %s finished in %.1f s", stage, seconds)


def _run_one(cfg: ExperimentConfig, backend: Backend, store: RunStore, stage: str) -> None:
    if stage == "aa":
        log.info("A/A result: %s", stage_aa(cfg, backend, store))
    elif stage == "controls":
        stage_controls(cfg, backend, store)
    elif stage == "phase1":
        stage_phase1(cfg, backend, store)
    elif stage == "select":
        stage_select(cfg, store)
    elif stage == "phase2":
        stage_phase2(cfg, backend, store)
    elif stage == "deviation":
        stage_deviation(cfg, backend, store)
    else:
        raise ValueError(f"unknown stage {stage}; valid: {STAGES}")
