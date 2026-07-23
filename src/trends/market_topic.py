"""A market topic monitored over time."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class MarketTopic:
    name: str
    category: str = "Market"
    keywords: list[str] = field(default_factory=list)
    notes: str = ""
    topic_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)

    CATEGORIES = (
        "Market",
        "Product",
        "Technology",
        "Consumer Interest",
        "Regulation",
        "Supply",
        "Competitor",
        "Other",
    )

    def __post_init__(self) -> None:
        self.name = str(self.name).strip()
        if not self.name:
            raise ValueError("Market topic name cannot be empty.")
        if self.category not in self.CATEGORIES:
            self.category = "Other"
        self.keywords = sorted({
            str(keyword).strip()
            for keyword in self.keywords
            if str(keyword).strip()
        })

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "MarketTopic":
        return cls(
            topic_id=str(data.get("topic_id") or uuid4().hex),
            name=str(data.get("name", "")),
            category=str(data.get("category", "Other")),
            keywords=list(data.get("keywords", [])),
            notes=str(data.get("notes", "")),
            created_at=str(data.get("created_at") or utc_now()),
        )
