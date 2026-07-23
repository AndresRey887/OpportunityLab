"""JSON persistence for permanent opportunity timelines."""

from __future__ import annotations

import json
from pathlib import Path

from src.timeline.timeline_event import TimelineEvent


class TimelineStore:
    def __init__(self, path: str | Path = "data/opportunity_timeline.json") -> None:
        self.path = Path(path)

    def load(self) -> list[TimelineEvent]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        events = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                events.append(TimelineEvent.from_dict(item))
            except (TypeError, ValueError):
                continue
        return events

    def save(self, events: list[TimelineEvent]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                [event.to_dict() for event in events],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary.replace(self.path)
