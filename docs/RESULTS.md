# Results summary (all runs)

Every number below comes from a verbatim run summary in `docs/RUN_LOG.md`, which comes from
`scripts/analyze.py` or `scripts/pool.py` on the stored run data (`results/<run>/analysis/`).
Values are estimate [95% bootstrap CI]. "Profit index" and "price index" are 0 at the Nash outcome
and 1 at the monopoly outcome. All differences are paired per root session, branch − control, in
the post window (rounds 150–199).

All runs are logged. Run 9 (`final_main`) is the pre-registered primary final result.

## 1. Runs

| Run | Name | Incumbent | Entrant family | Kept / phase-1 sessions | Role | Status |
|---|---|---|---|---|---|---|
| 1–3 | pilot | Qwen-7B | Mistral-7B | 3 / 4 | setup check | pre-sprint |
| 4 | `main` | Qwen-7B | Mistral-7B | 16 / 30 | primary (pre-registered) | pre-sprint run |
| 5 | `main_mistral` | Mistral-7B | Qwen-7B | 15 / 30 | replication | control cartel collapses: no succession test |
| 6 | `main_r2` | Qwen-7B | Mistral-7B | 22 / 30 | primary sprint result | done |
| 7 | `main_olmo` | Qwen-7B | OLMo-2-7B | 25 / 30 | H6 with OLMo-2 | done |
| 8 | `main_noannounce` | Qwen-7B | Mistral-7B | 24 / 30 | H7 (no swap notice) | done |
| 9 | `final_main` | Qwen-7B | Mistral-7B | 29 / 40 | primary final result | done |
| 10 | `final_olmo` | Qwen-7B | OLMo-2-7B | 31 / 40 | H8 (OLMo-2 replication) | done |
| 11 | `final_granite` | Qwen-7B | Granite-3.1-8B | – | H6 with a third family | failed in phase 2 (GPU call timeout) |
| 12 | `final_qwen14b` | Qwen-14B | Mistral-7B | 19 / 40 | scale check | control cartel collapses: no succession test |

A/A determinism was 1.0 in every run except run 9 (0.8125; phase-2 pairing there uses request de-duplication). Parse failures were at most 1.0% per session in every run except run 5 (up to 6.0%).

## 2. Main result: the price history carries the cartel (Qwen-7B incumbent)

| Test | Run 4 | Run 6 | Run 7 | Run 8 | Run 9 (primary final) | Run 10 |
|---|---|---|---|---|---|---|
| H1: same model + full history (`same_inherit` − control) | −0.003 [−0.065, 0.064] | 0.016 [−0.077, 0.122] | 0.213 [0.006, 0.529] | 0.002 [−0.014, 0.016] | −0.025 [−0.051, −0.001] | −0.014 [−0.038, 0.008] |
| H2: same model + no history (`same_blank` − control) | −0.670 [−0.998, −0.360] | −0.474 [−0.782, −0.202] | −0.624 [−1.021, −0.215] | −0.504 [−0.850, −0.208] | −0.611 [−0.856, −0.380] | −0.480 [−0.689, −0.292] |
| H3a: `same_inherit` − `same_blank` | 0.667 [0.368, 0.989] | 0.489 [0.247, 0.771] | 0.836 [0.553, 1.164] | 0.505 [0.209, 0.853] | 0.587 [0.349, 0.838] | 0.467 [0.279, 0.676] |
| `same_blank` price index − control | 0.492 [0.162, 0.834] | 0.582 [0.292, 0.888] | 0.406 [−0.055, 0.878] | 0.337 [0.036, 0.663] | 0.481 [0.223, 0.746] | 0.420 [0.163, 0.686] |

- H1, H2 and H3a are supported in all 6 runs. In run 9 the H1 CI is entirely above the −0.10 margin
  and also below 0: the inherited cartel is 0.025 lower than control, a small but non-zero drop.
- The blank entrant lowers profit because it prices above the monopoly price, not because
  competition returns. The price-index estimate is above 0 in 6 of 6 runs, and the CI is entirely
  above 0 in 5 of 6.
- Pooled: runs 4 + 6 (n = 38): H1 0.008 [−0.051, 0.077]. Runs 4 + 6 + 7, branches without the other
  model (n = 63, exploratory): H1 0.089 [−0.004, 0.222], H2 −0.583 [−0.789, −0.376], H3a 0.672
  [0.502, 0.856].
- H7 (no swap notice needed, run 8): 0.002 [−0.014, 0.016], supported. The placebo branch had the
  same design as control in run 8: −0.001 [−0.022, 0.015].
- H9 (the predecessor's notes alone carry part of the cartel), `same_notes` − `same_blank`:
  run 9 (primary test) 0.342 [0.054, 0.634], **supported**; run 10 −0.048 [−0.439, 0.312], inconclusive.
  In both runs the notes-only entrant still ends below control (run 9: −0.270 [−0.448, −0.115]) and
  overprices (price index − control: run 9 +0.296 [0.076, 0.548], run 10 +0.747 [0.281, 1.350]).
  The notes keep part of the cartel; the history keeps all of it.

## 3. The entrant's family decides what happens to the inherited prices

| Run | Entrant | `other_inherit` − control (profit index) | Price index − control | Entrant holds its last price |
|---|---|---|---|---|
| 4 | Mistral-7B | −0.552 [−0.763, −0.362] | −0.677 [−0.874, −0.500] | 23.8% of rounds |
| 6 | Mistral-7B | −0.595 [−0.824, −0.357] | −0.657 [−0.776, −0.527] | 25.5% |
| 8 | Mistral-7B | −0.778 [−0.947, −0.596] | −0.779 [−0.862, −0.691] | 21.6% |
| 9 | Mistral-7B | −0.701 [−0.844, −0.558] | −0.666 [−0.755, −0.569] | 24.0% |
| 7 | OLMo-2-7B | 0.194 [−0.057, 0.534] | 0.270 [0.097, 0.500] | 96.8% |
| 10 | OLMo-2-7B | −0.024 [−0.077, 0.019] | 0.034 [−0.014, 0.078] | 96.3% |

- H6 (a different family breaks the cartel): supported with Mistral (runs 4, 6, 8, 9). Not supported
  with OLMo-2 (runs 7, 10).
- H8 (the OLMo-2 result replicates, run 10): supported.
- The OLMo-2 entrant keeps one constant price. Its notes say "maintain" and "consistency", and
  they do not mention the rival (18 sampled replies, run 7). The Mistral entrant changes its price
  in about 3 of 4 rounds. "Holds its last price" comes from the exploratory price-dynamics table.
  The Qwen-7B controls hold their price in 87.7–90.7% of rounds.

## 4. Enforcement audit: no punishment beyond price-matching

| Run | H5 (cells with excess response CI > 0) | H5c (cells above the myopic control) | Audit check: trigger − myopic |
|---|---|---|---|
| 4 | 2 of 13 | 4 of 13 (exploratory) | 1.316 [0.782, 1.815] |
| 6 | 0 of 13 | 0 of 13 (exploratory) | 0.638 [0.069, 1.220] |
| 7 | 3 of 13 | 0 of 13 (exploratory) | 0.760 [0.172, 1.322] |
| 8 | 1 of 13 | 0 of 13 (exploratory) | 1.044 [0.507, 1.554] |
| 9 (primary final) | 2 of 15 | **1 of 15**: `same_notes`, entrant cuts, 0.317 [0.128, 0.496] | 0.361 [0.017, 0.703] |
| 10 | 3 of 15 | 0 of 15 | 0.269 [−0.061, 0.598]: **check fails, H5 and H5c not interpretable** |
| 12 | 0 of 15 | 12 of 15 (myopic control far below best response) | 0.884 [0.591, 1.176] |

- Instructed trigger agents punish fully or not at all; 40–70% of trigger sessions punished in runs
  4 and 6–8. In run 9 about 11 of 29 and 10 of 30 punished; in run 10 about 12 and 7 of 30.
- H5c (primary test, run 9) is not supported: 1 of 15 cells responds above the myopic control. The
  responder in that cell is the Qwen incumbent, and the cut comes from the notes-only entrant.
  In runs 4–10, every H5 cell with a CI above 0 (11 cells) has deviator seat 1, and in each of them
  seat 1 is the entrant (exploratory observation): the incumbent reacts more strongly to a cut by a
  new firm than to a cut by its old partner.
- The myopic control (agents told to value only the current period) has a positive excess response
  in runs 6–8. Agents follow a price cut more than a best response would, without punishment.

## 5. When there is no cartel to inherit

| Run | Incumbent | Control profit index, before → after swap round | Interpretation |
|---|---|---|---|
| 5 | Mistral-7B | 0.594 → −0.710 | The incumbent pair does not keep a cartel; succession cannot be tested |
| 12 | Qwen-14B | 0.423 → −0.434 | The same. Qwen-14B holds its last price in 10.2% and 9.2% of rounds |

## 6. Method notes

- Runs 4–8: paired branches agreed in only 46.0–47.9% of decisions when the design was identical
  (run 8 placebo vs control), because one different decision changes all later prompts. The mean
  effect stayed ≈ 0. Runs 9–12 generate identical requests once (`dedupe_requests`).
- Pre-sprint: runs 1–5. Runs 6–8 started 03:25 UTC on 23 Oct; check this against the official
  kickoff time (`docs/PREEXISTING_WORK.md`).
- Exploratory (defined after runs 4–8 were seen): H5c on runs 4–8, decision agreement, price
  dynamics, `pool.py --shared`.
