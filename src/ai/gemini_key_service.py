"""Select between primary and alternate Gemini API keys safely."""

from __future__ import annotations

import json
from pathlib import Path


class GeminiKeyService:
    PRIMARY = "Primary"
    ALTERNATE = "Alternate"
    OPTIONS = (PRIMARY, ALTERNATE)

    def __init__(
        self,
        selection_file: str | Path = "data/gemini_key_selection.json",
        primary_key: str | None = None,
        alternate_key: str | None = None,
    ) -> None:
        self.selection_file = Path(selection_file)
        configured = self._load_configured_keys()
        self._keys = {
            self.PRIMARY: self._clean_key(
                configured[self.PRIMARY]
                if primary_key is None else primary_key
            ),
            self.ALTERNATE: self._clean_key(
                configured[self.ALTERNATE]
                if alternate_key is None else alternate_key
            ),
        }
        self._selected = self._load_selection()

    @property
    def selected(self) -> str:
        return self._selected

    @property
    def active_key(self) -> str:
        return self._keys[self._selected]

    def select(self, name: str) -> str:
        if name not in self.OPTIONS:
            raise ValueError(f"Unknown Gemini key selection: {name}")
        self._selected = name
        self._save_selection()
        return self._selected

    def is_configured(self, name: str) -> bool:
        if name not in self.OPTIONS:
            raise ValueError(f"Unknown Gemini key selection: {name}")
        return bool(self._keys[name])

    def status(self) -> dict[str, object]:
        return {
            "selected": self.selected,
            "primary_configured": self.is_configured(self.PRIMARY),
            "alternate_configured": self.is_configured(self.ALTERNATE),
        }

    def _load_selection(self) -> str:
        try:
            data = json.loads(self.selection_file.read_text(encoding="utf-8"))
            selected = data.get("selected")
        except (OSError, json.JSONDecodeError, AttributeError):
            selected = None
        return selected if selected in self.OPTIONS else self.PRIMARY

    def _save_selection(self) -> None:
        self.selection_file.parent.mkdir(parents=True, exist_ok=True)
        self.selection_file.write_text(
            json.dumps({"selected": self.selected}, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _clean_key(value: object) -> str:
        return str(value or "").strip()

    @staticmethod
    def _load_configured_keys() -> dict[str, str]:
        try:
            from config import secrets
        except ImportError:
            return {
                GeminiKeyService.PRIMARY: "",
                GeminiKeyService.ALTERNATE: "",
            }
        primary = getattr(
            secrets,
            "GEMINI_API_KEY_PRIMARY",
            getattr(secrets, "GEMINI_API_KEY", ""),
        )
        alternate = getattr(secrets, "GEMINI_API_KEY_ALTERNATE", "")
        return {
            GeminiKeyService.PRIMARY: primary,
            GeminiKeyService.ALTERNATE: alternate,
        }
