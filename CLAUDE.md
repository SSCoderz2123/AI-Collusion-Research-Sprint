# CLAUDE.md

Guidance for Claude Code (and any other AI assistant) in this repository.

## Project

Apart Research AI Collusion Research Sprint, 23–25 Oct 2026. Track 1, question 1.2.
Research question: after two LLM pricing agents form a cartel, one agent is replaced.
Does collusion come back, and is it carried by the agent or by the price history the
entrant inherits? Full brief: `docs/RESEARCH_BRIEF.md`. Fixed design: `docs/PREREGISTRATION.md`.

## Layout

```
succession/          experiment package (pure Python, no GPU import at module level)
  market.py          logit Bertrand duopoly, Nash/monopoly benchmarks, best response
  prompts.py         prompt text and variants (default, myopic, trigger)
  parsing.py         reply -> (price, notes)
  backends.py        MockBackend, VLLMEngine, LocalVLLMBackend, ModalBackend, derive_seed
  session.py         AgentState, RoundRecord, Session (fork/serialise), Engine (batched rounds)
  branches.py        phase-2 swap branches
  experiment.py      stages: aa, controls, phase1, select, phase2, deviation (checkpointed)
  metrics.py         profit index, paired differences, bootstrap CI, dip, half-life, audit
  analysis.py        tables (JSON/Markdown) and figures (PNG)
  store.py           RunStore: atomic JSON writes, Modal Volume commit hook
modal_app.py         Modal app: Generator (GPU, vLLM) + orchestrate (CPU loop)
configs/             main.yaml (pre-registered), main_*.yaml (runs 5-8), final_*.yaml (runs 9-12), pilot, local_4060
scripts/             run_local.py (mock or local vLLM), analyze.py, pool.py, inspect_replies.py
tests/               pytest suite; runs with the mock backend, no GPU
docs/                brief, pre-registration, design, Modal guide, related work, disclosures
paper/               report outline only; the authors write the report text
results/             run data (git-ignored except .gitkeep)
```

## Commands

```bash
pip install -r requirements.txt
python -m pytest -q                                   # must pass before every commit
ruff check . && ruff format --check .                 # must be clean
python scripts/run_local.py --backend mock            # full pipeline, no GPU
modal run modal_app.py --config configs/pilot.yaml --stages aa,phase1,select,analyze
```

## Rules

Read and follow these files. They are part of this instruction file.

@.claude/rules/research-integrity.md
@.claude/rules/code.md
@.claude/rules/writing.md

## Invariants that code changes must keep

- `derive_seed` takes (experiment seed, root session, seat, round, attempt). It must never
  take the branch name. Paired branch comparisons depend on this.
- The default prompt never mentions collusion, cartels, coordination, punishment or cooperation.
  `tests/test_parsing_prompts.py::test_default_prompt_is_neutral` checks this.
- A swap branch clears the entrant's notes. "Same model + same history + same notes" equals no swap.
  Only exception: `same_notes` keeps the notes and hides all history (H9).
- With `dedupe_requests: true`, identical requests in one round are generated once. The `aa` stage
  must keep `dedupe=False`, or the A/A check becomes identical by construction.
- Every stage must resume from its checkpoint and give the same result as an uninterrupted run
  (`tests/test_pipeline.py::test_resume_gives_same_result`).
- `succession/` must import without vLLM or Modal installed. Import them inside functions.
