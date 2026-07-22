"""Outcome from one scheduled OpportunityLab search."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduledSearchResult:
    schedule_id: str
    query: str
    opportunity_count: int = 0
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None
