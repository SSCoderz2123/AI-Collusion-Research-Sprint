import json

import pytest

from succession.backends import ModalBackend, template_date
from succession.config import ModelSpec, SamplingSpec


class FakeCall:
    def __init__(self, result=None, hang=False):
        self.result, self.hang = result, hang

    def get(self, timeout=None):
        if self.hang:
            raise TimeoutError()
        return self.result


class FakeMethod:
    def __init__(self, hang):
        self.hang = hang

    def spawn(self, prompts, seeds):
        return FakeCall([json.dumps({"price": 1.8})] * len(prompts), self.hang)


def fake_generator(hang):
    class Gen:
        def __init__(self, spec_json, sampling_json):
            self.generate = FakeMethod(hang)

    return Gen


def specs():
    return [ModelSpec(name="a", hf_id="x/a")], SamplingSpec()


def test_modal_backend_returns_replies():
    s, samp = specs()
    out = ModalBackend(fake_generator(False), s, samp).generate_batches({"a": (["p1", "p2"], [1, 2])})
    assert len(out["a"]) == 2


def test_modal_backend_splits_batches_into_chunks_in_order():
    sent = []

    class Echo:
        def spawn(self, prompts, seeds):
            sent.append(list(prompts))
            return FakeCall([f"reply to {p}" for p in prompts])

    class Gen:
        def __init__(self, spec_json, sampling_json):
            self.generate = Echo()

    s, samp = specs()
    prompts = [f"p{i}" for i in range(10)]
    out = ModalBackend(Gen, s, samp, chunk_size=4).generate_batches({"a": (prompts, list(range(10)))})
    assert [len(c) for c in sent] == [4, 4, 2]
    assert out["a"] == [f"reply to {p}" for p in prompts]


def test_modal_backend_uses_the_gpu_of_the_model_spec():
    chosen = []

    class Gen:
        def __init__(self, spec_json, sampling_json):
            self.gpu = json.loads(spec_json)["gpu"]

        @classmethod
        def with_options(cls, gpu):
            chosen.append(gpu)
            return cls

    specs_ = [ModelSpec(name="small", hf_id="x/s"), ModelSpec(name="big", hf_id="x/b", gpu="L40S")]
    backend = ModalBackend(Gen, specs_, SamplingSpec())
    assert chosen == ["L40S"] and backend.handles["big"].gpu == "L40S" and backend.handles["small"].gpu is None


def test_modal_backend_fails_fast_when_generator_hangs():
    """Regression: a Generator that crashes at startup must not stall the run for 12 h."""
    s, samp = specs()
    backend = ModalBackend(fake_generator(True), s, samp, call_timeout=0.01)
    with pytest.raises(RuntimeError, match="gave no reply"):
        backend.generate_batches({"a": (["p"], [1])})


def test_chat_template_date_is_fixed():
    """Granite's template prints today's date; the engine passes this fixed date instead."""
    assert template_date("%B %d, %Y") == "October 23, 2026"
