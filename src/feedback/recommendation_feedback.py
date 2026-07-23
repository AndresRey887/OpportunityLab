"""Saved helpful or unhelpful recommendation feedback."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class RecommendationFeedback:
    opportunity_key: str
    title: str
    source: str
    keywords: list[str]
    helpful: bool
    notes: str = ""
    feedback_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RecommendationFeedback":
        return cls(
            opportunity_key=str(data.get("opportunity_key", "")),
            title=str(data.get("title", "")),
            source=str(data.get("source", "")),
            keywords=[
                str(value) for value in data.get("keywords", [])
                if value
            ],
            helpful=bool(data.get("helpful", False)),
            notes=str(data.get("notes", "")),
            feedback_id=str(data.get("feedback_id") or uuid4().hex),
            created_at=str(data.get("created_at") or utc_now()),
        )

    @staticmethod
    def key_for(opportunity) -> str:
        identity = (
            str(getattr(opportunity, "url", "")).strip().casefold()
            or str(getattr(opportunity, "title", "")).strip().casefold()
        )
        return sha256(identity.encode("utf-8")).hexdigest()
