from __future__ import annotations

import json
from pathlib import Path
import sys


class HighScoreStore:
    def __init__(self, filename: str = "winlinez_high_score.json") -> None:
        self.path = self._data_dir() / filename

    def load(self) -> int:
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return 0

        score = payload.get("best_score", 0)
        if isinstance(score, int) and score > 0:
            return score
        return 0

    def save(self, score: int) -> None:
        if score <= 0:
            return
        payload = {"best_score": int(score)}
        try:
            self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except OSError:
            return

    def _data_dir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path.cwd()
