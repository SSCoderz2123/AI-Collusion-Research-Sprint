# Running on Modal

All commands run on your PC (Windows PowerShell, macOS or Linux) from the repository root.
The GPU work runs on Modal. Your PC only sends the job and receives the summary.

## 1. One-time setup (about 15 minutes)

1. Claim the $50 sprint credit with the form in the organizers' email (valid until 1 Nov 2026).
2. Install the client and log in:

   ```bash
   pip install -r requirements.txt
   python -m modal setup          # opens a browser tab; approve, then close it
   ```

3. Get access to the gated Mistral model:
   1. Open https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3 and accept the licence.
   2. Create a read token at https://huggingface.co/settings/tokens.
   3. Store it in Modal:

      ```bash
      modal secret create huggingface HF_TOKEN=hf_your_token_here
      ```

   No token? Use an ungated second family. Set `other_model.hf_id` to
   `allenai/OLMo-2-1124-7B-Instruct` in the config, and run without the secret:
   PowerShell `$env:SUCCESSION_HF_SECRET=""`, bash `export SUCCESSION_HF_SECRET=""`.

4. Check the pipeline on your PC, without a GPU (about 10 seconds):

   ```bash
   python -m pytest -q
   python scripts/run_local.py --backend mock --config configs/pilot.yaml
   ```

## 2. Pilot (about 20–30 minutes, about $1)

```bash
modal run modal_app.py --config configs/pilot.yaml --stages aa,phase1,select,analyze
```

The first start downloads about 15 GB of weights into the Volume `succession-hf-cache`.
Later starts read from that cache.

Check the printed summary:

| Check | Pass condition | If it fails |
|---|---|---|
| A/A `identical_fraction` | ≥ 0.9 | Report the value. Pairing is weaker; the design stays valid. |
| Kept sessions | ≥ 2 of 4 reach index > 0.3 | Try the other family as incumbent (swap the two model blocks in the config), then pilot again. |
| Parse failures | < 5% | Raise `sampling.max_tokens` to 256. |

To re-run a pilot with a changed config, use a new run name, because stages resume from
saved data:

```bash
modal run modal_app.py --config configs/pilot.yaml --run pilot2 --stages aa,phase1,select,analyze
```

## 2b. Pilot phase 2 (about 20–30 minutes, about $1–2)

Tests the second model, the `huggingface` secret, and the controls, phase-2 and deviation stages:

```bash
modal run modal_app.py --config configs/pilot.yaml --stages controls,phase2,deviation,analyze
```

Record each run in `docs/RUN_LOG.md`.

## 3. Main run (about 4–6 hours wall time, about $8–15)

Fill in the date in `docs/PREREGISTRATION.md`, commit, then start:

```bash
modal run --detach modal_app.py --config configs/main.yaml --stages controls,phase1,select,phase2,deviation,analyze
```

`--detach` keeps the job running when you close the terminal or the PC.
Watch progress at https://modal.com/apps or with `modal app logs cartel-succession`.

**If it stops** (timeout, error, preemption), run the same command again. Every stage
continues from its last checkpoint (every 10 rounds).

## 4. Get the results

```bash
modal volume ls succession-runs main
modal volume get succession-runs main ./results/
python scripts/analyze.py results/main
```

Outputs in `results/main/analysis/`: `summary.md`, `phase2_summary.json`,
`deviation_audit_summary.json`, `controls_audit_summary.json`, `trajectories.png`,
`differences.png`.

## Cost estimate

These are estimates from the workload, not measurements. Read the real seconds per round
from the pilot logs, and check current prices at https://modal.com/pricing.

| Stage | Requests | L4 time (estimate) |
|---|---|---|
| controls (12 sessions × 60 rounds + audit) | ~2,000 | 0.3 h |
| phase 1 (20 × 100 × 2) | 4,000 | 0.4 h |
| phase 2 (≤140 branch sessions × 100 rounds) | ≤26,000 | 2.5–3 h per GPU, 2 GPUs in parallel |
| audit (≤560 copies × 7 rounds) | ≤7,000 | 0.5 h per GPU |
| model loading | – | ~0.3 h |
| **Total** | **≤40,000** | **~8–10 L4 hours ≈ $8–15** |

To finish faster, use a larger GPU. The cost stays about the same:
PowerShell `$env:SUCCESSION_GPU="A100-40GB"`, bash `export SUCCESSION_GPU=A100-40GB`.

## Useful commands

```bash
modal volume rm -r succession-runs pilot    # delete a run folder
modal app stop cartel-succession            # stop a running job
```
