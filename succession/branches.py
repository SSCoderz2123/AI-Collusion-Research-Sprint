"""Phase-2 branches: what happens to the replaced seat at the swap round.

| branch        | entrant at swap_seat                     | history the entrant sees | notes   |
|---------------|------------------------------------------|--------------------------|---------|
| control       | no swap                                  | -                        | -       |
| placebo       | no swap; incumbent gets the swap notice  | -                        | -       |
| same_inherit  | incumbent model, new instance            | full history             | cleared |
| same_blank    | incumbent model, new instance            | rounds from swap only    | cleared |
| other_inherit | other model family                       | full history             | cleared |
| other_blank   | other model family                       | rounds from swap only    | cleared |
| br_bot        | static best-response bot (negative ctrl) | last rival price         | -       |

A prompted LLM agent has no state outside its prompt. Its state is the
visible history plus its notes. So "same model, same history, same notes"
is identical to no swap. The swap branches therefore always clear notes, and
"inherit" vs "blank" sets which part of the history the entrant can see.

When announce is true, the incumbent gets the same notice in placebo and in
every swap branch, so placebo isolates the effect of the notice.
"""

from __future__ import annotations

from succession.config import ExperimentConfig
from succession.prompts import swap_notice
from succession.session import AgentState, Session

BRANCHES = ("control", "placebo", "same_inherit", "same_blank", "other_inherit", "other_blank", "br_bot")


def make_branch(base: Session, branch: str, cfg: ExperimentConfig) -> Session:
    if branch not in BRANCHES:
        raise ValueError(f"unknown branch: {branch}")
    s = base.fork(branch=branch)
    swap_round = base.next_round
    seat = cfg.phase2.swap_seat
    incumbent = 1 - seat
    s.swap_round = swap_round

    if branch == "control":
        return s
    if cfg.phase2.announce:
        s.seats[incumbent].notice = swap_notice(swap_round)
    if branch == "placebo":
        return s

    if branch == "br_bot":
        s.seats[seat] = AgentState(kind="br_bot", model=None, label="entrant", history_start=swap_round)
        return s

    model = cfg.incumbent_model.name if branch.startswith("same") else cfg.other_model.name
    history_start = 0 if branch.endswith("inherit") else swap_round
    s.seats[seat] = AgentState(
        kind="llm",
        model=model,
        prompt_variant=base.seats[seat].prompt_variant,
        history_start=history_start,
        notes="",
        label="entrant",
    )
    return s
