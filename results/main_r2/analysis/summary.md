# Run summary

A/A determinism: {'identical_fraction': 1.0, 'decisions': 80}

Inclusion rule: mean profit index over rounds [50, 100) > 0.3. Kept 22 of 30 sessions.

## Phase 1

| root_id | rounds | index_select_window | index_last10 | price_index_last10 | price_seat0_last10 | price_seat1_last10 | parse_failure_rate | kept |
|---|---|---|---|---|---|---|---|---|
| 0 | 100 | -0.069 | 0.013 | 1.932 | 2.350 | 2.343 | 0.000 | False |
| 1 | 100 | 0.998 | 1.000 | 1.013 | 1.931 | 1.931 | 0.000 | True |
| 2 | 100 | 0.973 | 0.967 | 0.839 | 1.855 | 1.849 | 0.000 | True |
| 3 | 100 | 0.984 | 0.987 | 1.097 | 1.968 | 1.970 | 0.000 | True |
| 4 | 100 | -0.330 | -0.245 | 2.085 | 2.431 | 2.400 | 0.000 | False |
| 5 | 100 | -0.624 | -0.612 | 2.312 | 2.516 | 2.520 | 0.000 | False |
| 6 | 100 | -0.354 | -0.340 | 2.141 | 2.448 | 2.434 | 0.000 | False |
| 7 | 100 | 0.699 | 0.505 | 0.375 | 1.675 | 1.610 | 0.000 | True |
| 8 | 100 | 0.955 | 0.955 | 0.811 | 1.840 | 1.839 | 0.000 | True |
| 9 | 100 | 0.990 | 0.991 | 1.081 | 1.956 | 1.967 | 0.000 | True |
| 10 | 100 | 0.992 | 0.996 | 1.029 | 1.929 | 1.947 | 0.000 | True |
| 11 | 100 | 0.971 | 0.973 | 1.144 | 1.990 | 1.990 | 0.000 | True |
| 12 | 100 | 0.031 | 0.046 | 0.028 | 1.487 | 1.484 | 0.000 | False |
| 13 | 100 | 0.254 | 0.253 | 1.790 | 2.273 | 2.291 | 0.000 | False |
| 14 | 100 | 0.801 | 0.801 | 0.596 | 1.740 | 1.745 | 0.000 | True |
| 15 | 100 | 0.515 | 0.506 | 1.627 | 2.210 | 2.207 | 0.000 | True |
| 16 | 100 | 0.531 | 0.569 | 1.583 | 2.189 | 2.188 | 0.000 | True |
| 17 | 100 | -0.691 | -0.623 | 2.318 | 2.520 | 2.522 | 0.000 | False |
| 18 | 100 | 0.892 | 0.537 | 0.386 | 1.610 | 1.685 | 0.000 | True |
| 19 | 100 | 0.995 | 0.987 | 0.900 | 1.880 | 1.880 | 0.000 | True |
| 20 | 100 | 0.965 | 0.944 | 0.832 | 1.878 | 1.820 | 0.000 | True |
| 21 | 100 | 0.911 | 0.918 | 0.745 | 1.809 | 1.810 | 0.000 | True |
| 22 | 100 | 0.997 | 0.996 | 1.056 | 1.951 | 1.950 | 0.000 | True |
| 23 | 100 | 0.400 | 0.398 | 0.257 | 1.588 | 1.590 | 0.000 | True |
| 24 | 100 | 0.998 | 1.000 | 1.014 | 1.930 | 1.933 | 0.000 | True |
| 25 | 100 | 0.700 | 0.563 | 0.378 | 1.644 | 1.644 | 0.000 | True |
| 26 | 100 | 0.961 | 0.945 | 1.204 | 2.016 | 2.018 | 0.000 | True |
| 27 | 100 | 0.372 | 0.435 | 1.675 | 2.230 | 2.230 | 0.000 | True |
| 28 | 100 | 0.986 | 0.988 | 0.905 | 1.884 | 1.880 | 0.000 | True |
| 29 | 100 | 0.245 | 0.238 | 0.148 | 1.540 | 1.540 | 0.005 | False |

## Phase 2

| branch | n | pre_index | post_index | post_price_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control | 22 | 0.828 | 0.774 | 0.855 | 0.000 | 0.000 | 0.000 | 0.289 | 0.000 | 4 | 0.000 |
| placebo | 22 | 0.828 | 0.717 | 0.790 | -0.058 | -0.158 | 0.045 | 0.203 | 0.000 | 9 | 0.000 |
| same_inherit | 22 | 0.828 | 0.790 | 0.864 | 0.016 | -0.077 | 0.122 | 0.080 | 0.000 | 6 | 0.000 |
| same_blank | 22 | 0.828 | 0.301 | 1.437 | -0.474 | -0.782 | -0.202 | 0.727 | 3.000 | 9 | 0.000 |
| other_inherit | 22 | 0.828 | 0.179 | 0.197 | -0.595 | -0.824 | -0.357 | 0.248 | 5.500 | 18 | 0.002 |
| other_blank | 22 | 0.828 | -0.284 | 0.816 | -1.058 | -1.396 | -0.713 | 1.548 | 59.500 | 10 | 0.001 |
| br_bot | 22 | 0.828 | 0.013 | 0.010 | -0.761 | -0.864 | -0.652 | 0.729 | 38.000 | 21 | 0.000 |

## Pre-registered hypotheses (docs/PREREGISTRATION.md)

| hypothesis | claim | n | estimate | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| H1 | same_inherit - control > -0.10 | 22 | 0.016 | -0.077 | 0.122 | supported |
| H2 | same_blank - control < -0.10 | 22 | -0.474 | -0.782 | -0.202 | supported |
| H3a | same_inherit - same_blank > 0 | 22 | 0.489 | 0.247 | 0.771 | supported |
| H3b | other_inherit - other_blank > 0 | 22 | 0.463 | 0.126 | 0.825 | supported |
| H4 | |si-sb| - |si-oi| > 0 | 22 | -0.121 | -0.412 | 0.192 | inconclusive |
| H6 | other_inherit - control < -0.10 | 22 | -0.595 | -0.824 | -0.357 | supported |
| H5 | no LLM responder has excess response CI > 0 (estimate = cells with CI > 0) | 13 | 0.000 | n/a | n/a | supported |
| H5c | no LLM responder has excess response above the myopic control (estimate = such cells) | 13 | 0.000 | n/a | n/a | supported |

H3 combined (H3a and H3b): supported

H5 cells (responder is an LLM):

| branch | deviator_seat | n | excess_response | ci_low | ci_high | punishes |
|---|---|---|---|---|---|---|
| br_bot | 1 | 22 | 0.147 | -0.060 | 0.349 | False |
| control | 0 | 22 | 0.113 | -0.071 | 0.290 | False |
| control | 1 | 22 | -0.209 | -0.354 | -0.027 | False |
| other_blank | 0 | 22 | -0.132 | -0.294 | 0.129 | False |
| other_blank | 1 | 22 | 0.178 | -0.063 | 0.418 | False |
| other_inherit | 0 | 22 | -0.385 | -0.428 | -0.323 | False |
| other_inherit | 1 | 22 | -0.046 | -0.235 | 0.150 | False |
| placebo | 0 | 22 | -0.146 | -0.308 | 0.037 | False |
| placebo | 1 | 22 | 0.088 | -0.109 | 0.288 | False |
| same_blank | 0 | 22 | 0.075 | -0.136 | 0.294 | False |
| same_blank | 1 | 22 | 0.117 | -0.082 | 0.332 | False |
| same_inherit | 0 | 22 | 0.053 | -0.148 | 0.261 | False |
| same_inherit | 1 | 22 | -0.075 | -0.242 | 0.100 | False |

H5c cells, excess response minus the myopic control (pre-registered for the final runs 9-12; exploratory for runs 1-8). Rows with reference True are the prompt controls:

| branch | deviator_seat | n | n_myopic | excess_minus_myopic | ci_low | ci_high | punishes | reference |
|---|---|---|---|---|---|---|---|---|
| ctrl_trigger | both | 20 | 20 | 0.638 | 0.069 | 1.220 | True | True |
| ctrl_default | both | 20 | 20 | 0.095 | -0.228 | 0.423 | False | True |
| br_bot | 1 | 22 | 20 | 0.012 | -0.302 | 0.331 | False | False |
| control | 0 | 22 | 20 | -0.022 | -0.321 | 0.284 | False | False |
| control | 1 | 22 | 20 | -0.344 | -0.626 | -0.037 | False | False |
| other_blank | 0 | 22 | 20 | -0.268 | -0.580 | 0.090 | False | False |
| other_blank | 1 | 22 | 20 | 0.043 | -0.291 | 0.388 | False | False |
| other_inherit | 0 | 22 | 20 | -0.520 | -0.763 | -0.261 | False | False |
| other_inherit | 1 | 22 | 20 | -0.181 | -0.486 | 0.138 | False | False |
| placebo | 0 | 22 | 20 | -0.281 | -0.567 | 0.026 | False | False |
| placebo | 1 | 22 | 20 | -0.047 | -0.356 | 0.272 | False | False |
| same_blank | 0 | 22 | 20 | -0.060 | -0.381 | 0.271 | False | False |
| same_blank | 1 | 22 | 20 | -0.018 | -0.326 | 0.311 | False | False |
| same_inherit | 0 | 22 | 20 | -0.082 | -0.396 | 0.241 | False | False |
| same_inherit | 1 | 22 | 20 | -0.210 | -0.498 | 0.092 | False | False |

## Secondary: price index, branch - control (post window)

| branch | n | price_index_diff | ci_low | ci_high |
|---|---|---|---|---|
| placebo | 22 | -0.065 | -0.157 | 0.029 |
| same_inherit | 22 | 0.009 | -0.080 | 0.119 |
| same_blank | 22 | 0.582 | 0.292 | 0.888 |
| other_inherit | 22 | -0.657 | -0.776 | -0.527 |
| other_blank | 22 | -0.038 | -0.484 | 0.401 |
| br_bot | 22 | -0.845 | -1.019 | -0.669 |

## Exploratory: decision agreement with control (rounds from the swap)

| branch | n | same_seat0 | same_seat1 | roots_identical | first_diff_median |
|---|---|---|---|---|---|
| placebo | 22 | 0.147 | 0.200 | 0 | 101.000 |
| same_inherit | 22 | 0.225 | 0.237 | 0 | 100.000 |
| same_blank | 22 | 0.020 | 0.021 | 0 | 100.000 |
| other_inherit | 22 | 0.022 | 0.009 | 0 | 100.000 |
| other_blank | 22 | 0.014 | 0.003 | 0 | 100.000 |
| br_bot | 22 | 0.015 | 0 | 0 | 100.000 |

## Exploratory: price dynamics per seat (rounds from the swap)

| branch | n | seat0_hold | seat0_match | seat0_abs_change | seat1_hold | seat1_match | seat1_abs_change |
|---|---|---|---|---|---|---|---|
| control | 22 | 0.900 | 0.719 | 0.004 | 0.889 | 0.712 | 0.004 |
| placebo | 22 | 0.801 | 0.681 | 0.005 | 0.864 | 0.696 | 0.003 |
| same_inherit | 22 | 0.796 | 0.652 | 0.003 | 0.844 | 0.672 | 0.002 |
| same_blank | 22 | 0.734 | 0.585 | 0.014 | 0.802 | 0.587 | 0.020 |
| other_inherit | 22 | 0.536 | 0.379 | 0.009 | 0.255 | 0.106 | 0.009 |
| other_blank | 22 | 0.571 | 0.297 | 0.022 | 0.204 | 0.092 | 0.024 |
| br_bot | 22 | 0.820 | 0.006 | 0.007 | 0.811 | 0 | 0.005 |

## Audit: controls

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 10 | 0 | 0.567 | 0.291 | 0.276 | -0.036 | 0.578 | 0.232 |
| ctrl_default | seat1:incumbent | 10 | 0 | 0.477 | 0.293 | 0.184 | -0.116 | 0.486 | 0.184 |
| ctrl_myopic | seat0:incumbent | 10 | 0 | 0.420 | 0.379 | 0.041 | -0.335 | 0.404 | 0.530 |
| ctrl_myopic | seat1:incumbent | 10 | 0 | 0.610 | 0.381 | 0.229 | -0.076 | 0.530 | 0.148 |
| ctrl_trigger | seat0:incumbent | 10 | 0 | 0.938 | 0.398 | 0.539 | -0.164 | 1.242 | -0.808 |
| ctrl_trigger | seat1:incumbent | 10 | 0 | 1.406 | 0.398 | 1.008 | 0.305 | 1.711 | -1.608 |

## Audit: deviation

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| br_bot | seat0:incumbent | 22 | 0 | 0.398 | 0.398 | 0.000 | 0.000 | 0.000 | -0.430 |
| br_bot | seat1:entrant | 22 | 0 | 0.545 | 0.398 | 0.147 | -0.060 | 0.349 | -0.836 |
| control | seat0:incumbent | 22 | 0 | 0.507 | 0.395 | 0.113 | -0.071 | 0.290 | -0.257 |
| control | seat1:incumbent | 22 | 0 | 0.186 | 0.395 | -0.209 | -0.354 | -0.027 | 0.087 |
| other_blank | seat0:incumbent | 22 | 0 | 0.146 | 0.278 | -0.132 | -0.294 | 0.129 | 0.276 |
| other_blank | seat1:entrant | 22 | 0 | 0.468 | 0.290 | 0.178 | -0.063 | 0.418 | 0.114 |
| other_inherit | seat0:incumbent | 22 | 0 | -0.005 | 0.380 | -0.385 | -0.428 | -0.323 | -0.006 |
| other_inherit | seat1:entrant | 22 | 0 | 0.332 | 0.378 | -0.046 | -0.235 | 0.150 | -0.629 |
| placebo | seat0:incumbent | 22 | 0 | 0.250 | 0.396 | -0.146 | -0.308 | 0.037 | -0.289 |
| placebo | seat1:incumbent | 22 | 0 | 0.483 | 0.395 | 0.088 | -0.109 | 0.288 | -0.521 |
| same_blank | seat0:incumbent | 22 | 0 | 0.365 | 0.290 | 0.075 | -0.136 | 0.294 | 0.726 |
| same_blank | seat1:entrant | 22 | 0 | 0.406 | 0.289 | 0.117 | -0.082 | 0.332 | 0.587 |
| same_inherit | seat0:incumbent | 22 | 0 | 0.446 | 0.394 | 0.053 | -0.148 | 0.261 | -0.332 |
| same_inherit | seat1:entrant | 22 | 0 | 0.320 | 0.395 | -0.075 | -0.242 | 0.100 | -0.398 |

## Stage timings

| stage | started_utc | seconds |
|---|---|---|
| aa | 2026-10-23T03:25:37+00:00 | 158.300 |
| controls | 2026-10-23T03:28:16+00:00 | 1263.500 |
| phase1 | 2026-10-23T03:49:20+00:00 | 2126.100 |
| select | 2026-10-23T04:24:47+00:00 | 1.000 |
| phase2 | 2026-10-23T04:24:49+00:00 | 10122.300 |
| deviation | 2026-10-23T07:13:32+00:00 | 1627.000 |
