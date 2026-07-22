"""JSON storage for scheduled OpportunityLab searches."""

from __future__ import annotations

import json
from pathlib import Path

from src.scheduling.search_schedule import SearchSchedule


class SearchScheduleStore:
    def __init__(self, path: str | Path = "data/search_schedules.json") -> None:
        self.path = Path(path)

    def load(self) -> list[SearchSchedule]:
        if not self.path.exists():
            return []

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        schedules = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                schedules.append(SearchSchedule.from_dict(item))
            except (TypeError, ValueError):
                continue

        return schedules

    def save(self, schedules: list[SearchSchedule]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary_path.write_text(
            json.dumps(
                [schedule.to_dict() for schedule in schedules],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary_path.replace(self.path)
