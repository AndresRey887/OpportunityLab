"""Offline test for the search-scheduling foundation."""

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
from src.version import VERSION_INFO


def main() -> None:
    start = datetime(2026, 7, 22, 3, 0, tzinfo=timezone.utc)
    schedule = SearchSchedule(
        query="camping product testers",
        interval_minutes=60,
        source_names=["Reddit", "YouTube", "Reddit"],
    )
    schedule.mark_ran(start)

    assert schedule.source_names == ["Reddit", "YouTube"]
    assert schedule.last_run_at == "2026-07-22T03:00:00+00:00"
    assert schedule.next_run_at == "2026-07-22T04:00:00+00:00"

    with tempfile.TemporaryDirectory() as directory:
        store = SearchScheduleStore(Path(directory) / "schedules.json")
        store.save([schedule])
        loaded = store.load()

    assert len(loaded) == 1
    assert loaded[0].to_dict() == schedule.to_dict()
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-23"
    assert VERSION_INFO.build == 23
    print("Phase 2 search schedule test passed.")


if __name__ == "__main__":
    main()
