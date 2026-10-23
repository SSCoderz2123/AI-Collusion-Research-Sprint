# Run summary

A/A determinism: {'identical_fraction': 1.0, 'decisions': 80}

Inclusion rule: mean profit index over rounds [30, 60) > 0.3. Kept 3 of 4 sessions.

## Phase 1

| root_id | rounds | index_select_window | index_last10 | price_seat0_last10 | price_seat1_last10 | parse_failure_rate | kept |
|---|---|---|---|---|---|---|---|
| 0 | 60 | 0.965 | 0.950 | 1.839 | 1.833 | 0.000 | True |
| 1 | 60 | 0.803 | 0.772 | 1.720 | 1.745 | 0.000 | True |
| 2 | 60 | -0.507 | -0.523 | 2.494 | 2.490 | 0.000 | False |
| 3 | 60 | 0.984 | 0.987 | 1.969 | 1.970 | 0.000 | True |

## Phase 2

| branch | n | pre_index | post_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|
| control | 3 | 0.911 | 0.906 | 0.000 | 0.000 | 0.000 | 0.018 | 9.500 | 1 | 0.000 |
| placebo | 3 | 0.911 | 0.929 | 0.023 | -0.024 | 0.115 | 0.019 | 0.000 | 2 | 0.000 |
| same_inherit | 3 | 0.911 | 0.910 | 0.005 | -0.009 | 0.027 | 0.013 | 0.000 | 2 | 0.000 |
| same_blank | 3 | 0.911 | 0.186 | -0.720 | -1.801 | -0.034 | 1.041 | 8.000 | 1 | 0.000 |
| other_inherit | 3 | 0.911 | 0.643 | -0.263 | -0.683 | -0.001 | 0.339 | 0.000 | 2 | 0.004 |
| other_blank | 3 | 0.911 | 0.370 | -0.536 | -1.608 | 0.017 | 1.489 | 5.500 | 1 | 0.000 |
| br_bot | 3 | 0.911 | 0.546 | -0.359 | -0.509 | -0.180 | 0.457 | n/a | 3 | 0.000 |

## Audit: controls

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 4 | 0 | 0.718 | 0.305 | 0.413 | -0.144 | 0.771 | 0.844 |
| ctrl_default | seat1:incumbent | 4 | 0 | 0.428 | 0.303 | 0.125 | -0.338 | 0.588 | 0.736 |
| ctrl_myopic | seat0:incumbent | 4 | 0 | 0.268 | 0.410 | -0.142 | -0.422 | 0.349 | -0.108 |
| ctrl_myopic | seat1:incumbent | 4 | 0 | 0.510 | 0.409 | 0.102 | -0.392 | 0.595 | -0.328 |
| ctrl_trigger | seat0:incumbent | 4 | 0 | 0.586 | 0.398 | 0.188 | -0.398 | 1.359 | -0.875 |
| ctrl_trigger | seat1:incumbent | 4 | 0 | 1.172 | 0.398 | 0.774 | -0.398 | 1.945 | -0.927 |

## Audit: deviation

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

## Stage timings

| stage | started_utc | seconds |
|---|---|---|
| controls | 2026-10-22T18:02:31+00:00 | 444.400 |
| phase2 | 2026-10-22T18:09:57+00:00 | 454.700 |
| deviation | 2026-10-22T18:17:33+00:00 | 170.300 |
