"""JSON persistence for opportunity outcomes."""

from __future__ import annotations

import json
from pathlib import Path

from src.outcomes.outcome_record import OutcomeRecord


class OutcomeStore:
    def __init__(self, path: str | Path = "data/opportunity_outcomes.json") -> None:
        self.path = Path(path)

    def load(self) -> list[OutcomeRecord]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        records = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                records.append(OutcomeRecord.from_dict(item))
            except (TypeError, ValueError):
                continue
        return records

    def save(self, records: list[OutcomeRecord]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                [record.to_dict() for record in records],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary.replace(self.path)
