"""Offline test for Phase 3 follow-up reminders and UI notices."""

from __future__ import annotations

import sys
import tempfile
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.opportunity import Opportunity
from src.reminders.reminder_service import ReminderService
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def add_record(service, title, url, follow_up_date, status="Reviewing"):
    record, _ = service.track(
        Opportunity(
            title=title,
            url=url,
            source="Company Websites",
            score=80,
        )
    )
    service.update(
        record.tracking_id,
        status=status,
        follow_up_date=follow_up_date,
    )
    return record


def main() -> None:
    today = date(2026, 7, 23)

    with tempfile.TemporaryDirectory() as directory:
        tracking = TrackingService(
            TrackingStore(Path(directory) / "tracked.json")
        )
        add_record(
            tracking,
            "Overdue opportunity",
            "https://example.com/overdue",
            "2026-07-22",
        )
        add_record(
            tracking,
            "Due today",
            "https://example.com/today",
            "2026-07-23",
        )
        add_record(
            tracking,
            "Coming soon",
            "https://example.com/upcoming",
            "2026-07-28",
        )
        add_record(
            tracking,
            "Closed item",
            "https://example.com/closed",
            "2026-07-20",
            status="Closed",
        )

        reminders = ReminderService(tracking)
        due = reminders.due(today)
        upcoming = reminders.upcoming(days=7, today=today)

        assert [reminder.state for reminder in due] == ["Overdue", "Due today"]
        assert [reminder.title for reminder in upcoming] == ["Coming soon"]
        assert all(reminder.title != "Closed item" for reminder in reminders.all(today))

    main_source = (
        PROJECT_ROOT / "src" / "ui" / "main_window.py"
    ).read_text(encoding="utf-8")
    tracking_source = (
        PROJECT_ROOT / "src" / "ui" / "tracking_window.py"
    ).read_text(encoding="utf-8")

    assert "def refresh_tracking_notice" in main_source
    assert "Follow-up reminders due" in main_source
    assert "Due or overdue" in tracking_source
    assert "Coming in 7 days" in tracking_source
    assert "Follow-up:" in tracking_source
    assert VERSION_INFO.version == "0.21.0"
    assert VERSION_INFO.package == "Package-021A-02"
    assert VERSION_INFO.build == 2
    print("Phase 3 follow-up reminder test passed.")


if __name__ == "__main__":
    main()
