"""Offline test for executing due scheduled searches."""

from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scheduling.scheduled_search_runner import ScheduledSearchRunner
from src.scheduling.search_schedule import SearchSchedule
from src.scheduling.search_schedule_store import SearchScheduleStore
from src.scheduling.search_scheduler import SearchScheduler
from src.version import VERSION_INFO


class FakeSearchService:
    def __init__(self) -> None:
        self.calls = []

    def search(self, query, source_names=None):
        self.calls.append((query, source_names))
        if query == "broken search":
            raise RuntimeError("Offline test failure")
        return [object(), object()]


def main() -> None:
    now = datetime(2026, 7, 22, 5, 0, tzinfo=timezone.utc)

    with tempfile.TemporaryDirectory() as directory:
        scheduler = SearchScheduler(
            SearchScheduleStore(Path(directory) / "schedules.json")
        )
        good = SearchSchedule(
            query="camping testers",
            interval_minutes=60,
            source_names=["Reddit"],
            schedule_id="good",
            next_run_at="2026-07-22T04:00:00+00:00",
        )
        broken = SearchSchedule(
            query="broken search",
            interval_minutes=60,
            schedule_id="broken",
            next_run_at="2026-07-22T04:00:00+00:00",
        )
        scheduler.add(good)
        scheduler.add(broken)

        service = FakeSearchService()
        results = ScheduledSearchRunner(scheduler, service).run_due(now)

        assert service.calls == [
            ("camping testers", ["Reddit"]),
            ("broken search", None),
        ]
        assert results[0].succeeded is True
        assert results[0].opportunity_count == 2
        assert results[1].succeeded is False
        assert results[1].error == "Offline test failure"
        assert scheduler.get("good").next_run_at == "2026-07-22T06:00:00+00:00"
        assert scheduler.get("broken").next_run_at == "2026-07-22T04:00:00+00:00"

    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-25"
    assert VERSION_INFO.build == 25
    print("Phase 2 scheduled search runner test passed.")


if __name__ == "__main__":
    main()
