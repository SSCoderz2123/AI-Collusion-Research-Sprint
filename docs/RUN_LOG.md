# Run log

One entry per Modal run. Numbers come from the run output or from `results/<run>/analysis/`.
Do not type a number that is not in one of those sources.

## Status

| Check | Status |
|---|---|
| Modal account, payment method, credit | Done (22 Oct) |
| GPU image builds (vLLM 0.8.5, transformers 4.51.3) | Pass (22 Oct, run 2) |
| Qwen2.5-7B Generator starts on L4 | Pass |
| A/A determinism (pilot) | Pass: identical_fraction 1.0 |
| Pilot inclusion rule | Pass: 3 of 4 sessions kept (pass condition ≥ 2) |
| Mistral-7B Generator + `huggingface` secret | **Not tested yet** (pilot phase 2) |
| Stages controls, phase2, deviation on GPU | **Not tested yet** (pilot phase 2) |
| Main run | Not started |

## Run 1: pilot, 22 Oct 2026 (failed)

- App: `cartel-succession`. Config: `configs/pilot.yaml`. Run name: `pilot`.
- First try: stopped by Modal: "Please add a payment method to use L4 GPU functions." Fixed by
  adding a payment method.
- Second try: every Generator start failed with
  `AttributeError: Qwen2Tokenizer has no attribute all_special_tokens_extended`.
  Cause: unpinned `transformers` (vLLM 0.8.5 declares only a lower bound). Fixed in PR #2
  (pin `transformers==4.51.3`, 30-minute fail-fast on GPU calls).

## Run 2: pilot, 22 Oct 2026 (pass)

- Modal app run: `ap-5J7FVa5v5LA4ERoyt96eSQ`. GPU: L4. Stages: `aa,phase1,select,analyze`.
- Pre-sprint setup test: the sprint starts 23 Oct. These results do not go into the report as
  findings (see `docs/PREEXISTING_WORK.md`).

### Timeline (UTC, from the run output)

| Time | Event |
|---|---|
| 14:32:39 | stage `aa` starts; Generator (Qwen2.5-7B-Instruct) container starts |
| 14:33:13 | vLLM V0 engine initialises (v0.8.5, bfloat16, max_seq_len 4096, prefix caching on) |
| 14:34:42 | weights downloaded: 84.8 s |
| 14:34:48 | model loaded: 14.25 GiB, 91.3 s in total |
| 14:35:18 | engine ready (profile, KV cache, warm-up 29.4 s) |
| 14:36:41 | A/A result: identical_fraction 1.0, 80 decisions |
| 14:37:13 – 14:41:22 | phase 1: checkpoints at rounds 10, 20, 30, 40, 50, 60 |
| 14:41:24 | select: kept 3 of 4 sessions |
| 14:41:28 | app completed |

### Measurements from the log

| Quantity | Value |
|---|---|
| L4 memory available to vLLM | 22.06 GiB × 0.90 = 19.86 GiB |
| KV cache | 4.15 GiB (4850 blocks) |
| Maximum concurrency at 4096 tokens per request | 18.95 |
| Phase 1, rounds 0–30 (8 requests per round) | about 3.2 s per round |
| Phase 1, rounds 30–60 (full 30-round history) | about 6.1 s per round |
| Generator cold start to first reply | about 2 min 40 s |

### Pass conditions (`docs/RUNNING_ON_MODAL.md`)

| Condition | Required | Result |
|---|---|---|
| A/A identical_fraction | ≥ 0.9 | 1.0 |
| Sessions kept | ≥ 2 of 4 | 3 of 4 |
| Parse failures | < 5% | Not shown in the run-2 summary. Download the run and run `scripts/analyze.py` (step below). |

### Not checked by run 2

- The second model family (Mistral-7B, gated) and the `huggingface` secret.
- Stages `controls`, `phase2`, `deviation` on a real GPU.
- Per-session profit index and parse-failure rate. Run 2 used the old summary, which did not
  print them. The analysis now prints a phase-1 table and a stage-timing table.

### Next step

Run phase 2 of the same pilot (same run name; the config is unchanged, so the run continues):

```
modal run modal_app.py --config configs/pilot.yaml --stages controls,phase2,deviation,analyze
modal volume get succession-runs pilot ./results/
python scripts/analyze.py results/pilot
```

Then add the summary to this log as run 3.
