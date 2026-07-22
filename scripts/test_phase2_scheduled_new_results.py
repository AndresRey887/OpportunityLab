"""Offline test for new-result detection in scheduled searches."""

from __future__ import annotations

import sys
import tempfile
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
                title="Repeated opportunity",
                url="https://example.com/same-result",
                snippet="Australian opportunity.",
                source="Reddit",
                score=80,
            )
        ]


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        scheduler = SearchScheduler(SearchScheduleStore(root / "schedules.json"))
        scheduler.add(
            SearchSchedule(
                query="camping testers",
                interval_minutes=60,
                schedule_id="new-results",
            )
        )
        history = ScheduledSearchHistoryStore(root / "results.json")
        runner = ScheduledSearchRunner(scheduler, FakeSearchService(), history)

        first = runner.run_schedule("new-results")
        second = runner.run_schedule("new-results")

        assert first.new_opportunity_count == 1
        assert first.opportunities[0]["is_new"] is True
        assert second.new_opportunity_count == 0
        assert second.opportunities[0]["is_new"] is False
        assert len(history.load()) == 2

    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-33"
    assert VERSION_INFO.build == 33
    print("Phase 2 scheduled new-result test passed.")


if __name__ == "__main__":
    main()
