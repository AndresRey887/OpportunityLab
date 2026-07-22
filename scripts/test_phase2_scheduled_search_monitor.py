"""Offline test for the scheduled-search background monitor."""

from __future__ import annotations

import sys
import threading
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scheduling.scheduled_search_monitor import ScheduledSearchMonitor
from src.version import VERSION_INFO


class FakeRunner:
    def __init__(self) -> None:
        self.calls = 0
        self.called = threading.Event()

    def run_due(self, now=None):
        self.calls += 1
        self.called.set()
        return []


def main() -> None:
    runner = FakeRunner()
    monitor = ScheduledSearchMonitor(runner, check_interval_seconds=0.05)

    assert monitor.running is False
    monitor.start()
    assert runner.called.wait(timeout=1.0)
    assert monitor.running is True

    monitor.start()
    monitor.stop()

    assert monitor.running is False
    assert runner.calls >= 1
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-26"
    assert VERSION_INFO.build == 26
    print("Phase 2 scheduled search monitor test passed.")


if __name__ == "__main__":
    main()
