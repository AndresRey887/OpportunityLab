"""Offline smoke test for source controls in the Filter Manager."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    filter_window_path = PROJECT_ROOT / "src" / "ui" / "filter_window.py"
    source = filter_window_path.read_text(encoding="utf-8")

    assert "Result Sources" in source
    assert "source_variables" in source
    assert "set_allowed_sources" in source
    assert "clear_allowed_sources" in source
    assert "Select at least one result source" in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-17"
    assert VERSION_INFO.build == 17

    print("Phase 2 source filter UI test passed.")


if __name__ == "__main__":
    main()
