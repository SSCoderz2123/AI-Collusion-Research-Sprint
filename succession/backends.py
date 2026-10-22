"""Text-generation backends.

All backends implement generate_batches(): one call per round with the
prompts for every model. A request carries an explicit sampling seed, so
two copies of a session that see the same prompt get the same reply
(on vLLM; see docs/DESIGN.md for the determinism check).
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
                [{"role": "user", "content": p}], tokenize=False, add_generation_prompt=True
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
    """Sends each model's batch to a Modal GPU container, all models in parallel.

    generator_cls is the Modal class defined in modal_app.py. Each model gets
    its own container, so two 7B models never share one GPU.
    """

    def __init__(self, generator_cls, specs: list[ModelSpec], sampling: SamplingSpec) -> None:
        self.handles = {
            s.name: generator_cls(spec_json=json.dumps(s.__dict__), sampling_json=json.dumps(sampling.__dict__))
            for s in specs
        }

    def generate_batches(self, batches: Batches) -> dict[str, list[str]]:
        calls = {
            model: self.handles[model].generate.spawn(prompts, seeds)
            for model, (prompts, seeds) in batches.items()
            if prompts
        }
        return {model: call.get() for model, call in calls.items()}
