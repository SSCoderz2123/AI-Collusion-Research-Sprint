"""Session state and the batched round engine.

A session is one market with two seats. Every seat holds an AgentState.
Copying a session (fork) copies all state, so branches start from the same
round-100 market. Sampling seeds depend only on (experiment seed, root
session, seat, round, attempt), never on the branch, so two branches that
show an agent the same prompt get the same reply.
"""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass, field

from succession.backends import Backend, derive_seed
from succession.config import ExperimentConfig
from succession.market import Market
from succession.parsing import parse_reply
from succession.prompts import HistoryRow, build_prompt


@dataclass
class AgentState:
    kind: str  # "llm" or "br_bot"
    model: str | None  # model name for kind "llm"
    prompt_variant: str = "default"
    history_start: int = 0  # first round this agent can see
    notes: str = ""
    notice: str | None = None
    label: str = "incumbent"  # "incumbent" or "entrant"


@dataclass
class RoundRecord:
    round: int
    prices: list[float]
    quantities: list[float]
    profits: list[float]
    notes: list[str]
    replies: list[str]
    parse_ok: list[bool]
    agents: list[str]  # "label:model" for each seat
    forced: list[bool]


@dataclass
class Session:
    root_id: int
    branch: str
    seats: list[AgentState]
    records: list[RoundRecord] = field(default_factory=list)
    tag: str = ""  # extra key for deviation copies, e.g. "dev0_base"
    swap_round: int | None = None
    forced_prices: dict[int, dict[int, float]] = field(default_factory=dict)  # round -> seat -> price

    @property
    def key(self) -> str:
        return f"{self.branch}/{self.root_id}" + (f"/{self.tag}" if self.tag else "")

    @property
    def next_round(self) -> int:
        return len(self.records)

    def fork(self, branch: str | None = None, tag: str | None = None) -> Session:
        new = copy.deepcopy(self)
        if branch is not None:
            new.branch = branch
        if tag is not None:
            new.tag = tag
        return new

    def to_dict(self) -> dict:
        d = asdict(self)
        d["forced_prices"] = {str(r): {str(s): p for s, p in v.items()} for r, v in self.forced_prices.items()}
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Session:
        return cls(
            root_id=d["root_id"],
            branch=d["branch"],
            seats=[AgentState(**s) for s in d["seats"]],
            records=[RoundRecord(**r) for r in d["records"]],
            tag=d.get("tag", ""),
            swap_round=d.get("swap_round"),
            forced_prices={int(r): {int(s): p for s, p in v.items()} for r, v in d.get("forced_prices", {}).items()},
        )


def visible_history(session: Session, seat: int, window: int) -> list[HistoryRow]:
    agent = session.seats[seat]
    rows = [r for r in session.records if r.round >= agent.history_start]
    rows = rows[-window:] if window > 0 else []
    rival = 1 - seat
    return [
        HistoryRow(
            round=r.round,
            own_price=r.prices[seat],
            rival_price=r.prices[rival],
            own_quantity=r.quantities[seat],
            own_profit=r.profits[seat],
        )
        for r in rows
    ]


def trigger_prices(market: Market) -> tuple[float, float, float]:
    """(high, threshold, low) for the instructed trigger-strategy control."""
    high, low = market.monopoly_price, market.nash_price
    return high, high - 0.25 * (high - low), low


class Engine:
    def __init__(self, cfg: ExperimentConfig, backend: Backend, dedupe: bool | None = None) -> None:
        self.cfg = cfg
        self.backend = backend
        self.market = Market(cfg.market)
        # The A/A stage passes dedupe=False: it must test the backend itself.
        self.dedupe = cfg.dedupe_requests if dedupe is None else dedupe

    def _prompt(self, session: Session, seat: int) -> str:
        agent = session.seats[seat]
        return build_prompt(
            variant=agent.prompt_variant,
            cost=self.cfg.market.cost,
            history=visible_history(session, seat, self.cfg.history_window),
            notes=agent.notes,
            current_round=session.next_round,
            notice=agent.notice,
            trigger_prices=trigger_prices(self.market) if agent.prompt_variant == "trigger" else None,
        )

    def _fallback_price(self, session: Session, seat: int) -> float:
        own = [r.prices[seat] for r in session.records if r.round >= session.seats[seat].history_start]
        return own[-1] if own else self.market.nash_price

    def step(self, sessions: list[Session]) -> None:
        """Play one round in every session. Sessions may be at different rounds."""
        decisions: dict[tuple[int, int], tuple[float, str, str, bool]] = {}
        pending: list[tuple[int, int]] = []

        for i, s in enumerate(sessions):
            for seat, agent in enumerate(s.seats):
                if agent.kind == "br_bot":
                    last = s.records[-1].prices[1 - seat] if s.records else self.market.nash_price
                    decisions[(i, seat)] = (self.market.best_response([last]), "", "", True)
                else:
                    pending.append((i, seat))

        # Up to two attempts per LLM seat. The second attempt uses a new seed.
        for attempt in range(2):
            if not pending:
                break
            batches: dict[str, tuple[list[str], list[int]]] = {}
            order: dict[str, list[tuple[tuple[int, int], int]]] = {}  # model -> ((session, seat), batch slot)
            slots: dict[str, dict[tuple[str, int], int]] = {}
            for i, seat in pending:
                s = sessions[i]
                model = s.seats[seat].model
                prompts, seeds = batches.setdefault(model, ([], []))
                prompt = self._prompt(s, seat)
                seed = derive_seed(self.cfg.seed, s.root_id, seat, s.next_round, attempt)
                known = slots.setdefault(model, {})
                if self.dedupe and (prompt, seed) in known:
                    slot = known[(prompt, seed)]
                else:
                    slot = len(prompts)
                    prompts.append(prompt)
                    seeds.append(seed)
                    known[(prompt, seed)] = slot
                order.setdefault(model, []).append(((i, seat), slot))
            replies = self.backend.generate_batches(batches)
            still: list[tuple[int, int]] = []
            for model, items in order.items():
                texts = replies[model]
                if len(texts) != len(batches[model][0]):
                    raise RuntimeError(f"backend returned {len(texts)} replies for {len(batches[model][0])} prompts")
                for (i, seat), slot in items:
                    text = texts[slot]
                    parsed = parse_reply(text, self.cfg.price_min, self.cfg.price_max)
                    if parsed.ok:
                        decisions[(i, seat)] = (parsed.price, parsed.notes, text, True)
                    elif attempt == 1:
                        s = sessions[i]
                        decisions[(i, seat)] = (self._fallback_price(s, seat), s.seats[seat].notes, text, False)
                    else:
                        still.append((i, seat))
            pending = still

        for i, s in enumerate(sessions):
            rnd = s.next_round
            forced = s.forced_prices.get(rnd, {})
            prices, notes, replies, oks, flags = [], [], [], [], []
            for seat in range(len(s.seats)):
                price, note, reply, ok = decisions[(i, seat)]
                if seat in forced:
                    price = forced[seat]
                prices.append(price)
                notes.append(note)
                replies.append(reply)
                oks.append(ok)
                flags.append(seat in forced)
            quantities = self.market.quantities(prices)
            profits = self.market.profits(prices)
            for seat, agent in enumerate(s.seats):
                if agent.kind == "llm" and oks[seat]:
                    agent.notes = notes[seat]
            s.records.append(
                RoundRecord(
                    round=rnd,
                    prices=prices,
                    quantities=quantities,
                    profits=profits,
                    notes=notes,
                    replies=replies,
                    parse_ok=oks,
                    agents=[f"{a.label}:{a.model or a.kind}" for a in s.seats],
                    forced=flags,
                )
            )

    def run(self, sessions: list[Session], until_round: int, on_round=None) -> None:
        """Step all sessions until each one has played until_round rounds."""
        while True:
            active = [s for s in sessions if s.next_round < until_round]
            if not active:
                return
            self.step(active)
            if on_round is not None:
                on_round(min(s.next_round for s in sessions))
