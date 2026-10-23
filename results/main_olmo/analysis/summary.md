# Run summary

A/A determinism: {'identical_fraction': 1.0, 'decisions': 80}

Inclusion rule: mean profit index over rounds [50, 100) > 0.3. Kept 25 of 30 sessions.

## Phase 1

| root_id | rounds | index_select_window | index_last10 | price_index_last10 | price_seat0_last10 | price_seat1_last10 | parse_failure_rate | kept |
|---|---|---|---|---|---|---|---|---|
| 0 | 100 | -0.955 | -0.908 | 2.520 | 2.609 | 2.615 | 0.000 | False |
| 1 | 100 | 0.552 | 0.845 | 0.769 | 1.867 | 1.774 | 0.000 | True |
| 2 | 100 | 0.997 | 0.999 | 1.033 | 1.940 | 1.940 | 0.000 | True |
| 3 | 100 | -0.091 | -0.074 | -0.044 | 1.456 | 1.450 | 0.000 | False |
| 4 | 100 | 0.292 | 0.348 | 1.731 | 2.255 | 2.256 | 0.000 | False |
| 5 | 100 | -0.237 | -0.123 | 2.013 | 2.392 | 2.374 | 0.000 | False |
| 6 | 100 | 0.985 | 0.975 | 0.861 | 1.864 | 1.860 | 0.000 | True |
| 7 | 100 | 0.741 | 0.439 | 0.286 | 1.601 | 1.603 | 0.000 | True |
| 8 | 100 | 0.973 | 0.981 | 1.121 | 1.978 | 1.981 | 0.000 | True |
| 9 | 100 | 0.999 | 1.000 | 1.011 | 1.930 | 1.930 | 0.000 | True |
| 10 | 100 | 0.936 | 0.931 | 1.229 | 2.029 | 2.028 | 0.000 | True |
| 11 | 100 | 0.940 | 0.951 | 1.192 | 2.014 | 2.010 | 0.000 | True |
| 12 | 100 | 0.976 | 0.976 | 1.135 | 1.984 | 1.988 | 0.000 | True |
| 13 | 100 | 0.999 | 0.999 | 0.967 | 1.910 | 1.910 | 0.000 | True |
| 14 | 100 | 0.990 | 0.981 | 0.879 | 1.871 | 1.870 | 0.000 | True |
| 15 | 100 | 0.991 | 0.987 | 0.902 | 1.882 | 1.879 | 0.000 | True |
| 16 | 100 | 0.964 | 0.935 | 0.776 | 1.832 | 1.815 | 0.000 | True |
| 17 | 100 | 0.996 | 0.997 | 1.050 | 1.950 | 1.945 | 0.000 | True |
| 18 | 100 | 0.989 | 0.990 | 1.086 | 1.963 | 1.965 | 0.000 | True |
| 19 | 100 | 0.880 | 0.849 | 0.649 | 1.766 | 1.767 | 0.000 | True |
| 20 | 100 | 0.996 | 0.996 | 1.055 | 1.950 | 1.950 | 0.000 | True |
| 21 | 100 | 0.978 | 0.973 | 1.143 | 1.990 | 1.989 | 0.000 | True |
| 22 | 100 | 0.864 | 0.852 | 0.652 | 1.769 | 1.766 | 0.000 | True |
| 23 | 100 | 0.819 | 0.760 | 0.551 | 1.721 | 1.723 | 0.000 | True |
| 24 | 100 | 0.980 | 0.969 | 0.845 | 1.855 | 1.855 | 0.000 | True |
| 25 | 100 | 0.989 | 0.989 | 1.090 | 1.970 | 1.961 | 0.000 | True |
| 26 | 100 | 0.256 | 0.196 | 0.122 | 1.531 | 1.525 | 0.000 | False |
| 27 | 100 | 0.991 | 0.999 | 1.006 | 1.929 | 1.926 | 0.000 | True |
| 28 | 100 | 0.991 | 0.993 | 1.070 | 1.962 | 1.951 | 0.000 | True |
| 29 | 100 | 0.934 | 0.896 | 0.711 | 1.791 | 1.798 | 0.000 | True |

## Phase 2

| branch | n | pre_index | post_index | post_price_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control | 25 | 0.930 | 0.687 | 0.720 | 0.000 | 0.000 | 0.000 | 0.157 | 0.000 | 9 | 0.000 |
| placebo | 25 | 0.930 | 0.802 | 0.771 | 0.115 | -0.235 | 0.497 | 0.139 | 0.000 | 8 | 0.000 |
| same_inherit | 25 | 0.930 | 0.900 | 0.836 | 0.213 | 0.006 | 0.529 | 0.127 | 0.000 | 6 | 0.000 |
| same_blank | 25 | 0.930 | 0.063 | 1.125 | -0.624 | -1.021 | -0.215 | 0.980 | 6.000 | 17 | 0.000 |
| other_inherit | 25 | 0.930 | 0.881 | 0.989 | 0.194 | -0.057 | 0.534 | 0.045 | 0.000 | 2 | 0.000 |
| other_blank | 25 | 0.930 | -0.215 | 0.985 | -0.902 | -1.522 | -0.291 | 1.243 | 30.000 | 16 | 0.000 |
| br_bot | 25 | 0.930 | 0.006 | 0.005 | -0.681 | -0.907 | -0.357 | 0.877 | n/a | 25 | 0.000 |

## Pre-registered hypotheses (docs/PREREGISTRATION.md)

| hypothesis | claim | n | estimate | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| H1 | same_inherit - control > -0.10 | 25 | 0.213 | 0.006 | 0.529 | supported |
| H2 | same_blank - control < -0.10 | 25 | -0.624 | -1.021 | -0.215 | supported |
| H3a | same_inherit - same_blank > 0 | 25 | 0.836 | 0.553 | 1.164 | supported |
| H3b | other_inherit - other_blank > 0 | 25 | 1.096 | 0.658 | 1.630 | supported |
| H4 | |si-sb| - |si-oi| > 0 | 25 | 0.818 | 0.501 | 1.122 | supported |
| H6 | other_inherit - control < -0.10 | 25 | 0.194 | -0.057 | 0.534 | not supported |
| H5 | no LLM responder has excess response CI > 0 (estimate = cells with CI > 0) | 13 | 3.000 | n/a | n/a | not supported |
| H5c | no LLM responder has excess response above the myopic control (estimate = such cells) | 13 | 0.000 | n/a | n/a | supported |

H3 combined (H3a and H3b): supported

H5 cells (responder is an LLM):

| branch | deviator_seat | n | excess_response | ci_low | ci_high | punishes |
|---|---|---|---|---|---|---|
| br_bot | 1 | 25 | -0.027 | -0.211 | 0.161 | False |
| control | 0 | 25 | -0.004 | -0.201 | 0.201 | False |
| control | 1 | 25 | 0.009 | -0.180 | 0.212 | False |
| other_blank | 0 | 25 | -0.287 | -0.343 | -0.226 | False |
| other_blank | 1 | 25 | 0.348 | 0.162 | 0.523 | True |
| other_inherit | 0 | 25 | -0.390 | -0.406 | -0.366 | False |
| other_inherit | 1 | 25 | 0.203 | 0.020 | 0.383 | True |
| placebo | 0 | 25 | -0.167 | -0.327 | -0.000 | False |
| placebo | 1 | 25 | -0.137 | -0.299 | 0.041 | False |
| same_blank | 0 | 25 | 0.098 | -0.106 | 0.309 | False |
| same_blank | 1 | 25 | 0.250 | 0.055 | 0.445 | True |
| same_inherit | 0 | 25 | -0.083 | -0.249 | 0.111 | False |
| same_inherit | 1 | 25 | -0.038 | -0.211 | 0.158 | False |

H5c cells, excess response minus the myopic control (pre-registered for the final runs 9-12; exploratory for runs 1-8). Rows with reference True are the prompt controls:

| branch | deviator_seat | n | n_myopic | excess_minus_myopic | ci_low | ci_high | punishes | reference |
|---|---|---|---|---|---|---|---|---|
| ctrl_trigger | both | 19 | 20 | 0.760 | 0.172 | 1.322 | True | True |
| ctrl_default | both | 20 | 20 | -0.135 | -0.456 | 0.191 | False | True |
| br_bot | 1 | 25 | 20 | -0.226 | -0.522 | 0.068 | False | False |
| control | 0 | 25 | 20 | -0.203 | -0.509 | 0.104 | False | False |
| control | 1 | 25 | 20 | -0.190 | -0.495 | 0.119 | False | False |
| other_blank | 0 | 25 | 20 | -0.485 | -0.728 | -0.245 | False | False |
| other_blank | 1 | 25 | 20 | 0.149 | -0.151 | 0.440 | False | False |
| other_inherit | 0 | 25 | 20 | -0.588 | -0.825 | -0.354 | False | False |
| other_inherit | 1 | 25 | 20 | 0.005 | -0.303 | 0.302 | False | False |
| placebo | 0 | 25 | 20 | -0.366 | -0.654 | -0.080 | False | False |
| placebo | 1 | 25 | 20 | -0.336 | -0.629 | -0.047 | False | False |
| same_blank | 0 | 25 | 20 | -0.100 | -0.417 | 0.218 | False | False |
| same_blank | 1 | 25 | 20 | 0.051 | -0.259 | 0.355 | False | False |
| same_inherit | 0 | 25 | 20 | -0.282 | -0.574 | 0.017 | False | False |
| same_inherit | 1 | 25 | 20 | -0.236 | -0.539 | 0.065 | False | False |

## Secondary: price index, branch - control (post window)

| branch | n | price_index_diff | ci_low | ci_high |
|---|---|---|---|---|
| placebo | 25 | 0.052 | -0.229 | 0.341 |
| same_inherit | 25 | 0.116 | -0.035 | 0.328 |
| same_blank | 25 | 0.406 | -0.055 | 0.878 |
| other_inherit | 25 | 0.270 | 0.097 | 0.500 |
| other_blank | 25 | 0.265 | -0.310 | 0.865 |
| br_bot | 25 | -0.715 | -0.905 | -0.481 |

## Exploratory: decision agreement with control (rounds from the swap)

| branch | n | same_seat0 | same_seat1 | roots_identical | first_diff_median |
|---|---|---|---|---|---|
| placebo | 25 | 0.145 | 0.163 | 0 | 102 |
| same_inherit | 25 | 0.134 | 0.143 | 0 | 100 |
| same_blank | 25 | 0.040 | 0.026 | 0 | 100 |
| other_inherit | 25 | 0.163 | 0.222 | 0 | 100 |
| other_blank | 25 | 0.026 | 0.018 | 0 | 100 |
| br_bot | 25 | 0.014 | 0 | 0 | 100 |

## Exploratory: price dynamics per seat (rounds from the swap)

| branch | n | seat0_hold | seat0_match | seat0_abs_change | seat1_hold | seat1_match | seat1_abs_change |
|---|---|---|---|---|---|---|---|
| control | 25 | 0.878 | 0.753 | 0.003 | 0.884 | 0.737 | 0.003 |
| placebo | 25 | 0.809 | 0.637 | 0.003 | 0.868 | 0.666 | 0.003 |
| same_inherit | 25 | 0.811 | 0.672 | 0.004 | 0.862 | 0.678 | 0.002 |
| same_blank | 25 | 0.744 | 0.620 | 0.012 | 0.792 | 0.631 | 0.015 |
| other_inherit | 25 | 0.790 | 0.604 | 0.004 | 0.968 | 0.590 | 0.001 |
| other_blank | 25 | 0.724 | 0.471 | 0.020 | 0.801 | 0.412 | 0.014 |
| br_bot | 25 | 0.801 | 0.006 | 0.007 | 0.793 | 0 | 0.005 |

## Audit: controls

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 10 | 0 | 0.488 | 0.311 | 0.177 | -0.160 | 0.556 | 0.224 |
| ctrl_default | seat1:incumbent | 10 | 0 | 0.259 | 0.309 | -0.050 | -0.274 | 0.211 | 0.516 |
| ctrl_myopic | seat0:incumbent | 10 | 0 | 0.311 | 0.280 | 0.030 | -0.263 | 0.376 | 0.955 |
| ctrl_myopic | seat1:incumbent | 10 | 0 | 0.648 | 0.281 | 0.367 | 0.055 | 0.656 | 0.332 |
| ctrl_trigger | seat0:incumbent | 9 | 1 | 1.563 | 0.398 | 1.164 | 0.383 | 1.945 | -2.222 |
| ctrl_trigger | seat1:incumbent | 10 | 0 | 1.172 | 0.398 | 0.774 | 0.071 | 1.477 | -1.505 |

## Audit: deviation

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| br_bot | seat0:incumbent | 25 | 0 | 0.398 | 0.398 | 0.000 | 0.000 | 0.000 | -0.383 |
| br_bot | seat1:entrant | 25 | 0 | 0.371 | 0.398 | -0.027 | -0.211 | 0.161 | -0.567 |
| control | seat0:incumbent | 25 | 0 | 0.388 | 0.392 | -0.004 | -0.201 | 0.201 | -0.043 |
| control | seat1:incumbent | 25 | 0 | 0.400 | 0.391 | 0.009 | -0.180 | 0.212 | -0.288 |
| other_blank | seat0:incumbent | 25 | 0 | 0.000 | 0.287 | -0.287 | -0.343 | -0.226 | 0.663 |
| other_blank | seat1:entrant | 25 | 0 | 0.634 | 0.286 | 0.348 | 0.162 | 0.523 | -0.622 |
| other_inherit | seat0:incumbent | 25 | 0 | 0.000 | 0.390 | -0.390 | -0.406 | -0.366 | 1.044 |
| other_inherit | seat1:entrant | 25 | 0 | 0.591 | 0.388 | 0.203 | 0.020 | 0.383 | -1.280 |
| placebo | seat0:incumbent | 25 | 0 | 0.235 | 0.402 | -0.167 | -0.327 | -0.000 | -0.076 |
| placebo | seat1:incumbent | 25 | 0 | 0.265 | 0.403 | -0.137 | -0.299 | 0.041 | -0.288 |
| same_blank | seat0:incumbent | 25 | 0 | 0.388 | 0.290 | 0.098 | -0.106 | 0.309 | 0.574 |
| same_blank | seat1:entrant | 25 | 0 | 0.540 | 0.290 | 0.250 | 0.055 | 0.445 | 0.384 |
| same_inherit | seat0:incumbent | 25 | 0 | 0.327 | 0.410 | -0.083 | -0.249 | 0.111 | 0.119 |
| same_inherit | seat1:entrant | 25 | 0 | 0.373 | 0.411 | -0.038 | -0.211 | 0.158 | -0.272 |

## Stage timings

| stage | started_utc | seconds |
|---|---|---|
| aa | 2026-10-23T03:25:38+00:00 | 169.000 |
| controls | 2026-10-23T03:28:28+00:00 | 1272.100 |
| phase1 | 2026-10-23T03:49:41+00:00 | 2162.800 |
| select | 2026-10-23T04:25:45+00:00 | 1.400 |
| phase2 | 2026-10-23T04:25:48+00:00 | 11217.200 |
| deviation | 2026-10-23T07:32:47+00:00 | 1812.800 |
