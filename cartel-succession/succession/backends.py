"""Text-generation backends.

All backends implement generate_batches(): one call per round with the
prompts for every model. A request carries an explicit sampling seed, so
two copies of a session that see the same prompt get the same reply
(on vLLM; the A/A stage checks this).
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Protocol

from succession.config import ModelSpec, SamplingSpec

# model name -> (prompts, seeds)
Batches = dict[str, tuple[list[str], list[int]]]


class Backend(Protocol):
    def generate_batches(self, batches: Batches) -> dict[str, list[str]]: ...


def derive_seed(*parts: object) -> int:
    """Stable 31-bit seed from any parts (independent of PYTHONHASHSEED)."""
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(digest[:4], "big") & 0x7FFFFFFF


# --------------------------------------------------------------------- mock
_LAST_RIVAL = re.compile(r"other firm's price (\d+\.\d+)")


class MockBackend:
    """Deterministic stand-in for tests and dry runs. No GPU, no network.

    Rule: match the other firm's last price, plus a small seeded step.
    The step is positive on average, so prices drift upward like a cartel.
    """

    def __init__(self, start_price: float = 1.6, drift: float = 0.02) -> None:
        self.start_price = start_price
        self.drift = drift
        self.calls = 0

    def generate_batches(self, batches: Batches) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for model, (prompts, seeds) in batches.items():
            replies = []
            for prompt, seed in zip(prompts, seeds, strict=True):
                self.calls += 1
                found = _LAST_RIVAL.findall(prompt)
                base = float(found[-1]) if found else self.start_price
                step = ((seed % 1000) / 1000.0 - 0.3) * self.drift
                price = min(base + step, 2.4)
                replies.append(json.dumps({"notes": f"mock {model}", "price": round(price, 3)}))
            out[model] = replies
        return out


# --------------------------------------------------------------------- vLLM
def template_date(fmt: str) -> str:
    """Fixed date for chat templates that print today's date (Granite: strftime_now).

    Without it, a run that crosses midnight UTC changes the prompt text halfway, and a rerun
    cannot reproduce it. 23 Oct 2026 = sprint start. The Qwen2.5 and OLMo-2 templates do not
    use the date, so their prompts do not change (checked with transformers 4.51.3)."""
    from datetime import date

    return date(2026, 10, 23).strftime(fmt)


class VLLMEngine:
    """One vLLM engine for one model. Used locally and inside Modal."""

    def __init__(self, spec: ModelSpec, sampling: SamplingSpec) -> None:
        import os

        # Per-request seeds are required for paired branches (see modal_app.py). Set before import.
        os.environ.setdefault("VLLM_USE_V1", "0")
        from vllm import LLM  # imported here so tests run without vLLM

        self.spec = spec
        self.sampling = sampling
        kwargs = dict(
            model=spec.hf_id,
            max_model_len=spec.max_model_len,
            gpu_memory_utilization=spec.gpu_memory_utilization,
            dtype=spec.dtype,
            enable_prefix_caching=True,
        )
        if spec.quantization:
            kwargs["quantization"] = spec.quantization
        self.llm = LLM(**kwargs)
        self.tokenizer = self.llm.get_tokenizer()

    def generate(self, prompts: list[str], seeds: list[int]) -> list[str]:
        from vllm import SamplingParams

        texts = [
            self.tokenizer.apply_chat_template(
                [{"role": "user", "content": p}],
                tokenize=False,
                add_generation_prompt=True,
                strftime_now=template_date,
            )
            for p in prompts
        ]
        params = [
            SamplingParams(
                temperature=self.sampling.temperature,
                top_p=self.sampling.top_p,
                max_tokens=self.sampling.max_tokens,
                seed=s,
            )
            for s in seeds
        ]
        outputs = self.llm.generate(texts, params, use_tqdm=False)
        return [o.outputs[0].text for o in outputs]


class LocalVLLMBackend:
    """Runs every model on the local GPU. Engines load on first use.

    Two 7B models in fp16 do not fit on an 8 GB card. For local tests use one
    model, or AWQ checkpoints with a low gpu_memory_utilization each.
    """

    def __init__(self, specs: list[ModelSpec], sampling: SamplingSpec) -> None:
        self.specs = {s.name: s for s in specs}
        self.sampling = sampling
        self.engines: dict[str, VLLMEngine] = {}

    def generate_batches(self, batches: Batches) -> dict[str, list[str]]:
        out = {}
        for model, (prompts, seeds) in batches.items():
            if model not in self.engines:
                self.engines[model] = VLLMEngine(self.specs[model], self.sampling)
            out[model] = self.engines[model].generate(prompts, seeds)
        return out


class ModalBackend:
    """Sends each model's batch to Modal GPU containers, all models in parallel.

    generator_cls is the Modal class defined in modal_app.py. Each model gets
    its own container pool, so two 7B models never share one GPU. A batch larger
    than chunk_size is split into chunks that run in parallel containers; the
    replies come back in the original order. A model with spec.gpu set runs on
    that GPU type (for example a 14B model on an L40S).
    """

    def __init__(
        self,
        generator_cls,
        specs: list[ModelSpec],
        sampling: SamplingSpec,
        call_timeout: float = 1800.0,
        chunk_size: int | None = None,
    ) -> None:
        self.call_timeout = call_timeout
        self.chunk_size = chunk_size
        self.handles = {}
        for s in specs:
            cls = generator_cls.with_options(gpu=s.gpu) if s.gpu else generator_cls
            self.handles[s.name] = cls(spec_json=json.dumps(s.__dict__), sampling_json=json.dumps(sampling.__dict__))

    def _chunks(self, n: int) -> list[tuple[int, int]]:
        size = self.chunk_size if self.chunk_size and self.chunk_size > 0 else max(n, 1)
        return [(lo, min(lo + size, n)) for lo in range(0, n, size)]

    def generate_batches(self, batches: Batches) -> dict[str, list[str]]:
        calls = {
            model: [
                self.handles[model].generate.spawn(prompts[lo:hi], seeds[lo:hi])
                for lo, hi in self._chunks(len(prompts))
            ]
            for model, (prompts, seeds) in batches.items()
            if prompts
        }
        # Fail fast: if a Generator crashes at startup, Modal restarts it and the call would
        # otherwise wait until the 12 h orchestrator timeout while GPU time is billed.
        # 30 min covers the first weight download (~15 GB) plus the largest phase-2 batch.
        from modal.exception import TimeoutError as ModalTimeoutError  # not a builtin subclass

        out = {model: [] for model, (prompts, _) in batches.items() if not prompts}
        for model, chunk_calls in calls.items():
            replies: list[str] = []
            for call in chunk_calls:
                try:
                    replies += call.get(timeout=self.call_timeout)
                except (TimeoutError, ModalTimeoutError) as exc:
                    raise RuntimeError(
                        f"Generator for '{model}' gave no reply in {self.call_timeout} s. "
                        "Check the Generator logs on modal.com; the run resumes from its last checkpoint."
                    ) from exc
            out[model] = replies
        return out
