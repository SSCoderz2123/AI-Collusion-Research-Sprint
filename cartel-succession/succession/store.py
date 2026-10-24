"""Save and load sessions. Works on a local folder or a mounted Modal Volume."""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from pathlib import Path

from succession.session import Session


class RunStore:
    def __init__(self, root: str | Path, commit: Callable[[], None] | None = None) -> None:
        """root: run folder. commit: called after each write (Modal Volume commit)."""
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._commit = commit

    def path(self, name: str) -> Path:
        return self.root / name

    def commit(self) -> None:
        if self._commit is not None:
            self._commit()

    def save_json(self, name: str, data) -> None:
        target = self.path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        os.replace(tmp, target)  # atomic: a crash never leaves half a file
        self.commit()

    def load_json(self, name: str):
        with open(self.path(name), encoding="utf-8") as fh:
            return json.load(fh)

    def exists(self, name: str) -> bool:
        return self.path(name).exists()

    def save_sessions(self, name: str, sessions: list[Session]) -> None:
        self.save_json(name, [s.to_dict() for s in sessions])

    def load_sessions(self, name: str) -> list[Session]:
        return [Session.from_dict(d) for d in self.load_json(name)]
