"""Persist pairs the user confirmed are not related."""

from __future__ import annotations

import json
from pathlib import Path


class DuplicateDecisionStore:
    def __init__(
        self,
        path: str | Path = "data/duplicate_decisions.json",
    ) -> None:
        self.path = Path(path)

    def load_ignored(self) -> set[str]:
        if not self.path.exists():
            return set()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return set()
        if not isinstance(data, dict):
            return set()
        values = data.get("ignored_pairs", [])
        if not isinstance(values, list):
            return set()
        return {str(value) for value in values if value}

    def save_ignored(self, ignored_pairs: set[str]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                {"ignored_pairs": sorted(ignored_pairs)},
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary.replace(self.path)
