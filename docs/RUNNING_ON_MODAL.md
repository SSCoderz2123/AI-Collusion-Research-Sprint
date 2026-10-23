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

## 5. Sprint runs 6–8, in parallel (about 3–5 hours)

Three runs, one orchestrator each; each model got up to 3 GPU containers (peak: 3 Qwen,
2 Mistral, 1 OLMo-2 = 6 L4s). The limit is now 8 per model (section 6). The first OLMo-2 start downloads about 15 GB of weights.

```bash
git checkout main
git pull
modal run --detach modal_app.py --config configs/main_r2.yaml,configs/main_olmo.yaml,configs/main_noannounce.yaml --stages aa,controls,phase1,select,phase2,deviation,analyze
```

Check after about 5 minutes: https://modal.com/apps shows `cartel-succession` running. Then
the laptop can be shut down.

Cost: each run has the same workload as run 4. Read the real cost of runs 4–5 on the Modal
billing page and multiply by about 1.5. Set the workspace budget above that.

Results, in the morning:

```bash
modal volume get succession-runs main_r2 ./results/
modal volume get succession-runs main_olmo ./results/
modal volume get succession-runs main_noannounce ./results/
python scripts/analyze.py results/main_r2
python scripts/analyze.py results/main_olmo
python scripts/analyze.py results/main_noannounce
python scripts/pool.py results/main results/main_r2
```

## 6. Final runs 9–12, in parallel (the last experiment)

Four runs, one orchestrator each (`docs/PREREGISTRATION.md`, "Final runs 9–12"):

| Run name | Config | Models |
|---|---|---|
| `final_main` | `configs/final_main.yaml` | Qwen2.5-7B incumbent, Mistral-7B entrant |
| `final_olmo` | `configs/final_olmo.yaml` | Qwen2.5-7B incumbent, OLMo-2-7B entrant |
| `final_granite` | `configs/final_granite.yaml` | Qwen2.5-7B incumbent, Granite-3.1-8B entrant (new download, about 16 GB) |
| `final_qwen14b` | `configs/final_qwen14b.yaml` | Qwen2.5-14B incumbent on an L40S (new download, about 30 GB), Mistral-7B entrant |

**Containers.** Each model has its own pool of at most `SUCCESSION_MAX_GPUS` containers
(default 8). Five models → at most 40 GPU containers, plus 4 CPU orchestrators = 44, below a
limit of 100. Each round's batch is split into chunks of `SUCCESSION_CHUNK` prompts (default 64),
which run in parallel containers.

1. Get the latest code:

   ```powershell
   git checkout main
   git pull
   python -m pytest -q
   ```

2. Check the two new models first (about 10–15 minutes, about $1). Each smoke config runs the
   new model as the incumbent for 2 sessions × 10 rounds. Both run in parallel, and the weights
   stay in the cache for step 3:

   ```powershell
   modal run modal_app.py --config configs/smoke_granite.yaml,configs/smoke_qwen14b.yaml --stages aa,phase1,select,analyze
   ```

   Pass condition for each: an A/A line, a phase-1 table, and `parse_failure_rate` below 0.05.
   Paste both summaries here before step 3. If one model fails, start the other three runs.

3. Start all four runs:

   ```powershell
   modal run --detach modal_app.py --config configs/final_main.yaml,configs/final_olmo.yaml,configs/final_granite.yaml,configs/final_qwen14b.yaml --stages aa,controls,phase1,select,phase2,deviation,analyze
   ```

   Optional, more parallel GPUs (set before the command, same PowerShell window):
   `$env:SUCCESSION_MAX_GPUS="12"` (5 models × 12 = 60 GPUs). Do not go above 19.

4. Check after about 10 minutes: https://modal.com/apps shows `cartel-succession` with
   several Generator containers. Then the PC can be shut down. If a run stops, run the same
   command again; every stage continues from its last checkpoint.

**Cost.** Each 7B run has about twice the workload of run 6 (more sessions, one more branch,
three times the prompt controls). Request de-duplication removes part of that. Read the cost of
runs 6–8 on the Modal billing page: plan about 2× one of those runs for each 7B run and about
5× for `final_qwen14b` (L40S price and a slower model). Set the workspace budget above the sum.

**Results:**

```powershell
modal volume get succession-runs final_main ./results/
modal volume get succession-runs final_olmo ./results/
modal volume get succession-runs final_granite ./results/
modal volume get succession-runs final_qwen14b ./results/
python scripts/analyze.py results/final_main > summary_final_main.txt
python scripts/analyze.py results/final_olmo > summary_final_olmo.txt
python scripts/analyze.py results/final_granite > summary_final_granite.txt
python scripts/analyze.py results/final_qwen14b > summary_final_qwen14b.txt
python scripts/pool.py --shared results/main results/main_r2 results/main_olmo results/final_main results/final_olmo results/final_granite > summary_pooled_shared.txt
```

## 6b. Re-analyze runs 4–8 with the new tables (no GPU, a few minutes)

The new analysis adds exploratory tables (H5c, decision agreement, price dynamics) to the old runs:

```powershell
python scripts/analyze.py results/main > summary_main_v2.txt
python scripts/analyze.py results/main_r2 > summary_main_r2_v2.txt
python scripts/analyze.py results/main_olmo > summary_main_olmo_v2.txt
python scripts/analyze.py results/main_noannounce > summary_main_noannounce_v2.txt
python scripts/pool.py --shared results/main results/main_r2 results/main_olmo > summary_pooled_shared_4_6_7.txt
python scripts/inspect_replies.py results/main_olmo other_inherit --seat 1 --roots 3 --rounds 4 > olmo_replies.txt
python scripts/inspect_replies.py results/main_olmo other_inherit --seat 1 --roots 2 --rounds 3 --start 193 >> olmo_replies.txt
```

## 7. Exploratory 3D figures (no GPU, $0)

Run on your PC after `git pull`, for the runs already in `./results/`:

```powershell
python scripts/plot_behavior.py results/final_main results/final_olmo results/main_r2 results/main_olmo results/main_noannounce results/main results/final_qwen14b
```

For each run, the script writes four files into `results/<run>/analysis/`:

| File | Content |
|---|---|
| `price_paths_3d.png` | Mean price path per branch, from 10 rounds before the swap: round × incumbent price index × entrant-seat price index. Grey base plane with a shadow of each path |
| `price_path_pca_3d.png` | One point per session: PCA of its post-swap price path (both seats), coloured by branch, with shadows on the base plane |
| `behavior_price_paths.json` | The values in the first figure |
| `behavior_pca.json` | The PCA coordinates and the explained-variance ratios |

Label both figures "exploratory" in the report: they were defined after the runs had been seen.

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
