# Run summary

A/A determinism: {'identical_fraction': 1.0, 'decisions': 80}

Inclusion rule: mean profit index over rounds [50, 100) > 0.3. Kept 15 of 30 sessions.

## Phase 1

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

## Phase 2

| branch | n | pre_index | post_index | post_price_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control | 15 | 0.594 | -0.710 | -0.351 | 0.000 | 0.000 | 0.000 | 0.440 | n/a | 15 | 0.013 |
| placebo | 15 | 0.594 | -0.693 | -0.368 | 0.016 | -0.200 | 0.245 | 0.387 | 94.000 | 14 | 0.013 |
| same_inherit | 15 | 0.594 | -0.652 | -0.336 | 0.057 | -0.236 | 0.338 | 0.421 | 73.000 | 14 | 0.014 |
| same_blank | 15 | 0.594 | -0.219 | 0.350 | 0.491 | -0.030 | 1.000 | 0.960 | 25.000 | 9 | 0.011 |
| other_inherit | 15 | 0.594 | -0.162 | -0.036 | 0.547 | 0.273 | 0.833 | 0.304 | 49.500 | 13 | 0.010 |
| other_blank | 15 | 0.594 | -0.241 | 0.009 | 0.468 | 0.014 | 0.844 | 0.396 | 53.000 | 13 | 0.010 |
| br_bot | 15 | 0.594 | -0.579 | -0.279 | 0.131 | -0.245 | 0.494 | 0.669 | n/a | 15 | 0.010 |

## Pre-registered hypotheses (docs/PREREGISTRATION.md)

| hypothesis | claim | n | estimate | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| H1 | same_inherit - control > -0.10 | 15 | 0.057 | -0.236 | 0.338 | inconclusive |
| H2 | same_blank - control < -0.10 | 15 | 0.491 | -0.030 | 1.000 | not supported |
| H3a | same_inherit - same_blank > 0 | 15 | -0.433 | -0.851 | -0.015 | not supported |
| H3b | other_inherit - other_blank > 0 | 15 | 0.079 | -0.292 | 0.487 | inconclusive |
| H4 | |si-sb| - |si-oi| > 0 | 15 | -0.057 | -0.491 | 0.433 | inconclusive |
| H5 | no LLM responder has excess response CI > 0 (estimate = cells with CI > 0) | 13 | 0.000 | n/a | n/a | supported |

H3 combined (H3a and H3b): not supported

H5 cells (responder is an LLM):

| branch | deviator_seat | n | excess_response | ci_low | ci_high | punishes |
|---|---|---|---|---|---|---|
| br_bot | 1 | 15 | -0.329 | -0.375 | -0.263 | False |
| control | 0 | 15 | -0.310 | -0.384 | -0.204 | False |
| control | 1 | 15 | -0.182 | -0.303 | 0.021 | False |
| other_blank | 0 | 15 | 0.015 | -0.201 | 0.247 | False |
| other_blank | 1 | 15 | -0.224 | -0.331 | -0.078 | False |
| other_inherit | 0 | 15 | -0.064 | -0.297 | 0.184 | False |
| other_inherit | 1 | 15 | -0.301 | -0.370 | -0.199 | False |
| placebo | 0 | 15 | -0.277 | -0.319 | -0.234 | False |
| placebo | 1 | 15 | -0.248 | -0.307 | -0.186 | False |
| same_blank | 0 | 15 | -0.276 | -0.348 | -0.188 | False |
| same_blank | 1 | 15 | -0.321 | -0.441 | -0.227 | False |
| same_inherit | 0 | 15 | -0.261 | -0.362 | -0.123 | False |
| same_inherit | 1 | 15 | -0.110 | -0.259 | 0.056 | False |

## Secondary: price index, branch − control (post window)

| branch | n | price_index_diff | ci_low | ci_high |
|---|---|---|---|---|
| placebo | 15 | -0.016 | -0.148 | 0.117 |
| same_inherit | 15 | 0.015 | -0.137 | 0.163 |
| same_blank | 15 | 0.701 | 0.198 | 1.331 |
| other_inherit | 15 | 0.315 | 0.153 | 0.479 |
| other_blank | 15 | 0.361 | 0.011 | 0.739 |
| br_bot | 15 | 0.072 | -0.148 | 0.278 |

## Audit: controls

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 10 | 0 | 0.331 | 0.363 | -0.032 | -0.441 | 0.520 | -0.197 |
| ctrl_default | seat1:incumbent | 10 | 0 | 0.002 | 0.372 | -0.370 | -0.429 | -0.311 | 0.087 |
| ctrl_myopic | seat0:incumbent | 10 | 0 | 0.025 | 0.345 | -0.320 | -0.355 | -0.288 | 0.194 |
| ctrl_myopic | seat1:incumbent | 10 | 0 | 0.144 | 0.346 | -0.202 | -0.368 | 0.075 | 0.624 |
| ctrl_trigger | seat0:incumbent | 8 | 2 | 0.084 | 0.403 | -0.320 | -0.426 | -0.131 | -0.266 |
| ctrl_trigger | seat1:incumbent | 9 | 1 | -0.237 | 0.398 | -0.635 | -1.228 | -0.213 | 0.693 |

## Audit: deviation

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

## Stage timings

| stage | started_utc | seconds |
|---|---|---|
| aa | 2026-10-22T18:40:58+00:00 | 178.200 |
| controls | 2026-10-22T18:43:58+00:00 | 2280.700 |
| phase1 | 2026-10-22T19:22:00+00:00 | 3248.200 |
| select | 2026-10-22T20:16:10+00:00 | 1.900 |
| phase2 | 2026-10-22T20:16:14+00:00 | 9099.900 |
| deviation | 2026-10-22T22:47:56+00:00 | 1361.500 |
