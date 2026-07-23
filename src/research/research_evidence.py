"""One sourced piece of company research evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ResearchEvidence:
    company_id: str
    category: str
    claim: str
    source_url: str = ""
    source_title: str = ""
    evidence_date: str = field(default_factory=lambda: date.today().isoformat())
    confidence: int = 3
    notes: str = ""
    evidence_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)

    CATEGORIES = (
        "Company Overview",
        "Product",
        "Market",
        "Competitor",
        "Social Signal",
        "Product Launch",
        "Risk",
        "Contact",
        "Other",
    )

    def __post_init__(self) -> None:
        self.category = str(self.category).strip()
        if self.category not in self.CATEGORIES:
            self.category = "Other"
        self.claim = str(self.claim).strip()
        if not self.claim:
            raise ValueError("Research claim cannot be empty.")
        self.confidence = max(1, min(int(self.confidence or 3), 5))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ResearchEvidence":
        return cls(
            company_id=str(data.get("company_id", "")),
            category=str(data.get("category", "Other")),
            claim=str(data.get("claim", "")),
            source_url=str(data.get("source_url", "")),
            source_title=str(data.get("source_title", "")),
            evidence_date=str(
                data.get("evidence_date") or date.today().isoformat()
            ),
            confidence=int(data.get("confidence", 3) or 3),
            notes=str(data.get("notes", "")),
            evidence_id=str(data.get("evidence_id") or uuid4().hex),
            created_at=str(data.get("created_at") or utc_now()),
        )
