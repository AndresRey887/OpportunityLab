"""Verify every shutdown action runs despite component failures."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.shutdown_coordinator import ShutdownAction, ShutdownCoordinator
from src.version import VERSION_INFO


def main() -> None:
    calls = []

    def first() -> None:
        calls.append("first")

    def failing() -> None:
        calls.append("failing")
        raise RuntimeError("expected test error")

    def final() -> None:
        calls.append("final")

    results = ShutdownCoordinator().run(
        (
            ShutdownAction("first", first),
            ShutdownAction("failing", failing),
            ShutdownAction("final", final),
        )
    )
    assert calls == ["first", "failing", "final"]
    assert [result.succeeded for result in results] == [True, False, True]
    assert results[1].error == "RuntimeError: expected test error"

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    assert "ShutdownCoordinator().run" in main_window
    assert "scheduled_search_monitor.stop" in main_window
    assert "task_manager.shutdown(wait=False)" in main_window
    assert 'ShutdownAction("main window", self.destroy)' in main_window
    assert VERSION_INFO.package == "Package-100A-08"
    assert VERSION_INFO.build == 10
    print("Phase 6 shutdown test passed.")


if __name__ == "__main__":
    main()
