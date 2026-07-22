"""Execute OpportunityLab searches that are due."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.scheduling.scheduled_search_result import ScheduledSearchResult
from src.scheduling.search_scheduler import SearchScheduler


class ScheduledSearchRunner:
    def __init__(self, scheduler: SearchScheduler, search_service: Any) -> None:
        self.scheduler = scheduler
        self.search_service = search_service
        self.last_results: list[ScheduledSearchResult] = []

    def run_due(self, now: datetime | None = None) -> list[ScheduledSearchResult]:
        results = []

        for schedule in self.scheduler.due(now):
            try:
                opportunities = self.search_service.search(
                    schedule.query,
                    source_names=(schedule.source_names or None),
                )
                result = ScheduledSearchResult(
                    schedule_id=schedule.schedule_id,
                    query=schedule.query,
                    opportunity_count=len(opportunities),
                )
                self.scheduler.mark_ran(schedule.schedule_id, now)
            except Exception as error:
                result = ScheduledSearchResult(
                    schedule_id=schedule.schedule_id,
                    query=schedule.query,
                    error=str(error),
                )

            results.append(result)

        self.last_results = results
        return list(results)
