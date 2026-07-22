"""Structured OpportunityLab search schedule."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import uuid4


@dataclass
class SearchSchedule:
    query: str
    interval_minutes: int
    source_names: list[str] = field(default_factory=list)
    enabled: bool = True
    schedule_id: str = field(default_factory=lambda: uuid4().hex)
    last_run_at: str | None = None
    next_run_at: str | None = None

    def __post_init__(self) -> None:
        self.query = self.query.strip()
        self.interval_minutes = int(self.interval_minutes)

        if not self.query:
            raise ValueError("A scheduled search requires a query.")

        if self.interval_minutes < 1:
            raise ValueError("Search interval must be at least one minute.")

        self.source_names = list(dict.fromkeys(self.source_names))

    @staticmethod
    def _utc(datetime_value: datetime) -> datetime:
        if datetime_value.tzinfo is None:
            datetime_value = datetime_value.replace(tzinfo=timezone.utc)
        return datetime_value.astimezone(timezone.utc)

    def schedule_next(self, now: datetime | None = None) -> str:
        current = self._utc(now or datetime.now(timezone.utc))
        next_run = current + timedelta(minutes=self.interval_minutes)
        self.next_run_at = next_run.isoformat()
        return self.next_run_at

    def mark_ran(self, now: datetime | None = None) -> None:
        current = self._utc(now or datetime.now(timezone.utc))
        self.last_run_at = current.isoformat()
        self.schedule_next(current)

    def is_due(self, now: datetime | None = None) -> bool:
        if not self.enabled:
            return False

        if self.next_run_at is None:
            return True

        try:
            next_run = datetime.fromisoformat(self.next_run_at)
        except ValueError:
            return True

        return self._utc(next_run) <= self._utc(
            now or datetime.now(timezone.utc)
        )

    def to_dict(self) -> dict:
        return {
            "schedule_id": self.schedule_id,
            "query": self.query,
            "interval_minutes": self.interval_minutes,
            "source_names": list(self.source_names),
            "enabled": self.enabled,
            "last_run_at": self.last_run_at,
            "next_run_at": self.next_run_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SearchSchedule":
        return cls(
            schedule_id=str(data.get("schedule_id") or uuid4().hex),
            query=str(data.get("query", "")),
            interval_minutes=int(data.get("interval_minutes", 0)),
            source_names=list(data.get("source_names", [])),
            enabled=bool(data.get("enabled", True)),
            last_run_at=data.get("last_run_at"),
            next_run_at=data.get("next_run_at"),
        )
