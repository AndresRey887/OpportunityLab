"""One dated social or web signal."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class SocialSignal:
    platform: str
    title: str
    summary: str
    sentiment: str = "Neutral"
    strength: int = 3
    signal_date: str = field(default_factory=lambda: date.today().isoformat())
    source_url: str = ""
    topic_id: str = ""
    notes: str = ""
    signal_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=utc_now)

    PLATFORMS = (
        "Reddit",
        "YouTube",
        "Company Website",
        "News",
        "Forum",
        "Other",
    )
    SENTIMENTS = ("Positive", "Neutral", "Negative", "Mixed")

    def __post_init__(self) -> None:
        if self.platform not in self.PLATFORMS:
            self.platform = "Other"
        if self.sentiment not in self.SENTIMENTS:
            self.sentiment = "Neutral"
        self.strength = max(1, min(int(self.strength or 3), 5))
        self.title = str(self.title).strip()
        self.summary = str(self.summary).strip()
        if not self.title or not self.summary:
            raise ValueError("Signal title and summary are required.")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocialSignal":
        return cls(
            platform=str(data.get("platform", "Other")),
            title=str(data.get("title", "")),
            summary=str(data.get("summary", "")),
            sentiment=str(data.get("sentiment", "Neutral")),
            strength=int(data.get("strength", 3) or 3),
            signal_date=str(data.get("signal_date") or date.today().isoformat()),
            source_url=str(data.get("source_url", "")),
            topic_id=str(data.get("topic_id", "")),
            notes=str(data.get("notes", "")),
            signal_id=str(data.get("signal_id") or uuid4().hex),
            created_at=str(data.get("created_at") or utc_now()),
        )
