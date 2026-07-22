"""Offline test for background scheduled-result reporting."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scheduling.scheduled_search_monitor import ScheduledSearchMonitor
from src.version import VERSION_INFO


class FakeRunner:
    def run_due(self, now=None):
        return ["scheduled result"]


def main() -> None:
    received = []
    monitor = ScheduledSearchMonitor(
        FakeRunner(),
        on_results=lambda results: received.extend(results),
    )
    results = monitor.check_now()

    assert results == ["scheduled result"]
    assert received == ["scheduled result"]

    main_source = (
        PROJECT_ROOT / "src" / "ui" / "main_window.py"
    ).read_text(encoding="utf-8")
    assert "self.scheduled_result_queue = queue.Queue()" in main_source
    assert "on_results=self.queue_scheduled_results" in main_source
    assert "def poll_scheduled_results" in main_source
    assert "New opportunities: {new_count}" in main_source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-34"
    assert VERSION_INFO.build == 34
    print("Phase 2 scheduled result notice test passed.")


if __name__ == "__main__":
    main()
