"""Persistent tracked opportunity record."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TrackedOpportunity:
    title: str
    url: str
    snippet: str = ""
    source: str = ""
    score: int = 0
    status: str = "New"
    rating: int = 0
    notes: str = ""
    follow_up_date: str = ""
    tracking_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    STATUSES = ("New", "Reviewing", "Applied", "Watching", "Closed")

    def __post_init__(self) -> None:
        self.title = str(self.title).strip()
        self.url = str(self.url).strip()
        self.score = max(0, min(int(self.score or 0), 100))
        self.rating = max(0, min(int(self.rating or 0), 5))

        if self.status not in self.STATUSES:
            self.status = "New"

    @classmethod
    def from_opportunity(cls, opportunity) -> "TrackedOpportunity":
        url = str(getattr(opportunity, "url", "")).strip()
        tracking_id = (
            sha256(url.casefold().encode("utf-8")).hexdigest()
            if url
            else uuid4().hex
        )
        return cls(
            tracking_id=tracking_id,
            title=str(getattr(opportunity, "title", "")),
            url=url,
            snippet=str(getattr(opportunity, "snippet", "")),
            source=str(getattr(opportunity, "source", "")),
            score=int(getattr(opportunity, "score", 0) or 0),
        )

    def touch(self) -> None:
        self.updated_at = utc_now()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TrackedOpportunity":
        allowed = {
            field_name
            for field_name in cls.__dataclass_fields__
        }
        return cls(**{
            key: value
            for key, value in data.items()
            if key in allowed
        })
