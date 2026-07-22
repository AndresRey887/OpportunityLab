"""Execute OpportunityLab searches that are due."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.scheduling.scheduled_search_history_store import (
    ScheduledSearchHistoryStore,
)
from src.scheduling.scheduled_search_result import ScheduledSearchResult
from src.scheduling.search_scheduler import SearchScheduler


class ScheduledSearchRunner:
    def __init__(
        self,
        scheduler: SearchScheduler,
        search_service: Any,
        history_store: ScheduledSearchHistoryStore | None = None,
    ) -> None:
        self.scheduler = scheduler
        self.search_service = search_service
        self.history_store = history_store or ScheduledSearchHistoryStore()
        self.last_results: list[ScheduledSearchResult] = []

    @staticmethod
    def _opportunity_summary(opportunity: Any) -> dict:
        return {
            "title": str(getattr(opportunity, "title", "")),
            "url": str(getattr(opportunity, "url", "")),
            "snippet": str(getattr(opportunity, "snippet", "")),
            "source": str(getattr(opportunity, "source", "")),
            "score": int(getattr(opportunity, "score", 0) or 0),
        }

    def run_due(self, now: datetime | None = None) -> list[ScheduledSearchResult]:
        results = []

        for schedule in self.scheduler.due(now):
            try:
                opportunities = self.search_service.search(
                    schedule.query,
                    source_names=(schedule.source_names or None),
                )
                summaries = [
                    self._opportunity_summary(opportunity)
                    for opportunity in opportunities
                ]
                result = ScheduledSearchResult(
                    schedule_id=schedule.schedule_id,
                    query=schedule.query,
                    opportunity_count=len(opportunities),
                    opportunities=summaries,
                )
                self.scheduler.mark_ran(schedule.schedule_id, now)
            except Exception as error:
                result = ScheduledSearchResult(
                    schedule_id=schedule.schedule_id,
                    query=schedule.query,
                    error=str(error),
                )

            self.history_store.append(result)
            results.append(result)

        self.last_results = results
        return list(results)
