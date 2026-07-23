"""Saved intelligence about a company or organisation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CompanyProfile:
    name: str
    domain: str = ""
    website: str = ""
    description: str = ""
    industry: str = ""
    location: str = ""
    email: str = ""
    phone: str = ""
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    linked_tracking_ids: list[str] = field(default_factory=list)
    company_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.name = str(self.name).strip() or "Unknown Organisation"
        self.domain = str(self.domain).strip().casefold()
        self.tags = sorted({
            str(tag).strip()
            for tag in self.tags
            if str(tag).strip()
        })
        self.linked_tracking_ids = list(dict.fromkeys(
            str(value) for value in self.linked_tracking_ids if value
        ))

    def touch(self) -> None:
        self.updated_at = utc_now()

    def link(self, tracking_id: str) -> bool:
        tracking_id = str(tracking_id).strip()
        if not tracking_id or tracking_id in self.linked_tracking_ids:
            return False
        self.linked_tracking_ids.append(tracking_id)
        self.touch()
        return True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CompanyProfile":
        return cls(
            company_id=str(data.get("company_id") or uuid4().hex),
            name=str(data.get("name", "")),
            domain=str(data.get("domain", "")),
            website=str(data.get("website", "")),
            description=str(data.get("description", "")),
            industry=str(data.get("industry", "")),
            location=str(data.get("location", "")),
            email=str(data.get("email", "")),
            phone=str(data.get("phone", "")),
            notes=str(data.get("notes", "")),
            tags=list(data.get("tags", [])),
            linked_tracking_ids=list(data.get("linked_tracking_ids", [])),
            created_at=str(data.get("created_at") or utc_now()),
            updated_at=str(data.get("updated_at") or utc_now()),
        )

    @staticmethod
    def id_for_domain(domain: str) -> str:
        return sha256(str(domain).casefold().encode("utf-8")).hexdigest()
