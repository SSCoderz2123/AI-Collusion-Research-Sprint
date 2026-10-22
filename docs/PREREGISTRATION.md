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
Report the number kept. If fewer than 8 of 20 sessions pass, report this and run phase 2 on
the kept sessions anyway. Do not lower the threshold after seeing phase-1 data.

## Fixed parameters

See `configs/main.yaml`. Model ids, temperature 0.7, history window 30, max 160 output
tokens, swap seat 1, swap round 100, phase-2 length 100, audit cut 10%, horizon 6, discount 0.95.

## Metrics

| Metric | Definition |
|---|---|
| post-window difference | branch − control, profit index, rounds 150–199, per root; mean and 95% percentile bootstrap CI (10,000 resamples over roots) |
| dip depth | mean index over rounds 80–99 minus the lowest 3-round mean in rounds 100–119 |
| recovery half-life | rounds after the swap until the 5-round mean recovers half of the dip; "never" if not within 100 rounds |
| excess response | (rival price cut one round later / deviator cut) − best-response benchmark |
| deviator gain | discounted (0.95) profit difference, deviation copy − base copy, over 7 rounds, in Nash-profit units |
| parse-failure rate | share of LLM decisions without a valid price after 2 attempts |

## Controls

- A/A determinism: 4 sessions, fork at round 10, 10 more rounds; report the identical-decision fraction.
- Myopic prompt (placebo): agents value only the current period.
- Trigger prompt (positive control): instructed trigger strategy; the audit must show a positive excess response.
- `br_bot` entrant (negative control): static best response; no collusion expected.
- `placebo` branch: no swap, but the incumbent gets the swap notice.

## Deviations

| Date | Change | Reason |
|---|---|---|
| | | |
