# Code rules

1. Python ≥ 3.10, type hints, `from __future__ import annotations` in package modules.
   Exception: `modal_app.py` must not use it, because Modal reads `modal.parameter()` type hints
   at import time.
2. Keep `succession/` free of module-level imports of `vllm`, `torch`, or `modal`.
3. All randomness goes through `derive_seed` or a seeded `random.Random`. No global RNG state.
4. All run data goes through `RunStore`. Writes are atomic (temp file + `os.replace`).
5. A new stage must be resumable: load the checkpoint if it exists, then continue.
6. Add or update a test in `tests/` for every behaviour change. Tests use `MockBackend`
   and must run in under 30 seconds without a GPU or network.
7. Before a commit: `python -m pytest -q`, `ruff check .`, `ruff format --check .` all pass.
8. Do not commit run data, model weights, tokens or `.env` files. `results/` is git-ignored.
9. Pin the vLLM version in `modal_app.py`, together with `transformers` (vLLM declares only a
   lower bound; an unpinned newer release broke the tokenizer on 22 Oct). Change either only
   together with a new A/A check.
