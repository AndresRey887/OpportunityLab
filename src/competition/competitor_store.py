"""JSON persistence for competitor relationships."""

from __future__ import annotations

import json
from pathlib import Path

from src.competition.competitor_link import CompetitorLink


class CompetitorStore:
    def __init__(
        self,
        path: str | Path = "data/company_competitors.json",
    ) -> None:
        self.path = Path(path)

    def load(self) -> list[CompetitorLink]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        links = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                links.append(CompetitorLink.from_dict(item))
            except (TypeError, ValueError):
                continue
        return links

    def save(self, links: list[CompetitorLink]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                [link.to_dict() for link in links],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary.replace(self.path)
