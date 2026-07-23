"""Contact details belonging to a tracked opportunity."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ContactRecord:
    tracking_id: str
    opportunity_title: str
    contact_name: str = ""
    organisation: str = ""
    email: str = ""
    phone: str = ""
    website: str = ""
    notes: str = ""
    updated_at: str = field(default_factory=utc_now)

    def touch(self) -> None:
        self.updated_at = utc_now()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ContactRecord":
        return cls(
            tracking_id=str(data.get("tracking_id", "")),
            opportunity_title=str(data.get("opportunity_title", "")),
            contact_name=str(data.get("contact_name", "")),
            organisation=str(data.get("organisation", "")),
            email=str(data.get("email", "")),
            phone=str(data.get("phone", "")),
            website=str(data.get("website", "")),
            notes=str(data.get("notes", "")),
            updated_at=str(data.get("updated_at") or utc_now()),
        )
