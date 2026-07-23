"""JSON persistence for social signals."""

from __future__ import annotations

import json
from pathlib import Path

from src.signals.social_signal import SocialSignal


class SocialSignalStore:
    def __init__(self, path: str | Path = "data/social_signals.json") -> None:
        self.path = Path(path)

    def load(self) -> list[SocialSignal]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        result = []
        for item in data:
            if isinstance(item, dict):
                try:
                    result.append(SocialSignal.from_dict(item))
                except (TypeError, ValueError):
                    pass
        return result

    def save(self, signals: list[SocialSignal]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps([item.to_dict() for item in signals], indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(self.path)
