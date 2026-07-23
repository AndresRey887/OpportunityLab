"""Verify monotonic startup performance tracking and integration."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.performance_tracker import PerformanceTracker
from src.version import VERSION_INFO


class FakeClock:
    def __init__(self) -> None:
        self.value = 10.0

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


def main() -> None:
    clock = FakeClock()
    tracker = PerformanceTracker("Test startup", clock=clock)
    clock.advance(0.25)
    first = tracker.checkpoint("services")
    clock.advance(0.50)
    second = tracker.checkpoint("interface")
    clock.advance(0.10)

    assert abs(first.elapsed_seconds - 0.25) < 0.000001
    assert abs(second.elapsed_seconds - 0.75) < 0.000001
    assert abs(tracker.elapsed_seconds - 0.85) < 0.000001
    assert len(tracker.checkpoints) == 2
    summary = tracker.summary()
    assert "services=0.250s" in summary
    assert "interface=0.750s" in summary
    assert "total=0.850s" in summary

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    assert 'PerformanceTracker("Application startup")' in main_window
    assert 'checkpoint("services")' in main_window
    assert 'checkpoint("interface")' in main_window
    assert 'checkpoint("ready")' in main_window
    assert VERSION_INFO.package == "Package-100A-08"
    assert VERSION_INFO.build == 10
    print("Phase 6 performance tracking test passed.")


if __name__ == "__main__":
    main()
