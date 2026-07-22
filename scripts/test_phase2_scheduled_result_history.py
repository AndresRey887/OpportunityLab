"""Offline test for persistent scheduled-search results."""

from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scheduling.scheduled_search_history_store import ScheduledSearchHistoryStore
from src.scheduling.scheduled_search_runner import ScheduledSearchRunner
from src.scheduling.search_schedule import SearchSchedule
from src.scheduling.search_schedule_store import SearchScheduleStore
from src.scheduling.search_scheduler import SearchScheduler
from src.version import VERSION_INFO


class FakeSearchService:
    def search(self, query, source_names=None):
        return [
            SimpleNamespace(
                title="Camping tester wanted",
                url="https://example.com/testing",
                snippet="Australian testing opportunity.",
                source="Company Websites",
                score=82,
            )
        ]


def main() -> None:
    now = datetime(2026, 7, 22, 6, 0, tzinfo=timezone.utc)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        scheduler = SearchScheduler(SearchScheduleStore(root / "schedules.json"))
        scheduler.add(
            SearchSchedule(
                query="camping testers",
                interval_minutes=60,
                schedule_id="camping",
                next_run_at="2026-07-22T05:00:00+00:00",
            )
        )
        history = ScheduledSearchHistoryStore(root / "results.json")
        runner = ScheduledSearchRunner(scheduler, FakeSearchService(), history)
        runner.run_due(now)

        saved = history.load()
        assert len(saved) == 1
        assert saved[0].succeeded is True
        assert saved[0].opportunity_count == 1
        assert saved[0].opportunities[0]["title"] == "Camping tester wanted"
        assert saved[0].opportunities[0]["score"] == 82

    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-29"
    assert VERSION_INFO.build == 29
    print("Phase 2 scheduled result-history test passed.")


if __name__ == "__main__":
    main()
