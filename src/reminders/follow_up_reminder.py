"""Follow-up reminder generated from a tracked opportunity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FollowUpReminder:
    tracking_id: str
    title: str
    due_date: date
    days_until: int

    @property
    def state(self) -> str:
        if self.days_until < 0:
            return "Overdue"
        if self.days_until == 0:
            return "Due today"
        return "Upcoming"
