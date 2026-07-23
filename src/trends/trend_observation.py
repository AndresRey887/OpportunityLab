"""One dated market signal observation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TrendObservation:
    topic_id: str
    direction: str
    strength: int
    summary: str
    observation_date: str = field(default_factory=lambda: date.today().isoformat())
    source_title: str = ""
    source_url: str = ""
    notes: str = ""
    observation_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)

    DIRECTIONS = ("Emerging", "Rising", "Stable", "Falling", "Volatile")

    def __post_init__(self) -> None:
        if self.direction not in self.DIRECTIONS:
            self.direction = "Stable"
        self.strength = max(1, min(int(self.strength or 3), 5))
        self.summary = str(self.summary).strip()
        if not self.summary:
            raise ValueError("Trend observation summary cannot be empty.")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TrendObservation":
        return cls(
            topic_id=str(data.get("topic_id", "")),
            direction=str(data.get("direction", "Stable")),
            strength=int(data.get("strength", 3) or 3),
            summary=str(data.get("summary", "")),
            observation_date=str(
                data.get("observation_date") or date.today().isoformat()
            ),
            source_title=str(data.get("source_title", "")),
            source_url=str(data.get("source_url", "")),
            notes=str(data.get("notes", "")),
            observation_id=str(data.get("observation_id") or uuid4().hex),
            created_at=str(data.get("created_at") or utc_now()),
        )
