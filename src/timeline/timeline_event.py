"""One chronological event in an opportunity timeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TimelineEvent:
    tracking_id: str
    event_type: str
    title: str
    details: str = ""
    event_at: str = field(default_factory=utc_now)
    event_id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        self.event_type = str(self.event_type).strip() or "Activity"
        self.title = str(self.title).strip()
        self.details = str(self.details).strip()
        if not self.title:
            raise ValueError("Timeline event title cannot be empty.")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TimelineEvent":
        return cls(
            tracking_id=str(data.get("tracking_id", "")),
            event_type=str(data.get("event_type", "Activity")),
            title=str(data.get("title", "")),
            details=str(data.get("details", "")),
            event_at=str(data.get("event_at") or utc_now()),
            event_id=str(data.get("event_id") or uuid4().hex),
        )
