import pytest

import succession.hypotheses


@pytest.fixture(autouse=True)
def fewer_bootstrap_resamples(monkeypatch):
    """10,000 resamples per test make the suite slower than the 30 s limit (.claude/rules/code.md).
    The tests check verdict logic on clearly separated data, so 2,000 resamples are enough.
    The environment variable reaches the scripts that tests start as subprocesses."""
    monkeypatch.setattr(succession.hypotheses, "N_BOOT", 2000)
    monkeypatch.setenv("SUCCESSION_TEST_N_BOOT", "2000")
