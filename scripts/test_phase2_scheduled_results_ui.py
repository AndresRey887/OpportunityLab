"""Offline smoke test for scheduled result history in the UI."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    window_path = PROJECT_ROOT / "src" / "ui" / "scheduled_search_window.py"
    source = window_path.read_text(encoding="utf-8")

    assert "self.history_store = master.scheduled_search_runner.history_store" in source
    assert "Recent Scheduled Results" in source
    assert "def refresh_history" in source
    assert "self.history_store.load()" in source
    assert "result.opportunities[:3]" in source
    assert "No scheduled search results yet." in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-30"
    assert VERSION_INFO.build == 30
    print("Phase 2 scheduled results UI test passed.")


if __name__ == "__main__":
    main()
