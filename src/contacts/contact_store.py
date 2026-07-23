"""JSON persistence for contacts and interaction history."""

from __future__ import annotations

import json
from pathlib import Path

from src.contacts.contact_record import ContactRecord
from src.contacts.interaction_entry import InteractionEntry


class ContactStore:
    def __init__(
        self,
        contact_path: str | Path = "data/opportunity_contacts.json",
        history_path: str | Path = "data/interaction_history.json",
    ) -> None:
        self.contact_path = Path(contact_path)
        self.history_path = Path(history_path)

    def load_contacts(self) -> list[ContactRecord]:
        return self._load(self.contact_path, ContactRecord.from_dict)

    def load_interactions(self) -> list[InteractionEntry]:
        return self._load(self.history_path, InteractionEntry.from_dict)

    def save_contacts(self, contacts: list[ContactRecord]) -> None:
        self._save(self.contact_path, [item.to_dict() for item in contacts])

    def save_interactions(self, interactions: list[InteractionEntry]) -> None:
        self._save(self.history_path, [item.to_dict() for item in interactions])

    @staticmethod
    def _load(path: Path, factory) -> list:
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        result = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                result.append(factory(item))
            except (TypeError, ValueError):
                continue
        return result

    @staticmethod
    def _save(path: Path, data: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(path.suffix + ".tmp")
        temporary_path.write_text(
            json.dumps(data, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temporary_path.replace(path)
