"""Outcome from one scheduled OpportunityLab search."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class ScheduledSearchResult:
    schedule_id: str
    query: str
    opportunity_count: int = 0
    opportunities: list[dict] = field(default_factory=list)
    error: str | None = None
    completed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def succeeded(self) -> bool:
        return self.error is None

    def to_dict(self) -> dict:
        return {
            "schedule_id": self.schedule_id,
            "query": self.query,
            "opportunity_count": self.opportunity_count,
            "opportunities": list(self.opportunities),
            "error": self.error,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduledSearchResult":
        return cls(
            schedule_id=str(data.get("schedule_id", "")),
            query=str(data.get("query", "")),
            opportunity_count=int(data.get("opportunity_count", 0)),
            opportunities=list(data.get("opportunities", [])),
            error=data.get("error"),
            completed_at=str(data.get("completed_at", "")),
        )
