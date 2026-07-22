"""Offline completion test for OpportunityLab Phase 2."""

from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.search_service import SearchService
from src.discovery.search_source import SearchSource
from src.filters.filter_engine import FilterEngine
from src.filters.filter_settings_store import FilterSettingsStore
from src.grouping.opportunity_grouper import OpportunityGrouper
from src.scheduling.scheduled_search_history_store import ScheduledSearchHistoryStore
from src.scheduling.scheduled_search_runner import ScheduledSearchRunner
from src.scheduling.search_schedule import SearchSchedule
from src.scheduling.search_schedule_store import SearchScheduleStore
from src.scheduling.search_scheduler import SearchScheduler
from src.version import VERSION_INFO


class OfflineSource(SearchSource):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.calls = 0

    def search(self, query: str) -> list[dict[str, Any]]:
        self.calls += 1
        return [
            {
                "title": f"{self.name} camping product tester",
                "link": f"https://example.com/{self.name.casefold()}",
                "snippet": "Australian product testing opportunity.",
            }
        ]


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        reddit = OfflineSource("Reddit")
        youtube = OfflineSource("YouTube")
        service = SearchService(sources=[reddit, youtube])
        service.filter_engine = FilterEngine(
            FilterSettingsStore(root / "filters.json")
        )
        service.filter_engine.set_allowed_sources(["Reddit"])

        opportunities = service.search("camping testers")
        assert reddit.calls == 1
        assert youtube.calls == 0
        assert len(opportunities) == 1
        assert service.last_search_run is not None
        assert service.last_search_run.source_count == 1

        groups = OpportunityGrouper().group_by_source(opportunities)
        assert groups[0].label == "Reddit"
        assert groups[0].count == 1

        reloaded_filters = FilterEngine(FilterSettingsStore(root / "filters.json"))
        assert reloaded_filters.get_allowed_sources() == ["reddit"]

        scheduler = SearchScheduler(SearchScheduleStore(root / "schedules.json"))
        scheduler.add(
            SearchSchedule(
                query="camping testers",
                interval_minutes=60,
                source_names=["Reddit"],
                schedule_id="completion-test",
                next_run_at="2026-07-22T06:00:00+00:00",
            )
        )
        history = ScheduledSearchHistoryStore(root / "scheduled-results.json")
        runner = ScheduledSearchRunner(scheduler, service, history)
        results = runner.run_due(
            datetime(2026, 7, 22, 7, 0, tzinfo=timezone.utc)
        )

        assert len(results) == 1
        assert results[0].succeeded is True
        assert results[0].new_opportunity_count == 1
        assert len(history.load()) == 1

    assert VERSION_INFO.version == "0.20.0"
    assert VERSION_INFO.package == "Package-020A-40"
    assert VERSION_INFO.build == 40
    assert VERSION_INFO.status == "Phase 2 Complete"
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    print("OpportunityLab Phase 2 completion test passed.")


if __name__ == "__main__":
    main()
