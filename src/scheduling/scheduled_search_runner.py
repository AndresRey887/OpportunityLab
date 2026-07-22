"""Execute OpportunityLab scheduled searches."""

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
    def _opportunity_summary(opportunity: Any, known_urls: set[str]) -> dict:
        url = str(getattr(opportunity, "url", "")).strip()
        return {
            "title": str(getattr(opportunity, "title", "")),
            "url": url,
            "snippet": str(getattr(opportunity, "snippet", "")),
            "source": str(getattr(opportunity, "source", "")),
            "score": int(getattr(opportunity, "score", 0) or 0),
            "is_new": bool(url and url.casefold() not in known_urls),
        }

    def _known_urls(self, schedule_id: str) -> set[str]:
        known_urls = set()
        for result in self.history_store.load():
            if result.schedule_id != schedule_id:
                continue
            for opportunity in result.opportunities:
                url = str(opportunity.get("url", "")).strip()
                if url:
                    known_urls.add(url.casefold())
        return known_urls

    def run_schedule(
        self,
        schedule_id: str,
        now: datetime | None = None,
    ) -> ScheduledSearchResult:
        schedule = self.scheduler.get(schedule_id)

        try:
            known_urls = self._known_urls(schedule.schedule_id)
            opportunities = self.search_service.search(
                schedule.query,
                source_names=(schedule.source_names or None),
            )
            summaries = [
                self._opportunity_summary(opportunity, known_urls)
                for opportunity in opportunities
            ]
            result = ScheduledSearchResult(
                schedule_id=schedule.schedule_id,
                query=schedule.query,
                opportunity_count=len(opportunities),
                new_opportunity_count=sum(
                    bool(summary["is_new"])
                    for summary in summaries
                ),
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
        self.last_results = [result]
        return result

    def run_due(self, now: datetime | None = None) -> list[ScheduledSearchResult]:
        results = [
            self.run_schedule(schedule.schedule_id, now)
            for schedule in self.scheduler.due(now)
        ]
        self.last_results = results
        return list(results)
