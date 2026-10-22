# Run log

One entry per Modal run. Numbers come from the run output or from `results/<run>/analysis/`.
Do not type a number that is not in one of those sources.

## Status

| Check | Status |
|---|---|
| Modal account, payment method, credit | Done (22 Oct) |
| GPU image builds (vLLM 0.8.5, transformers 4.51.3) | Pass (22 Oct, run 2) |
| Qwen2.5-7B Generator starts on L4 | Pass |
| A/A determinism (pilot) | Pass: identical_fraction 1.0 |
| Pilot inclusion rule | Pass: 3 of 4 sessions kept (pass condition ≥ 2) |
| Mistral-7B Generator + `huggingface` secret | Pass (run 3) |
| Stages controls, phase2, deviation on GPU | Pass (run 3) |
| Pilot parse failures | Pass: 0.000 in phase 1; ≤ 0.004 in phase 2 (required < 5%) |
| Main run (`main`, `main_mistral`) | Not started |

## Run 1: pilot, 22 Oct 2026 (failed)

- App: `cartel-succession`. Config: `configs/pilot.yaml`. Run name: `pilot`.
- First try: stopped by Modal: "Please add a payment method to use L4 GPU functions." Fixed by
  adding a payment method.
- Second try: every Generator start failed with
  `AttributeError: Qwen2Tokenizer has no attribute all_special_tokens_extended`.
  Cause: unpinned `transformers` (vLLM 0.8.5 declares only a lower bound). Fixed in PR #2
  (pin `transformers==4.51.3`, 30-minute fail-fast on GPU calls).

## Run 2: pilot, 22 Oct 2026 (pass)

- Modal app run: `ap-5J7FVa5v5LA4ERoyt96eSQ`. GPU: L4. Stages: `aa,phase1,select,analyze`.
- Pre-sprint setup test: the sprint starts 23 Oct. These results do not go into the report as
  findings (see `docs/PREEXISTING_WORK.md`).

### Timeline (UTC, from the run output)

| Time | Event |
|---|---|
| 14:32:39 | stage `aa` starts; Generator (Qwen2.5-7B-Instruct) container starts |
| 14:33:13 | vLLM V0 engine initialises (v0.8.5, bfloat16, max_seq_len 4096, prefix caching on) |
| 14:34:42 | weights downloaded: 84.8 s |
| 14:34:48 | model loaded: 14.25 GiB, 91.3 s in total |
| 14:35:18 | engine ready (profile, KV cache, warm-up 29.4 s) |
| 14:36:41 | A/A result: identical_fraction 1.0, 80 decisions |
| 14:37:13 – 14:41:22 | phase 1: checkpoints at rounds 10, 20, 30, 40, 50, 60 |
| 14:41:24 | select: kept 3 of 4 sessions |
| 14:41:28 | app completed |

### Measurements from the log

| Quantity | Value |
|---|---|
| L4 memory available to vLLM | 22.06 GiB × 0.90 = 19.86 GiB |
| KV cache | 4.15 GiB (4850 blocks) |
| Maximum concurrency at 4096 tokens per request | 18.95 |
| Phase 1, rounds 0–30 (8 requests per round) | about 3.2 s per round |
| Phase 1, rounds 30–60 (full 30-round history) | about 6.1 s per round |
| Generator cold start to first reply | about 2 min 40 s |

### Pass conditions (`docs/RUNNING_ON_MODAL.md`)

| Condition | Required | Result |
|---|---|---|
| A/A identical_fraction | ≥ 0.9 | 1.0 |
| Sessions kept | ≥ 2 of 4 | 3 of 4 |
| Parse failures | < 5% | Not shown in the run-2 summary. Download the run and run `scripts/analyze.py` (step below). |

### Not checked by run 2

- The second model family (Mistral-7B, gated) and the `huggingface` secret.
- Stages `controls`, `phase2`, `deviation` on a real GPU.
- Per-session profit index and parse-failure rate. Run 2 used the old summary, which did not
  print them. The analysis now prints a phase-1 table and a stage-timing table.

## Run 3: pilot phase 2, 22 Oct 2026 (pass)

- Modal app run: `ap-aujjGf5PlHX1Or8DsLVRwl`. Stages: `controls,phase2,deviation,analyze`.
  Same run folder `pilot` (resumed after run 2).
- Pre-sprint setup test. n = 3 root sessions per branch and 4 sessions per control: the
  numbers test the pipeline; they are not findings.
- Approximate cost of runs 2 and 3 together, from the Modal billing page (reported by the author): $0.50.

### Summary, verbatim from the run output

Phase 1:

| root_id | rounds | index_select_window | index_last10 | price_seat0_last10 | price_seat1_last10 | parse_failure_rate | kept |
|---|---|---|---|---|---|---|---|
| 0 | 60 | 0.965 | 0.950 | 1.839 | 1.833 | 0.000 | True |
| 1 | 60 | 0.803 | 0.772 | 1.720 | 1.745 | 0.000 | True |
| 2 | 60 | -0.507 | -0.523 | 2.494 | 2.490 | 0.000 | False |
| 3 | 60 | 0.984 | 0.987 | 1.969 | 1.970 | 0.000 | True |

Phase 2 (swap at round 60; post window = rounds 70–79):

| branch | n | pre_index | post_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|
| control | 3 | 0.911 | 0.906 | 0.000 | 0.000 | 0.000 | 0.018 | 9.500 | 1 | 0.000 |
| placebo | 3 | 0.911 | 0.929 | 0.023 | -0.024 | 0.115 | 0.019 | 0.000 | 2 | 0.000 |
| same_inherit | 3 | 0.911 | 0.910 | 0.005 | -0.009 | 0.027 | 0.013 | 0.000 | 2 | 0.000 |
| same_blank | 3 | 0.911 | 0.186 | -0.720 | -1.801 | -0.034 | 1.041 | 8.000 | 1 | 0.000 |
| other_inherit | 3 | 0.911 | 0.643 | -0.263 | -0.683 | -0.001 | 0.339 | 0.000 | 2 | 0.004 |
| other_blank | 3 | 0.911 | 0.370 | -0.536 | -1.608 | 0.017 | 1.489 | 5.500 | 1 | 0.000 |
| br_bot | 3 | 0.911 | 0.546 | -0.359 | -0.509 | -0.180 | 0.457 | n/a | 3 | 0.000 |

Audit, prompt controls ("deviator" = the seat forced to cut; the response is the other seat's):

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 4 | 0 | 0.718 | 0.305 | 0.413 | -0.144 | 0.771 | 0.844 |
| ctrl_default | seat1:incumbent | 4 | 0 | 0.428 | 0.303 | 0.125 | -0.338 | 0.588 | 0.736 |
| ctrl_myopic | seat0:incumbent | 4 | 0 | 0.268 | 0.410 | -0.142 | -0.422 | 0.349 | -0.108 |
| ctrl_myopic | seat1:incumbent | 4 | 0 | 0.510 | 0.409 | 0.102 | -0.392 | 0.595 | -0.328 |
| ctrl_trigger | seat0:incumbent | 4 | 0 | 0.586 | 0.398 | 0.188 | -0.398 | 1.359 | -0.875 |
| ctrl_trigger | seat1:incumbent | 4 | 0 | 1.172 | 0.398 | 0.774 | -0.398 | 1.945 | -0.927 |

Audit, phase-2 branches:

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| br_bot | seat0:incumbent | 3 | 0 | 0.429 | 0.429 | 0.000 | 0.000 | 0.000 | -0.131 |
| br_bot | seat1:entrant | 3 | 0 | 0.000 | 0.418 | -0.418 | -0.423 | -0.415 | -0.285 |
| control | seat0:incumbent | 3 | 0 | 0.000 | 0.414 | -0.414 | -0.434 | -0.382 | 0.029 |
| control | seat1:incumbent | 3 | 0 | 0.000 | 0.415 | -0.415 | -0.434 | -0.384 | 0.466 |
| other_blank | seat0:incumbent | 3 | 0 | -0.043 | 0.328 | -0.370 | -0.433 | -0.317 | 0.513 |
| other_blank | seat1:entrant | 3 | 0 | 0.331 | 0.311 | 0.020 | -0.436 | 0.632 | 0.626 |
| other_inherit | seat0:incumbent | 3 | 0 | 0.569 | 0.404 | 0.165 | -0.434 | 0.491 | 0.113 |
| other_inherit | seat1:entrant | 3 | 0 | 0.346 | 0.407 | -0.061 | -0.433 | 0.648 | 0.007 |
| placebo | seat0:incumbent | 3 | 0 | 0.613 | 0.410 | 0.203 | -0.372 | 0.576 | -0.075 |
| placebo | seat1:incumbent | 3 | 0 | 0.704 | 0.408 | 0.295 | -0.430 | 0.683 | -0.400 |
| same_blank | seat0:incumbent | 3 | 0 | 0.000 | 0.255 | -0.255 | -0.380 | -0.066 | 1.459 |
| same_blank | seat1:entrant | 3 | 0 | 1.307 | 0.287 | 1.021 | -0.363 | 2.484 | -0.848 |
| same_inherit | seat0:incumbent | 3 | 0 | 0.000 | 0.411 | -0.411 | -0.428 | -0.376 | 0.119 |
| same_inherit | seat1:entrant | 3 | 0 | 0.000 | 0.413 | -0.413 | -0.434 | -0.380 | 0.457 |

Stage timings:

| stage | started_utc | seconds |
|---|---|---|
| controls | 2026-10-22T18:02:31+00:00 | 444.400 |
| phase2 | 2026-10-22T18:09:57+00:00 | 454.700 |
| deviation | 2026-10-22T18:17:33+00:00 | 170.300 |

### Checks on run 3 (debug pass, 22 Oct)

| Observation | Diagnosis | Action |
|---|---|---|
| Control (no swap) shows `never_recovered` 1, placebo 2 | Metric artefact: a 0.01 drift counted as a dip that never recovers (reproduced) | Fixed: a dip < 0.05 now counts as no dip (half-life 0) |
| Session 2: prices 2.49, profit index −0.507 | Prices far above the monopoly price (price index ≈ 2.25) give a negative profit index. The inclusion rule correctly excluded it | Added the price index to the phase-1 and phase-2 tables |
| Many audit responses are exactly 0.000 | Consistent with a rival that keeps its price although it saw the cut (anchoring, as in Tran & Yu 2026). Not proven from the summary alone | Audit events now store the rival's prices in both copies, so this can be checked |
| `br_bot` row: response 0.429 = benchmark 0.429 | Sanity check passes: the bot is a pure best responder | None |
| Trigger positive control: excess response 0.188 and 0.774, CIs include 0 | n = 4 sessions per variant is too few | Main run uses 10 sessions per variant |
| Rerun with the new code | Old run folders lacked the new `controls` config field | The config check now fills new fields with their defaults |

### Next step

Main run and replication in parallel (see `docs/RUNNING_ON_MODAL.md`, section 3).
