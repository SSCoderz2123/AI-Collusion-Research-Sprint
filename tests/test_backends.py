import json

import pytest

from succession.backends import ModalBackend
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


def test_modal_backend_fails_fast_when_generator_hangs():
    """Regression: a Generator that crashes at startup must not stall the run for 12 h."""
    s, samp = specs()
    backend = ModalBackend(fake_generator(True), s, samp, call_timeout=0.01)
    with pytest.raises(RuntimeError, match="gave no reply"):
        backend.generate_batches({"a": (["p"], [1])})
