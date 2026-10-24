# Cartel Succession

Does LLM price collusion survive replacing an agent? Code for the study "Who Carries the Cartel?
LLM Price Collusion Survives Agent Replacement Through the Inherited Price History"
(AI Collusion Research Sprint, 23–25 Oct 2026; Track 1, question 1.2).

## Question

Two LLM pricing agents play a repeated logit Bertrand duopoly until prices are above the
competitive level. At round 100 one agent is replaced. The experiment measures whether the high
prices continue, and whether the model, the inherited price history or the inherited notes carry
them. A paired forced-cut audit tests whether the prices after the replacement are enforced or
only anchored. Background and design: `docs/RESEARCH_BRIEF.md`; prior work: `docs/RELATED_WORK.md`.

## Conditions

| Condition | Firm-2 price setter from round 100 | History seen | Entrant's notes |
|---|---|---|---|
| `control` | incumbent (no replacement) | all | kept |
| `placebo` | incumbent; firm 1 still gets the notice | all | kept |
| `same_inherit` | new instance of the same model | last 30 rounds | cleared |
| `same_blank` | new instance of the same model | none | cleared |
| `same_notes` | new instance of the same model | none | predecessor's |
| `other_inherit` | other model family | last 30 rounds | cleared |
| `other_blank` | other model family | none | cleared |
| `br_bot` | best response to firm 1's last price | firm 1's last price | – |

Seeds depend on the experiment seed, session, firm, round and retry count, never on the
condition, so the conditions of one session are paired.

## Quick start

```bash
pip install -r requirements.txt
python -m pytest -q                                    # mock backend, no GPU
python scripts/run_local.py --backend mock             # full pipeline with a mock model
python -m modal setup
modal run modal_app.py --config configs/pilot.yaml --stages aa,phase1,select,analyze
```

## Layout

```
succession/   experiment package: market, prompts, parsing, backends, session, branches,
              experiment stages, metrics, hypotheses, analysis, storage
modal_app.py  Modal app (GPU generator + CPU orchestrator)
configs/      main.yaml (pre-registered), main_*.yaml (runs 5-8), final_*.yaml (runs 9-12), pilot.yaml, local_4060.yaml
scripts/      run_local.py, analyze.py, pool.py, inspect_replies.py, plot_behavior.py
tests/        pytest suite (mock backend)
docs/         research brief, related work
```

## License

MIT. See `LICENSE`.
