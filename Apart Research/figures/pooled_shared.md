# Pooled: results/main, results/main_r2, results/main_olmo, results/final_main (--shared: branches without the other model; exploratory)

| hypothesis | claim | n | estimate | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| H1 | same_inherit - control > -0.10 | 92 | 0.053 | -0.011 | 0.148 | supported |
| H2 | same_blank - control < -0.10 | 92 | -0.592 | -0.751 | -0.432 | supported |
| H3a | same_inherit - same_blank > 0 | 92 | 0.645 | 0.503 | 0.793 | supported |
| H3b | other_inherit - other_blank > 0 | 0 | n/a | n/a | n/a | no data |
| H4 | |si-sb| - |si-oi| > 0 | 0 | n/a | n/a | n/a | no data |
| H6 | other_inherit - control < -0.10 | 0 | n/a | n/a | n/a | no data |
| H5 | no LLM responder has excess response CI > 0 (estimate = cells with CI > 0) | 9 | 2.000 | n/a | n/a | not supported |
| H5c | no LLM responder has excess response above the myopic control (estimate = such cells) | 9 | 0.000 | n/a | n/a | supported |

H3 combined: no data

| branch | n | price_index_diff | ci_low | ci_high |
|---|---|---|---|---|
| placebo | 92 | -0.023 | -0.111 | 0.065 |
| same_inherit | 92 | 0.024 | -0.029 | 0.091 |
| same_blank | 92 | 0.487 | 0.306 | 0.667 |
| br_bot | 92 | -0.818 | -0.896 | -0.732 |

H5c cells, excess response minus the myopic control:

| branch | deviator_seat | n | n_myopic | excess_minus_myopic | ci_low | ci_high | punishes | reference |
|---|---|---|---|---|---|---|---|---|
| ctrl_trigger | both | 118 | 120 | 0.633 | 0.392 | 0.868 | True | True |
| ctrl_default | both | 120 | 120 | -0.028 | -0.155 | 0.098 | False | True |
| br_bot | 1 | 92 | 120 | 0.120 | -0.015 | 0.250 | False | False |
| control | 0 | 92 | 120 | -0.053 | -0.186 | 0.081 | False | False |
| control | 1 | 92 | 120 | -0.155 | -0.280 | -0.025 | False | False |
| placebo | 0 | 92 | 120 | -0.177 | -0.308 | -0.051 | False | False |
| placebo | 1 | 92 | 120 | -0.031 | -0.161 | 0.103 | False | False |
| same_blank | 0 | 92 | 120 | -0.018 | -0.153 | 0.114 | False | False |
| same_blank | 1 | 92 | 120 | 0.122 | -0.013 | 0.255 | False | False |
| same_inherit | 0 | 92 | 120 | -0.061 | -0.191 | 0.069 | False | False |
| same_inherit | 1 | 92 | 120 | -0.025 | -0.158 | 0.106 | False | False |

