"""Offline test for persistent search schedule management."""

from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scheduling.search_schedule import SearchSchedule
from src.scheduling.search_schedule_store import SearchScheduleStore
from src.scheduling.search_scheduler import SearchScheduler
from src.version import VERSION_INFO


def main() -> None:
    now = datetime(2026, 7, 22, 4, 0, tzinfo=timezone.utc)

    with tempfile.TemporaryDirectory() as directory:
        store = SearchScheduleStore(Path(directory) / "schedules.json")
        scheduler = SearchScheduler(store)
        schedule = SearchSchedule(
            query="camping product testers",
            interval_minutes=30,
            schedule_id="camping-test",
            next_run_at="2026-07-22T03:30:00+00:00",
        )
        scheduler.add(schedule)

        assert [item.schedule_id for item in scheduler.due(now)] == ["camping-test"]

        scheduler.mark_ran("camping-test", now)
        assert scheduler.due(now) == []
        assert schedule.next_run_at == "2026-07-22T04:30:00+00:00"

        scheduler.set_enabled("camping-test", False)
        reloaded = SearchScheduler(store)
        assert reloaded.get("camping-test").enabled is False

        reloaded.remove("camping-test")
        assert SearchScheduler(store).all() == []

    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-24"
    assert VERSION_INFO.build == 24
    print("Phase 2 search scheduler test passed.")


if __name__ == "__main__":
    main()
