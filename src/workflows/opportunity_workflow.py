"""Persistent checklist belonging to a tracked opportunity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.workflows.action_item import ActionItem


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OpportunityWorkflow:
    tracking_id: str
    title: str
    items: list[ActionItem] = field(default_factory=list)
    updated_at: str = field(default_factory=utc_now)

    @property
    def completed_count(self) -> int:
        return sum(item.completed for item in self.items)

    @property
    def progress_percent(self) -> int:
        if not self.items:
            return 0
        return round(self.completed_count / len(self.items) * 100)

    def touch(self) -> None:
        self.updated_at = utc_now()

    def to_dict(self) -> dict:
        return {
            "tracking_id": self.tracking_id,
            "title": self.title,
            "items": [item.to_dict() for item in self.items],
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OpportunityWorkflow":
        return cls(
            tracking_id=str(data.get("tracking_id", "")),
            title=str(data.get("title", "")),
            items=[
                ActionItem.from_dict(item)
                for item in data.get("items", [])
                if isinstance(item, dict)
            ],
            updated_at=str(data.get("updated_at") or utc_now()),
        )
