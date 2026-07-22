"""Offline test for running a saved schedule immediately."""

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
                title="Test result",
                url="https://example.com/result",
                snippet="Australian opportunity.",
                source="Reddit",
                score=75,
            )
        ]


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        scheduler = SearchScheduler(SearchScheduleStore(root / "schedules.json"))
        schedule = SearchSchedule(
            query="camping testers",
            interval_minutes=60,
            schedule_id="run-now",
        )
        scheduler.add(schedule)
        history = ScheduledSearchHistoryStore(root / "results.json")
        runner = ScheduledSearchRunner(scheduler, FakeSearchService(), history)

        result = runner.run_schedule("run-now")

        assert result.succeeded is True
        assert result.opportunity_count == 1
        assert len(history.load()) == 1
        assert scheduler.get("run-now").last_run_at is not None

    window_source = (
        PROJECT_ROOT / "src" / "ui" / "scheduled_search_window.py"
    ).read_text(encoding="utf-8")
    assert 'text="Run Now"' in window_source
    assert "target=self.runner.run_schedule" in window_source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-31"
    assert VERSION_INFO.build == 31
    print("Phase 2 schedule Run Now test passed.")


if __name__ == "__main__":
    main()
