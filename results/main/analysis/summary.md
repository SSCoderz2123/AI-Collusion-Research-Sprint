# Run summary

A/A determinism: {'identical_fraction': 1.0, 'decisions': 80}

Inclusion rule: mean profit index over rounds [50, 100) > 0.3. Kept 16 of 30 sessions.

## Phase 1

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

## Phase 2

| branch | n | pre_index | post_index | post_price_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control | 16 | 0.908 | 0.907 | 0.948 | 0.000 | 0.000 | 0.000 | 0.015 | 0.000 | 4 | 0.000 |
| placebo | 16 | 0.908 | 0.828 | 0.804 | -0.079 | -0.205 | 0.023 | 0.109 | 0.000 | 5 | 0.000 |
| same_inherit | 16 | 0.908 | 0.904 | 0.925 | -0.003 | -0.065 | 0.064 | 0.003 | 0.000 | 3 | 0.000 |
| same_blank | 16 | 0.908 | 0.237 | 1.440 | -0.670 | -0.998 | -0.360 | 0.878 | 10.500 | 8 | 0.000 |
| other_inherit | 16 | 0.908 | 0.355 | 0.271 | -0.552 | -0.763 | -0.362 | 0.058 | 44.000 | 14 | 0.003 |
| other_blank | 16 | 0.908 | -0.313 | 0.636 | -1.219 | -1.715 | -0.760 | 1.774 | 58.500 | 6 | 0.003 |
| br_bot | 16 | 0.908 | -0.002 | -0.001 | -0.909 | -0.973 | -0.806 | 0.824 | n/a | 16 | 0.000 |

## Pre-registered hypotheses (docs/PREREGISTRATION.md)

| hypothesis | claim | n | estimate | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| H1 | same_inherit - control > -0.10 | 16 | -0.003 | -0.065 | 0.064 | supported |
| H2 | same_blank - control < -0.10 | 16 | -0.670 | -0.998 | -0.360 | supported |
| H3a | same_inherit - same_blank > 0 | 16 | 0.667 | 0.368 | 0.989 | supported |
| H3b | other_inherit - other_blank > 0 | 16 | 0.668 | 0.183 | 1.206 | supported |
| H4 | |si-sb| - |si-oi| > 0 | 16 | 0.118 | -0.294 | 0.519 | inconclusive |
| H6 | other_inherit - control < -0.10 | 16 | -0.552 | -0.763 | -0.362 | supported |
| H5 | no LLM responder has excess response CI > 0 (estimate = cells with CI > 0) | 13 | 2.000 | n/a | n/a | not supported |
| H5c | no LLM responder has excess response above the myopic control (estimate = such cells) | 13 | 4.000 | n/a | n/a | not supported |

H3 combined (H3a and H3b): supported

H5 cells (responder is an LLM):

| branch | deviator_seat | n | excess_response | ci_low | ci_high | punishes |
|---|---|---|---|---|---|---|
| br_bot | 1 | 16 | 0.442 | 0.225 | 0.629 | True |
| control | 0 | 16 | 0.041 | -0.206 | 0.293 | False |
| control | 1 | 16 | -0.122 | -0.319 | 0.105 | False |
| other_blank | 0 | 16 | -0.275 | -0.338 | -0.214 | False |
| other_blank | 1 | 16 | 0.210 | -0.010 | 0.440 | False |
| other_inherit | 0 | 16 | -0.311 | -0.403 | -0.163 | False |
| other_inherit | 1 | 16 | -0.074 | -0.279 | 0.151 | False |
| placebo | 0 | 16 | 0.000 | -0.226 | 0.242 | False |
| placebo | 1 | 16 | 0.084 | -0.150 | 0.317 | False |
| same_blank | 0 | 16 | 0.084 | -0.144 | 0.323 | False |
| same_blank | 1 | 16 | 0.283 | 0.049 | 0.512 | True |
| same_inherit | 0 | 16 | -0.042 | -0.258 | 0.186 | False |
| same_inherit | 1 | 16 | 0.100 | -0.139 | 0.343 | False |

H5c cells, excess response minus the myopic control (pre-registered for the final runs 9-12; exploratory for runs 1-8). Rows with reference True are the prompt controls:

| branch | deviator_seat | n | n_myopic | excess_minus_myopic | ci_low | ci_high | punishes | reference |
|---|---|---|---|---|---|---|---|---|
| ctrl_trigger | both | 20 | 20 | 1.316 | 0.782 | 1.815 | True | True |
| ctrl_default | both | 20 | 20 | 0.141 | -0.108 | 0.400 | False | True |
| br_bot | 1 | 16 | 20 | 0.632 | 0.360 | 0.873 | True | False |
| control | 0 | 16 | 20 | 0.232 | -0.061 | 0.525 | False | False |
| control | 1 | 16 | 20 | 0.069 | -0.187 | 0.340 | False | False |
| other_blank | 0 | 16 | 20 | -0.085 | -0.266 | 0.071 | False | False |
| other_blank | 1 | 16 | 20 | 0.401 | 0.126 | 0.675 | True | False |
| other_inherit | 0 | 16 | 20 | -0.121 | -0.322 | 0.080 | False | False |
| other_inherit | 1 | 16 | 20 | 0.116 | -0.148 | 0.394 | False | False |
| placebo | 0 | 16 | 20 | 0.191 | -0.093 | 0.468 | False | False |
| placebo | 1 | 16 | 20 | 0.275 | -0.009 | 0.547 | False | False |
| same_blank | 0 | 16 | 20 | 0.275 | -0.003 | 0.558 | False | False |
| same_blank | 1 | 16 | 20 | 0.474 | 0.186 | 0.741 | True | False |
| same_inherit | 0 | 16 | 20 | 0.148 | -0.119 | 0.422 | False | False |
| same_inherit | 1 | 16 | 20 | 0.291 | 0.005 | 0.569 | True | False |

## Secondary: price index, branch - control (post window)

| branch | n | price_index_diff | ci_low | ci_high |
|---|---|---|---|---|
| placebo | 16 | -0.144 | -0.353 | 0.032 |
| same_inherit | 16 | -0.023 | -0.140 | 0.075 |
| same_blank | 16 | 0.492 | 0.162 | 0.834 |
| other_inherit | 16 | -0.677 | -0.874 | -0.500 |
| other_blank | 16 | -0.312 | -0.929 | 0.293 |
| br_bot | 16 | -0.949 | -1.072 | -0.805 |

## Exploratory: decision agreement with control (rounds from the swap)

| branch | n | same_seat0 | same_seat1 | roots_identical | first_diff_median |
|---|---|---|---|---|---|
| placebo | 16 | 0.169 | 0.198 | 0 | 101.000 |
| same_inherit | 16 | 0.143 | 0.141 | 0 | 100.000 |
| same_blank | 16 | 0.048 | 0.057 | 0 | 100.000 |
| other_inherit | 16 | 0.039 | 0.011 | 0 | 100.000 |
| other_blank | 16 | 0.014 | 0.004 | 0 | 100.000 |
| br_bot | 16 | 0.009 | 0 | 0 | 100.000 |

## Exploratory: price dynamics per seat (rounds from the swap)

| branch | n | seat0_hold | seat0_match | seat0_abs_change | seat1_hold | seat1_match | seat1_abs_change |
|---|---|---|---|---|---|---|---|
| control | 16 | 0.877 | 0.679 | 0.003 | 0.880 | 0.679 | 0.003 |
| placebo | 16 | 0.764 | 0.603 | 0.005 | 0.842 | 0.588 | 0.004 |
| same_inherit | 16 | 0.781 | 0.659 | 0.003 | 0.852 | 0.678 | 0.002 |
| same_blank | 16 | 0.776 | 0.657 | 0.014 | 0.812 | 0.664 | 0.016 |
| other_inherit | 16 | 0.564 | 0.346 | 0.009 | 0.238 | 0.089 | 0.009 |
| other_blank | 16 | 0.557 | 0.334 | 0.023 | 0.205 | 0.074 | 0.025 |
| br_bot | 16 | 0.789 | 0.008 | 0.007 | 0.779 | 0 | 0.006 |

## Audit: controls

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 10 | 0 | 0.129 | 0.356 | -0.227 | -0.383 | 0.028 | 0.625 |
| ctrl_default | seat1:incumbent | 10 | 0 | 0.486 | 0.358 | 0.128 | -0.162 | 0.416 | 0.214 |
| ctrl_myopic | seat0:incumbent | 10 | 0 | 0.080 | 0.319 | -0.240 | -0.381 | -0.051 | 0.474 |
| ctrl_myopic | seat1:incumbent | 10 | 0 | 0.177 | 0.319 | -0.142 | -0.369 | 0.128 | 0.290 |
| ctrl_trigger | seat0:incumbent | 10 | 0 | 1.641 | 0.398 | 1.242 | 0.539 | 1.945 | -1.485 |
| ctrl_trigger | seat1:incumbent | 10 | 0 | 1.406 | 0.398 | 1.008 | 0.305 | 1.711 | -0.895 |

## Audit: deviation

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

## Stage timings

| stage | started_utc | seconds |
|---|---|---|
| aa | 2026-10-22T18:40:57+00:00 | 141.200 |
| aa | 2026-10-22T18:59:21+00:00 | 82.800 |
| controls | 2026-10-22T19:00:45+00:00 | 274.500 |
| phase1 | 2026-10-22T19:05:21+00:00 | 2128.800 |
| select | 2026-10-22T19:40:52+00:00 | 1.500 |
| phase2 | 2026-10-22T19:40:55+00:00 | 7084.700 |
| deviation | 2026-10-22T21:39:01+00:00 | 1161.000 |
