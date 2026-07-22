"""Offline smoke test for per-source status counts."""

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

    assert "self.search_service.source_statistics.items()" in source
    assert "source_stats.get('result_count', 0)" in source
    assert 'source_parts.append(f"{source_name}: failed")' in source
    assert 'source_detail = "   ".join(source_parts)' in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-22"
    assert VERSION_INFO.build == 22

    print("Phase 2 source status-count test passed.")


if __name__ == "__main__":
    main()
