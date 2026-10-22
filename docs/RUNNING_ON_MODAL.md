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

## 3. Main run + replication, in parallel (about 3–6 hours, about $12–25)

**Sprint rule first.** The sprint starts Fri 23 Oct 2026. A run that starts before then is
pre-sprint work: disclose it in `docs/PREEXISTING_WORK.md` and in the report. A run that starts
after the sprint start counts as sprint work.

1. Write the start date into `docs/PREREGISTRATION.md` ("Status: … fixed when phase 1 of the
   main run starts"), commit and push.
2. Start both runs. Each config gets its own orchestrator; each model gets up to 2 GPU containers:

   ```bash
   modal run --detach modal_app.py --config configs/main.yaml,configs/main_mistral.yaml --stages aa,controls,phase1,select,phase2,deviation,analyze
   ```

   Run names: `main` (Qwen incumbent, primary) and `main_mistral` (Mistral incumbent, replication).

`--detach` keeps the job running when you close the terminal or the PC.
Watch progress at https://modal.com/apps or with `modal app logs cartel-succession`.

**If it stops** (timeout, error, preemption), run the same command again. Every stage
continues from its last checkpoint (every 10 rounds). A run that already finished returns
its summary again without new GPU work.

**Budget guard.** Keep the Modal workspace budget at about $30. Modal stops all runs at that limit.

## 4. Get the results

```bash
modal volume get succession-runs main ./results/
modal volume get succession-runs main_mistral ./results/
python scripts/analyze.py results/main
python scripts/analyze.py results/main_mistral
```

Outputs in `results/<run>/analysis/`: `summary.md`, `phase1_summary.json`,
`phase2_summary.json`, `deviation_audit_summary.json`, `controls_audit_summary.json`,
`phase1_trajectories.png`, `trajectories.png`, `differences.png`, and `timings.json` in the run
folder. Add both summaries to `docs/RUN_LOG.md`.

## Cost estimate

Estimates from the workload and the pilot timings (`docs/RUN_LOG.md`), not measurements.
Check the real time per round in the first phase-2 checkpoints, and current prices at
https://modal.com/pricing.

| Stage, per run | Model calls (upper bound) | Notes |
|---|---|---|
| aa | 160 | ~5 min including the first model load |
| controls (30 sessions × 60 rounds + audit) | ~5,300 | pilot: 444 s for 12 sessions |
| phase 1 (30 × 100 × 2) | 6,000 | pilot: 3–6 s per round for 4 sessions |
| phase 2 (≤210 branch sessions × 100 rounds) | ≤42,000 | the longest stage; large batches per round |
| deviation (≤840 copies × 7 rounds) | ≤11,800 | |
| **Per run** | **≤65,000** | about 2–4 h wall time, 2 GPU containers |
| **main + main_mistral** | **≤130,000** | run in parallel: about 3–6 h wall time, about 12–16 L4 hours ≈ **$12–25** |

The pilot (runs 2–3, 2 models, about 30 minutes of GPU work) cost about $0.50.

To finish faster, use a larger GPU. The cost stays about the same:
PowerShell `$env:SUCCESSION_GPU="A100-40GB"`, bash `export SUCCESSION_GPU=A100-40GB`.

## Useful commands

```bash
modal volume rm -r succession-runs pilot    # delete a run folder
modal app stop cartel-succession            # stop a running job
```
