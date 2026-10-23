# Cartel Succession

Does LLM price collusion survive replacing an agent?
Apart Research AI Collusion Research Sprint, 23–25 Oct 2026. Track 1 (Markets and Collusion), question 1.2.

> **Preexisting work:** the experiment harness in this repository was written on 22 Oct 2026,
> before the sprint start, with Claude Code. Before the sprint only a pilot setup test ran
> (`docs/RUN_LOG.md`).
> See `docs/PREEXISTING_WORK.md` and `docs/AI_USE.md`.

## Question

Two LLM pricing agents play a repeated pricing game until prices are above the competitive
level. At round 100 one agent is replaced. We measure whether the high prices come back, and
whether the model or the inherited price history carries them. A paired forced-cut audit tests
whether the prices after the swap are enforced or only anchored.

## Design

| Branch | Entrant | Entrant sees |
|---|---|---|
| control | none | – |
| placebo | none (incumbent gets the swap notice) | – |
| same_inherit / same_blank | same model, new instance | full history / rounds from the swap |
| other_inherit / other_blank | other model family | full history / rounds from the swap |
| br_bot | static best-response bot | last rival price |

Market: logit Bertrand duopoly (Nash 1.473, monopoly 1.925). Models: Qwen2.5-7B-Instruct and
Mistral-7B-Instruct-v0.3 on vLLM. Seeds do not depend on the branch, so branches of one session
are paired. Details: `docs/RESEARCH_BRIEF.md`, `docs/PREREGISTRATION.md`, `docs/DESIGN.md`.

## Quick start

```bash
pip install -r requirements.txt
python -m pytest -q                                    # 71 tests, no GPU
python scripts/run_local.py --backend mock             # full pipeline with a mock model
python -m modal setup
modal run modal_app.py --config configs/pilot.yaml --stages aa,phase1,select,analyze
```

Full Modal guide, with cost estimates: `docs/RUNNING_ON_MODAL.md`.

## Repository layout

```
succession/   experiment package: market, prompts, parsing, backends, session, branches,
              experiment stages, metrics, analysis, storage
modal_app.py  Modal app (GPU Generator + CPU orchestrator)
configs/      main.yaml (pre-registered), main_*.yaml (runs 5-8), final_*.yaml (runs 9-12), pilot.yaml, local_4060.yaml
scripts/      run_local.py, analyze.py, pool.py, inspect_replies.py, plot_behavior.py
tests/        pytest suite (mock backend)
docs/         brief, pre-registration, design, Modal guide, related work, disclosures
paper/        report outline
CLAUDE.md     instructions for AI assistants; rules in .claude/rules/
```

## License

MIT. See `LICENSE`.
