"""Experiment configuration, loaded from a YAML file in configs/."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

from succession.market import MarketParams


@dataclass
class ModelSpec:
    """One LLM that the generator serves."""

    name: str  # short label used in data files, e.g. "qwen7b"
    hf_id: str  # Hugging Face model id
    max_model_len: int = 4096
    gpu_memory_utilization: float = 0.90
    dtype: str = "auto"
    quantization: str | None = None


@dataclass
class SamplingSpec:
    temperature: float = 0.7
    top_p: float = 1.0
    max_tokens: int = 160


@dataclass
class Phase1Spec:
    n_sessions: int = 20
    rounds: int = 100
    # Pre-registered inclusion rule: keep a session when the mean profit
    # index of both firms over rounds [select_from, rounds) exceeds threshold.
    select_from: int = 50
    select_threshold: float = 0.3


@dataclass
class Phase2Spec:
    rounds: int = 100  # rounds after the swap
    branches: list[str] = field(
        default_factory=lambda: [
            "control",
            "placebo",
            "same_inherit",
            "same_blank",
            "other_inherit",
            "other_blank",
            "br_bot",
        ]
    )
    swap_seat: int = 1  # 0-based seat that is replaced
    announce: bool = True  # incumbent receives a notice in placebo and swap branches


@dataclass
class ControlsSpec:
    n_per_variant: int = 4  # sessions per prompt variant (default, myopic, trigger)
    rounds: int = 60


@dataclass
class DeviationSpec:
    enabled: bool = True
    cut: float = 0.10  # forced price cut as a fraction of the deviator's last price
    horizon: int = 6  # rounds simulated after the deviation round
    discount: float = 0.95
    deviator_seats: list[int] = field(default_factory=lambda: [0, 1])


@dataclass
class ExperimentConfig:
    name: str = "succession_main"
    seed: int = 20261023
    history_window: int = 30
    prompt_variant: str = "default"
    price_min: float = 0.0
    price_max: float = 10.0
    incumbent_model: ModelSpec = field(
        default_factory=lambda: ModelSpec(name="qwen7b", hf_id="Qwen/Qwen2.5-7B-Instruct")
    )
    other_model: ModelSpec = field(
        default_factory=lambda: ModelSpec(name="mistral7b", hf_id="mistralai/Mistral-7B-Instruct-v0.3")
    )
    sampling: SamplingSpec = field(default_factory=SamplingSpec)
    market: MarketParams = field(default_factory=MarketParams)
    phase1: Phase1Spec = field(default_factory=Phase1Spec)
    phase2: Phase2Spec = field(default_factory=Phase2Spec)
    deviation: DeviationSpec = field(default_factory=DeviationSpec)
    controls: ControlsSpec = field(default_factory=ControlsSpec)
    checkpoint_every: int = 10

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> ExperimentConfig:
        data = dict(data)
        sub = {
            "incumbent_model": ModelSpec,
            "other_model": ModelSpec,
            "sampling": SamplingSpec,
            "market": MarketParams,
            "phase1": Phase1Spec,
            "phase2": Phase2Spec,
            "deviation": DeviationSpec,
            "controls": ControlsSpec,
        }
        for key, klass in sub.items():
            if key in data and isinstance(data[key], dict):
                data[key] = klass(**data[key])
        return cls(**data)


def load_config(path: str | Path) -> ExperimentConfig:
    with open(path, encoding="utf-8") as fh:
        return ExperimentConfig.from_dict(yaml.safe_load(fh) or {})
