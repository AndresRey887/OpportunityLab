"""A saved competitor relationship between two companies."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CompetitorLink:
    company_id: str
    competitor_company_id: str
    market_overlap: str = ""
    strength: int = 3
    notes: str = ""
    link_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.company_id == self.competitor_company_id:
            raise ValueError("A company cannot compete with itself.")
        self.strength = max(1, min(int(self.strength or 3), 5))
        self.market_overlap = str(self.market_overlap).strip()
        self.notes = str(self.notes).strip()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CompetitorLink":
        return cls(
            company_id=str(data.get("company_id", "")),
            competitor_company_id=str(data.get("competitor_company_id", "")),
            market_overlap=str(data.get("market_overlap", "")),
            strength=int(data.get("strength", 3) or 3),
            notes=str(data.get("notes", "")),
            link_id=str(data.get("link_id") or uuid4().hex),
            created_at=str(data.get("created_at") or utc_now()),
        )
