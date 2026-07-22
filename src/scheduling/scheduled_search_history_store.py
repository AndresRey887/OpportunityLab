"""Persistent history for scheduled-search results."""

from __future__ import annotations

import json
from pathlib import Path

from src.scheduling.scheduled_search_result import ScheduledSearchResult


class ScheduledSearchHistoryStore:
    def __init__(
        self,
        path: str | Path = "data/scheduled_search_results.json",
        maximum_results: int = 200,
    ) -> None:
        self.path = Path(path)
        self.maximum_results = max(1, int(maximum_results))

    def load(self) -> list[ScheduledSearchResult]:
        if not self.path.exists():
            return []

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        results = []
        for item in data:
            if isinstance(item, dict):
                try:
                    results.append(ScheduledSearchResult.from_dict(item))
                except (TypeError, ValueError):
                    continue
        return results

    def append(self, result: ScheduledSearchResult) -> None:
        results = self.load()
        results.append(result)
        self.save(results[-self.maximum_results:])

    def save(self, results: list[ScheduledSearchResult]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary_path.write_text(
            json.dumps(
                [result.to_dict() for result in results],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary_path.replace(self.path)

    def clear(self) -> None:
        self.save([])
