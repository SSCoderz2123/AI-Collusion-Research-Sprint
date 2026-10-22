# Design notes

## Data flow

```
configs/*.yaml ──> ExperimentConfig
                        │
modal_app.main (your PC) ──> orchestrate (Modal CPU container)
                                  │  each round: one batch per model
                                  ├──> Generator[qwen7b]    (Modal L4, vLLM)
                                  └──> Generator[mistral7b] (Modal L4, vLLM)
                                  │
                                  └──> RunStore on Volume "succession-runs"/<run>/
                                         config.json
                                         aa/result.json, aa/sessions.json
                                         controls/sessions.json, controls/audit_*.json
                                         phase1/sessions.json, phase1/selection.json
                                         phase2/sessions.json
                                         deviation/audit_sessions.json, deviation/audit_events.json
                                         analysis/summary.md, *.json, *.png
```

## One round (`Engine.step`)

1. For every session and seat: a bot computes its price; an LLM seat gets a prompt.
2. Prompts are grouped by model. Each model gets one batched call. All models run in parallel.
3. Each reply is parsed. A failed parse gets a second attempt with a new seed. A second failure
   uses the agent's last price and is recorded as `parse_ok = false`.
4. A forced price (audit) replaces the decided price for that seat and round.
5. The market computes quantities and profits. The round is appended to the session.

## Pairing and determinism

The seed of a request is `derive_seed(experiment seed, root session, seat, round, attempt)`.
It does not depend on the branch. So when two branches show an agent the same prompt, vLLM
samples the same reply, and the branches differ only through the swap.

vLLM honours per-request seeds, but results can still vary with batch composition (floating-point
order). The A/A stage measures this: identical copies, same seeds, different batches. Tran & Yu
(2026) report 94–98% identical calls with vLLM. Report our value. Pairing reduces variance;
it does not create bias when it is imperfect.

## Why notes are cleared at a swap

A prompted LLM has no state outside its prompt: visible history plus its own notes. An entrant
with the same model, the same history and the same notes is the old agent. So every swap clears
notes, and the inherit/blank factor sets the visible history. The `placebo` branch separates the
effect of the notice from the effect of the swap.

## Audit

At the end of each branch (round 200), each session is copied twice per deviator seat. In the
"cut" copy the deviator's price for one round is 10% below its last price. Both copies play
6 more rounds with the same seeds. The rival's price change one round later, per unit of cut,
is compared with the change that a static best responder would make (0.29–0.44 per unit near
the Nash–monopoly range). Method: Tran & Yu (2026), arXiv 2610.28787.

## Known limits of the harness

- Two firms only (`n_firms` > 2 is not supported by the history format).
- One prompt wording. Prompt sensitivity is a limit to report.
- vLLM determinism is not exact across batch compositions (see above).
