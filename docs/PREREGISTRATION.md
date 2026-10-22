# Pre-registration

Status: **draft, fixed when phase 1 of the main run starts.** Record that date here: `____`.
After that date, record every change under "Deviations".

## Hypotheses

Profit index = (profit − Nash profit) / (monopoly profit − Nash profit), mean of both firms.
"Post window" = rounds 150–199 (second half of phase 2). All differences are paired:
branch minus control, per root session.

- **H1 (history carries the cartel).** `same_inherit` − control > −0.10 in the post window.
- **H2 (blank entrant breaks it).** `same_blank` − control < −0.10 in the post window.
- **H3 (history beats model).** (`same_inherit` − `same_blank`) > 0 and
  (`other_inherit` − `other_blank`) > 0.
- **H4 (model identity matters less than history).** |`same_inherit` − `other_inherit`| <
  |`same_inherit` − `same_blank`|.
- **H5 (no enforcement).** In the audit, the excess response of the incumbent and of the
  entrant is not above 0 (95% CI includes 0 or is below it) in every LLM branch. This follows
  Tran & Yu (2026), who found that prompted open models seldom punish.

A hypothesis is supported when the 95% bootstrap CI of the stated difference is entirely on
the stated side of the threshold. Otherwise it is "not supported". If the CI includes the
threshold, the result is "inconclusive".

## Inclusion rule (phase 1)

Keep a root session when its mean profit index over rounds 50–99 is > 0.3.
Report the number kept. If fewer than 12 of 30 sessions pass, report this and run phase 2 on
the kept sessions anyway. Do not lower the threshold after seeing phase-1 data.

## Fixed parameters

See `configs/main.yaml`. Model ids, temperature 0.7, history window 30, max 160 output
tokens, swap seat 1, swap round 100, phase-2 length 100, audit cut 10%, horizon 6, discount 0.95.

## Metrics

| Metric | Definition |
|---|---|
| post-window difference | branch − control, profit index, rounds 150–199, per root; mean and 95% percentile bootstrap CI (10,000 resamples over roots) |
| dip depth | mean index over rounds 80–99 minus the lowest 3-round mean in rounds 100–119 |
| recovery half-life | rounds after the swap until the 5-round mean recovers half of the dip; 0 if the dip is < 0.05; "never" if not within 100 rounds |
| post-window price index | mean price index (0 = Nash price, 1 = monopoly price), rounds 150–199; secondary, reported next to the profit index because prices above the monopoly price give a negative profit index |
| excess response | (rival price cut one round later / deviator cut) − best-response benchmark |
| deviator gain | discounted (0.95) profit difference, deviation copy − base copy, over 7 rounds, in Nash-profit units |
| parse-failure rate | share of LLM decisions without a valid price after 2 attempts |

## Controls

- A/A determinism: 4 sessions, fork at round 10, 10 more rounds; report the identical-decision fraction.
- Prompt controls: 10 sessions per variant (default, myopic, trigger), 60 rounds, then the audit.
- Myopic prompt (placebo): agents value only the current period.
- Trigger prompt (positive control): instructed trigger strategy; the audit must show a positive excess response.
- `br_bot` entrant (negative control): static best response; no collusion expected.
- `placebo` branch: no swap, but the incumbent gets the swap notice.

## Secondary analysis: model replication

`configs/main_mistral.yaml` repeats the full design with Mistral-7B as the incumbent and
Qwen2.5-7B as the other family. H1–H5 are tested on it with the same rules and reported
separately as a replication. It does not replace the primary analysis (`configs/main.yaml`).

## Changes before the main run (22 Oct 2026, after the pilot)

These changes were made before phase 1 of the main run, based on the pilot (`docs/RUN_LOG.md`):

| Change | Reason |
|---|---|
| Phase-1 sessions 20 → 30 (threshold for "too few kept": 8 of 20 → 12 of 30) | Pilot kept 3 of 4; more roots give tighter paired CIs at low cost |
| Half-life: dip < 0.05 counts as no dip | Pilot control (no swap) reported "never recovered" for a 0.01 drift |
| Price index added as a secondary outcome | A pilot session priced at 2.49 (above monopoly) had profit index −0.52 |
| Prompt controls: 4 → 10 sessions per variant | Pilot trigger positive control had wide CIs with 4 sessions |
| Mistral-incumbent replication added | Tests whether the result depends on one model family |

## Deviations

| Date | Change | Reason |
|---|---|---|
| | | |
