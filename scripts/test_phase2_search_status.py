"""Offline smoke test for the expanded search status display."""

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

    assert "search_run.raw_result_count" in source
    assert "search_run.unique_result_count" in source
    assert 'f"Sources: {successful_sources}/{search_run.source_count}"' in source
    assert 'f"Unique: {unique_count}' in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-21"
    assert VERSION_INFO.build == 21

    print("Phase 2 search status test passed.")


if __name__ == "__main__":
    main()
