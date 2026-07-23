"""One dated interaction with an opportunity contact."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class InteractionEntry:
    tracking_id: str
    interaction_type: str
    summary: str
    interaction_date: str = field(default_factory=lambda: date.today().isoformat())
    entry_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)

    TYPES = ("Email", "Phone", "Meeting", "Application", "Note", "Other")

    def __post_init__(self) -> None:
        self.interaction_type = str(self.interaction_type).strip()
        self.summary = str(self.summary).strip()
        self.interaction_date = str(self.interaction_date).strip()
        if self.interaction_type not in self.TYPES:
            self.interaction_type = "Other"
        if not self.summary:
            raise ValueError("Interaction summary cannot be empty.")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "InteractionEntry":
        return cls(
            tracking_id=str(data.get("tracking_id", "")),
            interaction_type=str(data.get("interaction_type", "Other")),
            summary=str(data.get("summary", "")),
            interaction_date=str(data.get("interaction_date") or date.today().isoformat()),
            entry_id=str(data.get("entry_id") or uuid4().hex),
            created_at=str(data.get("created_at") or utc_now()),
        )
