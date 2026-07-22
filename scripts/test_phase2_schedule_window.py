"""Offline smoke test for the Scheduled Searches window."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    window_source = (
        PROJECT_ROOT / "src" / "ui" / "scheduled_search_window.py"
    ).read_text(encoding="utf-8")
    main_source = (
        PROJECT_ROOT / "src" / "ui" / "main_window.py"
    ).read_text(encoding="utf-8")

    assert "class ScheduledSearchWindow" in window_source
    assert "Create Scheduled Search" in window_source
    assert "self.scheduler.add(schedule)" in window_source
    assert "self.scheduler.set_enabled" in window_source
    assert "self.scheduler.remove" in window_source
    assert 'text="Schedules..."' in main_source
    assert "self.open_scheduled_searches" in main_source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-28"
    assert VERSION_INFO.build == 28
    print("Phase 2 schedule window test passed.")


if __name__ == "__main__":
    main()
