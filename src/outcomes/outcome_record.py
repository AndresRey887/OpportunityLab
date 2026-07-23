"""Recorded result of pursuing an opportunity."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OutcomeRecord:
    tracking_id: str
    opportunity_title: str
    result: str = "Undecided"
    outcome_date: str = ""
    estimated_value: float = 0.0
    result_notes: str = ""
    lessons_learned: str = ""
    updated_at: str = field(default_factory=utc_now)

    RESULTS = (
        "Undecided",
        "Successful",
        "Unsuccessful",
        "Withdrawn",
        "Expired",
    )

    def __post_init__(self) -> None:
        if self.result not in self.RESULTS:
            self.result = "Undecided"
        try:
            self.estimated_value = max(0.0, float(self.estimated_value or 0))
        except (TypeError, ValueError):
            self.estimated_value = 0.0

    def touch(self) -> None:
        self.updated_at = utc_now()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "OutcomeRecord":
        return cls(
            tracking_id=str(data.get("tracking_id", "")),
            opportunity_title=str(data.get("opportunity_title", "")),
            result=str(data.get("result", "Undecided")),
            outcome_date=str(data.get("outcome_date", "")),
            estimated_value=data.get("estimated_value", 0),
            result_notes=str(data.get("result_notes", "")),
            lessons_learned=str(data.get("lessons_learned", "")),
            updated_at=str(data.get("updated_at") or utc_now()),
        )
