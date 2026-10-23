# Run summary

A/A determinism: {'identical_fraction': 1.0, 'decisions': 80}

Inclusion rule: mean profit index over rounds [50, 100) > 0.3. Kept 24 of 30 sessions.

## Phase 1

| root_id | rounds | index_select_window | index_last10 | price_index_last10 | price_seat0_last10 | price_seat1_last10 | parse_failure_rate | kept |
|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 0.985 | 0.976 | 0.864 | 1.865 | 1.862 | 0.000 | True |
| 1 | 100 | 0.980 | 0.991 | 1.081 | 1.960 | 1.963 | 0.000 | True |
| 2 | 100 | 0.902 | 0.907 | 1.265 | 2.042 | 2.048 | 0.000 | True |
| 3 | 100 | -0.541 | -0.366 | 2.157 | 2.449 | 2.447 | 0.000 | False |
| 4 | 100 | 0.263 | 0.262 | 0.165 | 1.545 | 1.550 | 0.000 | False |
| 5 | 100 | 0.999 | 0.999 | 0.977 | 1.919 | 1.910 | 0.000 | True |
| 6 | 100 | 0.996 | 0.991 | 0.915 | 1.888 | 1.885 | 0.000 | True |
| 7 | 100 | 0.981 | 0.972 | 0.852 | 1.857 | 1.860 | 0.000 | True |
| 8 | 100 | 0.997 | 0.996 | 0.944 | 1.900 | 1.899 | 0.000 | True |
| 9 | 100 | -1.032 | -0.873 | 2.493 | 2.600 | 2.600 | 0.000 | False |
| 10 | 100 | 0.641 | 0.680 | 1.498 | 2.150 | 2.150 | 0.000 | True |
| 11 | 100 | -0.475 | -0.374 | 2.161 | 2.450 | 2.450 | 0.000 | False |
| 12 | 100 | 0.996 | 0.996 | 1.053 | 1.950 | 1.948 | 0.000 | True |
| 13 | 100 | 0.993 | 0.985 | 0.892 | 1.870 | 1.882 | 0.000 | True |
| 14 | 100 | 0.945 | 0.937 | 0.777 | 1.820 | 1.828 | 0.000 | True |
| 15 | 100 | 0.927 | 0.919 | 0.746 | 1.810 | 1.810 | 0.000 | True |
| 16 | 100 | 0.983 | 0.980 | 0.874 | 1.870 | 1.866 | 0.000 | True |
| 17 | 100 | 0.990 | 0.986 | 0.897 | 1.879 | 1.878 | 0.000 | True |
| 18 | 100 | -0.206 | -0.237 | -0.139 | 1.410 | 1.410 | 0.000 | False |
| 19 | 100 | -0.291 | -0.295 | 2.114 | 2.427 | 2.430 | 0.000 | False |
| 20 | 100 | 0.961 | 0.955 | 0.811 | 1.839 | 1.840 | 0.000 | True |
| 21 | 100 | 0.979 | 0.975 | 0.861 | 1.858 | 1.866 | 0.000 | True |
| 22 | 100 | 0.998 | 0.994 | 0.936 | 1.894 | 1.898 | 0.000 | True |
| 23 | 100 | 0.995 | 0.986 | 0.895 | 1.879 | 1.876 | 0.000 | True |
| 24 | 100 | 0.373 | 0.432 | 1.677 | 2.230 | 2.232 | 0.000 | True |
| 25 | 100 | 0.961 | 0.961 | 0.824 | 1.851 | 1.840 | 0.000 | True |
| 26 | 100 | 0.996 | 0.996 | 0.945 | 1.900 | 1.900 | 0.000 | True |
| 27 | 100 | 0.964 | 0.927 | 0.760 | 1.821 | 1.812 | 0.000 | True |
| 28 | 100 | 0.980 | 0.976 | 1.134 | 1.980 | 1.991 | 0.000 | True |
| 29 | 100 | 0.838 | 0.858 | 0.659 | 1.770 | 1.772 | 0.000 | True |

## Phase 2

| branch | n | pre_index | post_index | post_price_index | diff_vs_control | diff_ci_low | diff_ci_high | dip_depth | half_life_median | never_recovered | parse_failure_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control | 24 | 0.934 | 0.934 | 0.919 | 0.000 | 0.000 | 0.000 | 0.009 | 0.000 | 4 | 0.000 |
| placebo | 24 | 0.934 | 0.934 | 0.910 | -0.001 | -0.022 | 0.015 | 0.010 | 0.000 | 1 | 0.000 |
| same_inherit | 24 | 0.934 | 0.936 | 0.922 | 0.002 | -0.014 | 0.016 | 0.014 | 0.000 | 3 | 0.000 |
| same_blank | 24 | 0.934 | 0.431 | 1.256 | -0.504 | -0.850 | -0.208 | 1.157 | 2.000 | 8 | 0.000 |
| other_inherit | 24 | 0.934 | 0.156 | 0.140 | -0.778 | -0.947 | -0.596 | 0.090 | 0.000 | 22 | 0.003 |
| other_blank | 24 | 0.934 | -0.274 | 0.806 | -1.208 | -1.716 | -0.805 | 1.336 | 38.000 | 11 | 0.003 |
| br_bot | 24 | 0.934 | 0.029 | 0.030 | -0.905 | -0.951 | -0.835 | 0.788 | 89.000 | 23 | 0.001 |

## Pre-registered hypotheses (docs/PREREGISTRATION.md)

| hypothesis | claim | n | estimate | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| H1 | same_inherit - control > -0.10 | 24 | 0.002 | -0.014 | 0.016 | supported |
| H2 | same_blank - control < -0.10 | 24 | -0.504 | -0.850 | -0.208 | supported |
| H3a | same_inherit - same_blank > 0 | 24 | 0.505 | 0.209 | 0.853 | supported |
| H3b | other_inherit - other_blank > 0 | 24 | 0.430 | 0.012 | 0.926 | supported |
| H4 | |si-sb| - |si-oi| > 0 | 24 | -0.274 | -0.628 | 0.097 | inconclusive |
| H6 | other_inherit - control < -0.10 | 24 | -0.778 | -0.947 | -0.596 | supported |
| H5 | no LLM responder has excess response CI > 0 (estimate = cells with CI > 0) | 13 | 1.000 | n/a | n/a | not supported |
| H5c | no LLM responder has excess response above the myopic control (estimate = such cells) | 13 | 0.000 | n/a | n/a | supported |

H3 combined (H3a and H3b): supported

H5 cells (responder is an LLM):

| branch | deviator_seat | n | excess_response | ci_low | ci_high | punishes |
|---|---|---|---|---|---|---|
| br_bot | 1 | 24 | 0.069 | -0.118 | 0.265 | False |
| control | 0 | 24 | 0.022 | -0.177 | 0.233 | False |
| control | 1 | 24 | 0.111 | -0.074 | 0.305 | False |
| other_blank | 0 | 23 | -0.010 | -0.370 | 0.617 | False |
| other_blank | 1 | 24 | 0.175 | -0.073 | 0.446 | False |
| other_inherit | 0 | 24 | -0.311 | -0.375 | -0.223 | False |
| other_inherit | 1 | 24 | 0.160 | -0.039 | 0.361 | False |
| placebo | 0 | 24 | -0.098 | -0.267 | 0.091 | False |
| placebo | 1 | 24 | 0.145 | -0.056 | 0.349 | False |
| same_blank | 0 | 24 | -0.051 | -0.220 | 0.130 | False |
| same_blank | 1 | 24 | 0.223 | 0.009 | 0.429 | True |
| same_inherit | 0 | 24 | 0.077 | -0.114 | 0.270 | False |
| same_inherit | 1 | 24 | -0.006 | -0.196 | 0.194 | False |

H5c cells, excess response minus the myopic control (pre-registered for the final runs 9-12; exploratory for runs 1-8). Rows with reference True are the prompt controls:

| branch | deviator_seat | n | n_myopic | excess_minus_myopic | ci_low | ci_high | punishes | reference |
|---|---|---|---|---|---|---|---|---|
| ctrl_trigger | both | 20 | 20 | 1.044 | 0.507 | 1.554 | True | True |
| ctrl_default | both | 20 | 20 | -0.107 | -0.416 | 0.203 | False | True |
| br_bot | 1 | 24 | 20 | -0.129 | -0.427 | 0.173 | False | False |
| control | 0 | 24 | 20 | -0.176 | -0.480 | 0.121 | False | False |
| control | 1 | 24 | 20 | -0.087 | -0.381 | 0.207 | False | False |
| other_blank | 0 | 23 | 20 | -0.208 | -0.682 | 0.486 | False | False |
| other_blank | 1 | 24 | 20 | -0.023 | -0.365 | 0.322 | False | False |
| other_inherit | 0 | 24 | 20 | -0.509 | -0.749 | -0.273 | False | False |
| other_inherit | 1 | 24 | 20 | -0.038 | -0.347 | 0.268 | False | False |
| placebo | 0 | 24 | 20 | -0.296 | -0.589 | -0.005 | False | False |
| placebo | 1 | 24 | 20 | -0.053 | -0.365 | 0.243 | False | False |
| same_blank | 0 | 24 | 20 | -0.249 | -0.540 | 0.034 | False | False |
| same_blank | 1 | 24 | 20 | 0.025 | -0.281 | 0.330 | False | False |
| same_inherit | 0 | 24 | 20 | -0.121 | -0.419 | 0.168 | False | False |
| same_inherit | 1 | 24 | 20 | -0.204 | -0.504 | 0.093 | False | False |

## Secondary: price index, branch - control (post window)

| branch | n | price_index_diff | ci_low | ci_high |
|---|---|---|---|---|
| placebo | 24 | -0.009 | -0.037 | 0.018 |
| same_inherit | 24 | 0.003 | -0.027 | 0.032 |
| same_blank | 24 | 0.337 | 0.036 | 0.663 |
| other_inherit | 24 | -0.779 | -0.862 | -0.691 |
| other_blank | 24 | -0.113 | -0.643 | 0.428 |
| br_bot | 24 | -0.889 | -0.966 | -0.823 |

## Exploratory: decision agreement with control (rounds from the swap)

| branch | n | same_seat0 | same_seat1 | roots_identical | first_diff_median |
|---|---|---|---|---|---|
| placebo | 24 | 0.479 | 0.460 | 2 | 119.500 |
| same_inherit | 24 | 0.326 | 0.271 | 0 | 102.000 |
| same_blank | 24 | 0.079 | 0.063 | 0 | 100.000 |
| other_inherit | 24 | 0.055 | 0.004 | 0 | 100.000 |
| other_blank | 24 | 0.032 | 0.006 | 0 | 100.000 |
| br_bot | 24 | 0.043 | 0 | 0 | 100.000 |

## Exploratory: price dynamics per seat (rounds from the swap)

| branch | n | seat0_hold | seat0_match | seat0_abs_change | seat1_hold | seat1_match | seat1_abs_change |
|---|---|---|---|---|---|---|---|
| control | 24 | 0.885 | 0.745 | 0.002 | 0.889 | 0.750 | 0.002 |
| placebo | 24 | 0.891 | 0.756 | 0.002 | 0.901 | 0.767 | 0.002 |
| same_inherit | 24 | 0.895 | 0.747 | 0.002 | 0.888 | 0.758 | 0.002 |
| same_blank | 24 | 0.840 | 0.598 | 0.019 | 0.832 | 0.585 | 0.023 |
| other_inherit | 24 | 0.678 | 0.289 | 0.007 | 0.216 | 0.072 | 0.009 |
| other_blank | 24 | 0.670 | 0.250 | 0.019 | 0.191 | 0.070 | 0.027 |
| br_bot | 24 | 0.863 | 0.004 | 0.007 | 0.854 | 0 | 0.005 |

## Audit: controls

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| ctrl_default | seat0:incumbent | 10 | 0 | 0.474 | 0.392 | 0.081 | -0.208 | 0.373 | -0.118 |
| ctrl_default | seat1:incumbent | 10 | 0 | 0.493 | 0.391 | 0.102 | -0.192 | 0.397 | -0.216 |
| ctrl_myopic | seat0:incumbent | 10 | 0 | 0.408 | 0.312 | 0.096 | -0.217 | 0.432 | 0.319 |
| ctrl_myopic | seat1:incumbent | 10 | 0 | 0.615 | 0.315 | 0.300 | -0.014 | 0.607 | 0.035 |
| ctrl_trigger | seat0:incumbent | 10 | 0 | 1.641 | 0.398 | 1.242 | 0.539 | 1.945 | -1.824 |
| ctrl_trigger | seat1:incumbent | 10 | 0 | 1.641 | 0.398 | 1.242 | 0.539 | 1.945 | -2.140 |

## Audit: deviation

| branch | deviator | n | n_invalid | response | br_benchmark | excess_response | excess_ci_low | excess_ci_high | deviator_gain |
|---|---|---|---|---|---|---|---|---|---|
| br_bot | seat0:incumbent | 24 | 0 | 0.399 | 0.399 | 0.000 | 0.000 | 0.000 | -0.555 |
| br_bot | seat1:entrant | 24 | 0 | 0.467 | 0.399 | 0.069 | -0.118 | 0.265 | -0.825 |
| control | seat0:incumbent | 24 | 0 | 0.426 | 0.404 | 0.022 | -0.177 | 0.233 | -0.417 |
| control | seat1:incumbent | 24 | 0 | 0.515 | 0.404 | 0.111 | -0.074 | 0.305 | -0.343 |
| other_blank | seat0:incumbent | 23 | 1 | 0.268 | 0.278 | -0.010 | -0.370 | 0.617 | 0.599 |
| other_blank | seat1:entrant | 24 | 0 | 0.466 | 0.290 | 0.175 | -0.073 | 0.446 | 0.153 |
| other_inherit | seat0:incumbent | 24 | 0 | 0.066 | 0.378 | -0.311 | -0.375 | -0.223 | -0.339 |
| other_inherit | seat1:entrant | 24 | 0 | 0.536 | 0.375 | 0.160 | -0.039 | 0.361 | -0.649 |
| placebo | seat0:incumbent | 24 | 0 | 0.306 | 0.404 | -0.098 | -0.267 | 0.091 | 0.444 |
| placebo | seat1:incumbent | 24 | 0 | 0.549 | 0.404 | 0.145 | -0.056 | 0.349 | -0.261 |
| same_blank | seat0:incumbent | 24 | 0 | 0.272 | 0.323 | -0.051 | -0.220 | 0.130 | 0.446 |
| same_blank | seat1:entrant | 24 | 0 | 0.546 | 0.323 | 0.223 | 0.009 | 0.429 | 0.267 |
| same_inherit | seat0:incumbent | 24 | 0 | 0.480 | 0.403 | 0.077 | -0.114 | 0.270 | -0.155 |
| same_inherit | seat1:entrant | 24 | 0 | 0.397 | 0.404 | -0.006 | -0.196 | 0.194 | -0.232 |

## Stage timings

| stage | started_utc | seconds |
|---|---|---|
| aa | 2026-10-23T03:25:38+00:00 | 145.800 |
| controls | 2026-10-23T03:28:05+00:00 | 1246.300 |
| phase1 | 2026-10-23T03:48:52+00:00 | 2140.200 |
| select | 2026-10-23T04:24:33+00:00 | 1.100 |
| phase2 | 2026-10-23T04:24:35+00:00 | 10067.400 |
| deviation | 2026-10-23T07:12:23+00:00 | 1656.000 |
