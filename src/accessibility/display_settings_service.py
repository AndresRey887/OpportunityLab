"""Persist the user's preferred OpportunityLab interface scale."""

from __future__ import annotations

import json
from pathlib import Path


class DisplaySettingsService:
    LEVELS = {
        "Normal": 1.0,
        "Large": 1.18,
        "Extra Large": 1.35,
    }

    def __init__(
        self,
        storage_file: str | Path = "data/display_settings.json",
    ) -> None:
        self.storage_file = Path(storage_file)
        self._selected = self._load()

    @property
    def selected(self) -> str:
        return self._selected

    @property
    def scale(self) -> float:
        return self.LEVELS[self._selected]

    def select(self, name: str) -> float:
        if name not in self.LEVELS:
            raise ValueError(f"Unknown text size: {name}")
        self._selected = name
        self._save()
        return self.scale

    def _load(self) -> str:
        try:
            data = json.loads(self.storage_file.read_text(encoding="utf-8"))
            selected = data.get("text_size")
        except (OSError, json.JSONDecodeError, AttributeError):
            selected = None
        return selected if selected in self.LEVELS else "Normal"

    def _save(self) -> None:
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.storage_file.write_text(
            json.dumps({"text_size": self.selected}, indent=2),
            encoding="utf-8",
        )
