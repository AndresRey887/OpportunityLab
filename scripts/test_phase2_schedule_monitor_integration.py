"""Offline smoke test for main-window schedule monitor integration."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    main_window_path = PROJECT_ROOT / "src" / "ui" / "main_window.py"
    source = main_window_path.read_text(encoding="utf-8")

    assert "self.search_scheduler = SearchScheduler()" in source
    assert "self.scheduled_search_runner = ScheduledSearchRunner(" in source
    assert "self.scheduled_search_monitor = ScheduledSearchMonitor(" in source
    assert "self.scheduled_search_monitor.start()" in source
    assert "self.scheduled_search_monitor.stop()" in source
    assert "self.scheduled_search_service = SearchService()" in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-27"
    assert VERSION_INFO.build == 27
    print("Phase 2 schedule monitor integration test passed.")


if __name__ == "__main__":
    main()
