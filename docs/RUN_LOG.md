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
| Main run `main` (run 4) | Done 22 Oct; H1, H2, H3 supported; H4 inconclusive; H5 not supported |
| Replication `main_mistral` (run 5) | Done 22 Oct; control cartel collapses; audit positive control fails; cannot test succession |
| Sprint runs 6–8 (`main_r2`, `main_olmo`, `main_noannounce`) | Pre-registered 23 Oct; not started |

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

## Run 4: main (Qwen incumbent, primary), 22 Oct 2026

- Started 22 Oct 2026 18:40:57 UTC with `modal run --detach … --config configs/main.yaml,configs/main_mistral.yaml`.
  The `aa` stage ran twice (18:40:57 and 18:59:21 UTC): the run was started again with `--detach`
  and resumed from its checkpoints. Phase 1 started 19:05:21 UTC.
- **Pre-sprint run.** It started before the sprint start (Fri 23 Oct 2026). Disclosed in
  `docs/PREEXISTING_WORK.md`.
- The design was fixed before phase 1: `docs/PREREGISTRATION.md` and `configs/main.yaml` were merged
  to `main` at 18:38:51 UTC (merge `5d8c2fe`, commit `8cf75a6`).
- Summary below is verbatim from `python scripts/analyze.py results/main`. It was produced
  before the hypothesis evaluator existed; re-run the script to add the H1–H5 section.

### Summary, verbatim

A/A determinism: {'identical_fraction': 1.0, 'decisions': 80}

Inclusion rule: mean profit index over rounds [50, 100) > 0.3. Kept 16 of 30 sessions.

Phase 1:

| root_id | rounds | index_select_window | index_last10 | price_index_last10 | price_seat0_last10 | price_seat1_last10 | parse_failure_rate | kept |
|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 0.558 | 0.626 | 1.541 | 2.169 | 2.170 | 0.000 | True |
| 1 | 100 | -1.606 | -1.567 | -0.852 | 1.087 | 1.089 | 0.000 | False |
| 2 | 100 | 0.289 | 0.345 | 1.733 | 2.248 | 2.265 | 0.000 | False |
| 3 | 100 | 0.997 | 0.998 | 0.966 | 1.909 | 1.910 | 0.000 | True |
| 4 | 100 | 0.634 | 0.482 | 0.318 | 1.621 | 1.612 | 0.000 | True |
| 5 | 100 | -0.271 | -0.179 | 2.045 | 2.399 | 2.396 | 0.000 | False |
| 6 | 100 | -0.099 | -0.002 | 1.941 | 2.351 | 2.350 | 0.000 | False |
| 7 | 100 | 0.995 | 0.996 | 1.055 | 1.950 | 1.950 | 0.000 | True |
| 8 | 100 | -0.420 | -0.352 | 2.148 | 2.440 | 2.448 | 0.000 | False |
| 9 | 100 | 0.999 | 0.999 | 0.967 | 1.910 | 1.910 | 0.000 | True |
| 10 | 100 | 0.980 | 0.956 | 0.813 | 1.842 | 1.839 | 0.000 | True |
| 11 | 100 | 0.922 | 0.948 | 1.197 | 2.013 | 2.015 | 0.000 | True |
| 12 | 100 | 0.968 | 0.973 | 1.144 | 1.990 | 1.990 | 0.000 | True |
| 13 | 100 | -1.580 | -1.574 | 3.254 | 2.945 | 2.943 | 0.000 | False |
| 14 | 100 | -0.275 | -0.195 | -0.095 | 1.468 | 1.392 | 0.000 | False |
| 15 | 100 | -0.320 | -0.316 | 2.127 | 2.438 | 2.431 | 0.000 | False |
| 16 | 100 | 0.983 | 0.991 | 0.922 | 1.890 | 1.889 | 0.000 | True |
| 17 | 100 | -0.028 | -0.047 | 1.968 | 2.365 | 2.360 | 0.000 | False |
| 18 | 100 | 0.989 | 0.979 | 0.873 | 1.867 | 1.868 | 0.000 | True |
| 19 | 100 | 0.430 | 0.824 | 1.365 | 2.100 | 2.080 | 0.000 | True |
| 20 | 100 | -0.528 | -0.473 | -0.272 | 1.350 | 1.350 | 0.000 | False |
| 21 | 100 | -0.001 | -0.022 | 1.953 | 2.357 | 2.355 | 0.000 | False |
| 22 | 100 | 1.000 | 1.000 | 1.011 | 1.930 | 1.930 | 0.000 | True |
| 23 | 100 | 0.138 | 0.272 | 1.780 | 2.305 | 2.250 | 0.000 | False |
| 24 | 100 | 0.989 | 1.000 | 0.990 | 1.921 | 1.920 | 0.000 | True |
| 25 | 100 | 0.262 | 0.245 | 0.154 | 1.542 | 1.543 | 0.000 | False |
| 26 | 100 | 0.988 | 0.990 | 0.912 | 1.880 | 1.890 | 0.000 | True |
| 27 | 100 | 0.855 | 0.853 | 0.653 | 1.770 | 1.766 | 0.000 | True |
| 28 | 100 | 0.956 | 0.939 | 1.216 | 2.023 | 2.022 | 0.005 | True |
| 29 | 100 | -1.058 | -0.997 | -0.554 | 1.226 | 1.219 | 0.010 | False |

Phase 2 (swap at round 100; post window = rounds 150–199):

| branch | n | pre_index | post_index | post_price_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control | 16 | 0.908 | 0.907 | 0.948 | 0.000 | 0.000 | 0.000 | 0.015 | 0.000 | 4 | 0.000 |
| placebo | 16 | 0.908 | 0.828 | 0.804 | -0.079 | -0.205 | 0.023 | 0.109 | 0.000 | 5 | 0.000 |
| same_inherit | 16 | 0.908 | 0.904 | 0.925 | -0.003 | -0.065 | 0.064 | 0.003 | 0.000 | 3 | 0.000 |
| same_blank | 16 | 0.908 | 0.237 | 1.440 | -0.670 | -0.998 | -0.360 | 0.878 | 10.500 | 8 | 0.000 |
| other_inherit | 16 | 0.908 | 0.355 | 0.271 | -0.552 | -0.763 | -0.362 | 0.058 | 44.000 | 14 | 0.003 |
| other_blank | 16 | 0.908 | -0.313 | 0.636 | -1.219 | -1.715 | -0.760 | 1.774 | 58.500 | 6 | 0.003 |
| br_bot | 16 | 0.908 | -0.002 | -0.001 | -0.909 | -0.973 | -0.806 | 0.824 | n/a | 16 | 0.000 |

Audit, prompt controls ("deviator" = the seat forced to cut; the response is the other seat's):

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 10 | 0 | 0.129 | 0.356 | -0.227 | -0.383 | 0.028 | 0.625 |
| ctrl_default | seat1:incumbent | 10 | 0 | 0.486 | 0.358 | 0.128 | -0.162 | 0.416 | 0.214 |
| ctrl_myopic | seat0:incumbent | 10 | 0 | 0.080 | 0.319 | -0.240 | -0.381 | -0.051 | 0.474 |
| ctrl_myopic | seat1:incumbent | 10 | 0 | 0.177 | 0.319 | -0.142 | -0.369 | 0.128 | 0.290 |
| ctrl_trigger | seat0:incumbent | 10 | 0 | 1.641 | 0.398 | 1.242 | 0.539 | 1.945 | -1.485 |
| ctrl_trigger | seat1:incumbent | 10 | 0 | 1.406 | 0.398 | 1.008 | 0.305 | 1.711 | -0.895 |

Audit, phase-2 branches:

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| br_bot | seat0:incumbent | 16 | 0 | 0.398 | 0.398 | 0.000 | 0.000 | 0.000 | -0.498 |
| br_bot | seat1:entrant | 16 | 0 | 0.840 | 0.398 | 0.442 | 0.225 | 0.629 | -1.087 |
| control | seat0:incumbent | 16 | 0 | 0.438 | 0.396 | 0.041 | -0.206 | 0.293 | 0.075 |
| control | seat1:incumbent | 16 | 0 | 0.275 | 0.396 | -0.122 | -0.319 | 0.105 | 0.196 |
| other_blank | seat0:incumbent | 16 | 0 | 0.002 | 0.277 | -0.275 | -0.338 | -0.214 | 0.177 |
| other_blank | seat1:entrant | 16 | 0 | 0.487 | 0.277 | 0.210 | -0.010 | 0.440 | 0.066 |
| other_inherit | seat0:incumbent | 16 | 0 | 0.086 | 0.397 | -0.311 | -0.403 | -0.163 | -0.240 |
| other_inherit | seat1:entrant | 16 | 0 | 0.319 | 0.393 | -0.074 | -0.279 | 0.151 | -0.829 |
| placebo | seat0:incumbent | 16 | 0 | 0.406 | 0.406 | 0.000 | -0.226 | 0.242 | -0.144 |
| placebo | seat1:incumbent | 16 | 0 | 0.489 | 0.405 | 0.084 | -0.150 | 0.317 | -0.574 |
| same_blank | seat0:incumbent | 16 | 0 | 0.373 | 0.289 | 0.084 | -0.144 | 0.323 | 0.553 |
| same_blank | seat1:entrant | 16 | 0 | 0.573 | 0.290 | 0.283 | 0.049 | 0.512 | 0.934 |
| same_inherit | seat0:incumbent | 16 | 0 | 0.355 | 0.397 | -0.042 | -0.258 | 0.186 | -0.030 |
| same_inherit | seat1:entrant | 16 | 0 | 0.499 | 0.398 | 0.100 | -0.139 | 0.343 | -0.288 |

Stage timings:

| stage | started_utc | seconds |
|---|---|---|
| aa | 2026-10-22T18:40:57+00:00 | 141.200 |
| aa | 2026-10-22T18:59:21+00:00 | 82.800 |
| controls | 2026-10-22T19:00:45+00:00 | 274.500 |
| phase1 | 2026-10-22T19:05:21+00:00 | 2128.800 |
| select | 2026-10-22T19:40:52+00:00 | 1.500 |
| phase2 | 2026-10-22T19:40:55+00:00 | 7084.700 |
| deviation | 2026-10-22T21:39:01+00:00 | 1161.000 |

## Run 5: main_mistral (Mistral incumbent, replication), 22 Oct 2026

- Same launch as run 4. Pre-sprint run (disclosed). Summary verbatim from
  `python scripts/analyze.py results/main_mistral`.

### Summary, verbatim

A/A determinism: {'identical_fraction': 1.0, 'decisions': 80}

Inclusion rule: mean profit index over rounds [50, 100) > 0.3. Kept 15 of 30 sessions.

Phase 1:

| root_id | rounds | index_select_window | index_last10 | price_index_last10 | price_seat0_last10 | price_seat1_last10 | parse_failure_rate | kept |
|---|---|---|---|---|---|---|---|---|
| 0 | 100 | -1.838 | -2.128 | 0.036 | 2.034 | 0.944 | 0.000 | False |
| 1 | 100 | -2.936 | -3.202 | -1.666 | 0.734 | 0.706 | 0.015 | False |
| 2 | 100 | -0.432 | -0.722 | -0.401 | 1.272 | 1.311 | 0.015 | False |
| 3 | 100 | 0.564 | 0.911 | 0.776 | 1.773 | 1.875 | 0.015 | True |
| 4 | 100 | -0.945 | -1.110 | -0.607 | 1.210 | 1.187 | 0.010 | False |
| 5 | 100 | 0.025 | -0.418 | -0.235 | 1.352 | 1.381 | 0.015 | False |
| 6 | 100 | 0.271 | -0.104 | -0.060 | 1.453 | 1.439 | 0.015 | False |
| 7 | 100 | 0.728 | 0.657 | 0.458 | 1.678 | 1.681 | 0.060 | True |
| 8 | 100 | 0.408 | -0.051 | -0.025 | 1.446 | 1.478 | 0.005 | True |
| 9 | 100 | -0.763 | -0.944 | -0.522 | 1.218 | 1.256 | 0.000 | False |
| 10 | 100 | 0.196 | 0.011 | 0.020 | 1.447 | 1.517 | 0.040 | False |
| 11 | 100 | 0.592 | 0.417 | 0.272 | 1.584 | 1.608 | 0.030 | True |
| 12 | 100 | -2.267 | -2.422 | -1.280 | 0.926 | 0.863 | 0.005 | False |
| 13 | 100 | 0.805 | 0.970 | 0.861 | 1.867 | 1.857 | 0.010 | True |
| 14 | 100 | 0.661 | 0.694 | 1.486 | 2.155 | 2.134 | 0.015 | True |
| 15 | 100 | 0.589 | 0.340 | 0.220 | 1.566 | 1.579 | 0.035 | True |
| 16 | 100 | 0.492 | 0.274 | 0.176 | 1.539 | 1.566 | 0.010 | True |
| 17 | 100 | -0.317 | -0.384 | 0.013 | 1.651 | 1.306 | 0.035 | False |
| 18 | 100 | 0.715 | 0.919 | 0.751 | 1.830 | 1.795 | 0.005 | True |
| 19 | 100 | 0.115 | -0.203 | -0.118 | 1.422 | 1.417 | 0.005 | False |
| 20 | 100 | 0.667 | 0.565 | 0.385 | 1.634 | 1.660 | 0.000 | True |
| 21 | 100 | 0.443 | 0.188 | 0.119 | 1.539 | 1.514 | 0.060 | True |
| 22 | 100 | -2.048 | -2.012 | -1.078 | 0.998 | 0.973 | 0.000 | False |
| 23 | 100 | 0.679 | 0.446 | 0.297 | 1.596 | 1.618 | 0.015 | True |
| 24 | 100 | 0.732 | 0.608 | 0.415 | 1.661 | 1.660 | 0.000 | True |
| 25 | 100 | -1.186 | -1.750 | -0.944 | 1.041 | 1.051 | 0.000 | False |
| 26 | 100 | 0.769 | 0.584 | 0.402 | 1.676 | 1.633 | 0.015 | True |
| 27 | 100 | -1.952 | -2.098 | -1.121 | 0.951 | 0.981 | 0.055 | False |
| 28 | 100 | 0.881 | 0.669 | 0.468 | 1.690 | 1.678 | 0.000 | True |
| 29 | 100 | -1.763 | -2.259 | -1.188 | 0.977 | 0.895 | 0.005 | False |

Phase 2 (swap at round 100; post window = rounds 150–199):

| branch | n | pre_index | post_index | post_price_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control | 15 | 0.594 | -0.710 | -0.351 | 0.000 | 0.000 | 0.000 | 0.440 | n/a | 15 | 0.013 |
| placebo | 15 | 0.594 | -0.693 | -0.368 | 0.016 | -0.200 | 0.245 | 0.387 | 94.000 | 14 | 0.013 |
| same_inherit | 15 | 0.594 | -0.652 | -0.336 | 0.057 | -0.236 | 0.338 | 0.421 | 73.000 | 14 | 0.014 |
| same_blank | 15 | 0.594 | -0.219 | 0.350 | 0.491 | -0.030 | 1.000 | 0.960 | 25.000 | 9 | 0.011 |
| other_inherit | 15 | 0.594 | -0.162 | -0.036 | 0.547 | 0.273 | 0.833 | 0.304 | 49.500 | 13 | 0.010 |
| other_blank | 15 | 0.594 | -0.241 | 0.009 | 0.468 | 0.014 | 0.844 | 0.396 | 53.000 | 13 | 0.010 |
| br_bot | 15 | 0.594 | -0.579 | -0.279 | 0.131 | -0.245 | 0.494 | 0.669 | n/a | 15 | 0.010 |

Audit, prompt controls:

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 10 | 0 | 0.331 | 0.363 | -0.032 | -0.441 | 0.520 | -0.197 |
| ctrl_default | seat1:incumbent | 10 | 0 | 0.002 | 0.372 | -0.370 | -0.429 | -0.311 | 0.087 |
| ctrl_myopic | seat0:incumbent | 10 | 0 | 0.025 | 0.345 | -0.320 | -0.355 | -0.288 | 0.194 |
| ctrl_myopic | seat1:incumbent | 10 | 0 | 0.144 | 0.346 | -0.202 | -0.368 | 0.075 | 0.624 |
| ctrl_trigger | seat0:incumbent | 8 | 2 | 0.084 | 0.403 | -0.320 | -0.426 | -0.131 | -0.266 |
| ctrl_trigger | seat1:incumbent | 9 | 1 | -0.237 | 0.398 | -0.635 | -1.228 | -0.213 | 0.693 |

Audit, phase-2 branches:

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| br_bot | seat0:incumbent | 15 | 0 | 0.279 | 0.279 | 0.000 | 0.000 | 0.000 | -0.425 |
| br_bot | seat1:entrant | 15 | 0 | 0.032 | 0.361 | -0.329 | -0.375 | -0.263 | -0.100 |
| control | seat0:incumbent | 15 | 0 | -0.018 | 0.291 | -0.310 | -0.384 | -0.204 | -0.770 |
| control | seat1:incumbent | 15 | 0 | 0.106 | 0.288 | -0.182 | -0.303 | 0.021 | -0.641 |
| other_blank | seat0:incumbent | 15 | 0 | 0.345 | 0.330 | 0.015 | -0.201 | 0.247 | -0.685 |
| other_blank | seat1:entrant | 15 | 0 | 0.114 | 0.338 | -0.224 | -0.331 | -0.078 | -0.526 |
| other_inherit | seat0:incumbent | 15 | 0 | 0.278 | 0.342 | -0.064 | -0.297 | 0.184 | -0.623 |
| other_inherit | seat1:entrant | 15 | 0 | 0.048 | 0.349 | -0.301 | -0.370 | -0.199 | -0.240 |
| placebo | seat0:incumbent | 15 | 0 | 0.015 | 0.293 | -0.277 | -0.319 | -0.234 | -0.487 |
| placebo | seat1:incumbent | 15 | 0 | 0.042 | 0.290 | -0.248 | -0.307 | -0.186 | -0.489 |
| same_blank | seat0:incumbent | 15 | 0 | 0.048 | 0.324 | -0.276 | -0.348 | -0.188 | -0.614 |
| same_blank | seat1:entrant | 15 | 0 | 0.010 | 0.331 | -0.321 | -0.441 | -0.227 | -0.117 |
| same_inherit | seat0:incumbent | 15 | 0 | 0.032 | 0.292 | -0.261 | -0.362 | -0.123 | -0.371 |
| same_inherit | seat1:entrant | 15 | 0 | 0.178 | 0.289 | -0.110 | -0.259 | 0.056 | -1.007 |

Stage timings:

| stage | started_utc | seconds |
|---|---|---|
| aa | 2026-10-22T18:40:58+00:00 | 178.200 |
| controls | 2026-10-22T18:43:58+00:00 | 2280.700 |
| phase1 | 2026-10-22T19:22:00+00:00 | 3248.200 |
| select | 2026-10-22T20:16:10+00:00 | 1.900 |
| phase2 | 2026-10-22T20:16:14+00:00 | 9099.900 |
| deviation | 2026-10-22T22:47:56+00:00 | 1361.500 |

## Checks on runs 4–5 against the pre-registration (23 Oct)

Verdict rule: the 95% CI must lie entirely on the stated side of the threshold. H1, H2 and H5
can be read from the tables above. H3 and H4 need a CI of a difference between two branches,
which the run-4/5 summaries do not contain: re-run `scripts/analyze.py` (it now writes
`analysis/hypotheses.json`) and copy that section here. Do not quote H3/H4 verdicts before that.

### Run 4 (primary, Qwen incumbent)

| Check | Source in the table | Result |
|---|---|---|
| Inclusion: ≥ 12 of 30 kept | selection line | 16 of 30: pass |
| A/A determinism | A/A line | 1.0 |
| Parse failures < 5% | phase-1 and phase-2 tables | ≤ 0.010 per session, ≤ 0.003 per branch: pass |
| Audit positive control (trigger) | controls audit | excess 1.242 [0.539, 1.945] and 1.008 [0.305, 1.711]: the audit detects instructed punishment |
| Audit placebo (myopic) and default prompt | controls audit | no CI entirely above 0 |
| Negative control (`br_bot` entrant) | phase 2 | post price index −0.001: prices fall to the Nash price |
| **H1** same_inherit − control > −0.10 | diff −0.003 [−0.065, 0.064] | **supported** |
| **H2** same_blank − control < −0.10 | diff −0.670 [−0.998, −0.360] | **supported** (but see the price index below) |
| H3, H4 | need `hypotheses.json` | pending |
| **H5** no LLM responder punishes | deviation audit | **not supported**: 2 cells have a CI entirely above 0: `same_blank` entrant cut → incumbent 0.283 [0.049, 0.512]; `br_bot` cut → incumbent 0.442 [0.225, 0.629] |

Observations that the profit index alone hides (from `post_price_index`):

- `same_blank`: profit index 0.237 but price index **1.440**: the prices go **above** the monopoly
  price, not down to the Nash price. The blank same-model entrant does not restore
  competition; it miscoordinates upward. Phase 1 shows the same Qwen tendency: 9 of the 14
  excluded sessions have price index > 1.7 (sessions 2, 5, 6, 8, 13, 15, 17, 21, 23); 4 are below
  the Nash price (1, 14, 20, 29).
- `other_inherit`: price index 0.271: a Mistral entrant with the full history moves prices
  toward the Nash price.
- `other_blank`: profit index −0.313 with price index 0.636: the two firms end at different prices.
- `placebo` (notice only): −0.079 [−0.205, 0.023]: the CI includes 0.

### Run 5 (replication, Mistral incumbent)

| Check | Source | Result |
|---|---|---|
| Inclusion | selection line | 15 of 30: pass |
| A/A determinism | A/A line | 1.0 |
| Parse failures | phase 1 | above 5% in 3 sessions: 7 and 21 (0.060), 27 (0.055); ≤ 0.014 per phase-2 branch |
| Audit positive control (trigger) | controls audit | **fails**: excess −0.320 [−0.426, −0.131] and −0.635 [−1.228, −0.213]; 3 invalid events. Mistral does not follow the instructed trigger rule, so the audit cannot be validated on Mistral |
| Baseline cartel persists in control | phase 2 control | **no**: profit index 0.594 before the swap → −0.710 after; price index −0.351 (below Nash); 15 of 15 never recover |
| H1 | 0.057 [−0.236, 0.338] | inconclusive |
| H2 | 0.491 [−0.030, 1.000] | not supported (the swap branches end higher than the collapsing control) |

Conclusion for run 5: the Mistral cartel does not persist without a swap, so the replication
cannot test succession. Report it as a negative result about Mistral's stability, not as
evidence for or against H1–H5.

## Hypothesis evaluation of runs 4–5 (23 Oct, `succession/hypotheses.py`)

Verbatim from `python scripts/analyze.py results/main` and `results/main_mistral`, run after
PR #5 was merged. This replaces the "pending" entries above.

### Run 4 (`main`, primary)

| hypothesis | claim | n | estimate | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| H1 | same_inherit - control > -0.10 | 16 | -0.003 | -0.065 | 0.064 | supported |
| H2 | same_blank - control < -0.10 | 16 | -0.670 | -0.998 | -0.360 | supported |
| H3a | same_inherit - same_blank > 0 | 16 | 0.667 | 0.368 | 0.989 | supported |
| H3b | other_inherit - other_blank > 0 | 16 | 0.668 | 0.183 | 1.206 | supported |
| H4 | \|si-sb\| - \|si-oi\| > 0 | 16 | 0.118 | -0.294 | 0.519 | inconclusive |
| H5 | no LLM responder has excess response CI > 0 (estimate = cells with CI > 0) | 13 | 2.000 | n/a | n/a | not supported |

H3 combined (H3a and H3b): supported. H5 cells with CI > 0: `br_bot` deviator seat 1
(0.442 [0.225, 0.629]) and `same_blank` deviator seat 1 (0.283 [0.049, 0.512]).

Secondary, price index, branch − control:

| branch | n | price_index_diff | ci_low | ci_high |
|---|---|---|---|---|
| placebo | 16 | -0.144 | -0.353 | 0.032 |
| same_inherit | 16 | -0.023 | -0.140 | 0.075 |
| same_blank | 16 | 0.492 | 0.162 | 0.834 |
| other_inherit | 16 | -0.677 | -0.874 | -0.500 |
| other_blank | 16 | -0.312 | -0.929 | 0.293 |
| br_bot | 16 | -0.949 | -1.072 | -0.805 |

### Run 5 (`main_mistral`, replication)

| hypothesis | claim | n | estimate | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| H1 | same_inherit - control > -0.10 | 15 | 0.057 | -0.236 | 0.338 | inconclusive |
| H2 | same_blank - control < -0.10 | 15 | 0.491 | -0.030 | 1.000 | not supported |
| H3a | same_inherit - same_blank > 0 | 15 | -0.433 | -0.851 | -0.015 | not supported |
| H3b | other_inherit - other_blank > 0 | 15 | 0.079 | -0.292 | 0.487 | inconclusive |
| H4 | \|si-sb\| - \|si-oi\| > 0 | 15 | -0.057 | -0.491 | 0.433 | inconclusive |
| H5 | no LLM responder has excess response CI > 0 (estimate = cells with CI > 0) | 13 | 0.000 | n/a | n/a | supported |

H3 combined: not supported. Secondary price index, branch − control: placebo −0.016
[−0.148, 0.117]; same_inherit 0.015 [−0.137, 0.163]; same_blank 0.701 [0.198, 1.331];
other_inherit 0.315 [0.153, 0.479]; other_blank 0.361 [0.011, 0.739]; br_bot 0.072 [−0.148, 0.278].
Run 5 remains uninformative about succession: its control cartel collapses (see above), and its
H5 "supported" has no validated audit, because the Mistral trigger positive control failed.

### What runs 4–5 establish (Qwen incumbent only)

1. Same model + inherited history: no change against control (H1; profit and price index both ≈ 0).
2. Same model + blank history: profit falls (H2) because prices rise **above** the monopoly
   price (price index +0.492 [0.162, 0.834]), not because competition returns.
3. History matters for both entrant families (H3a, H3b).
4. Model identity vs history (H4): no decision; the CI is wide.
5. Different family (Mistral) + inherited history: prices fall toward Nash (price index −0.677).
6. Enforcement: mostly absent; 2 of 13 cells punish (H5 not supported).

Open points: one seed set, run before the sprint start, one "other" family (Mistral). Runs 6–8
address these (`docs/PREREGISTRATION.md`, sprint additions).

### Next step

Runs 6–8 (`docs/RUNNING_ON_MODAL.md`, section 5). Add their summaries and the pooled result here.
