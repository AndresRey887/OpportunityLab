"""Saved response draft for one tracked opportunity."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OpportunityDraft:
    tracking_id: str
    title: str
    template_id: str = ""
    subject: str = ""
    body: str = ""
    updated_at: str = field(default_factory=utc_now)

    def touch(self) -> None:
        self.updated_at = utc_now()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "OpportunityDraft":
        return cls(
            tracking_id=str(data.get("tracking_id", "")),
            title=str(data.get("title", "")),
            template_id=str(data.get("template_id", "")),
            subject=str(data.get("subject", "")),
            body=str(data.get("body", "")),
            updated_at=str(data.get("updated_at") or utc_now()),
        )
