"""Offline smoke test for result-card source labels."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    panel_path = PROJECT_ROOT / "src" / "ui" / "results_panel.py"
    source = panel_path.read_text(encoding="utf-8")

    assert 'getattr(opportunity, "source", "Unknown Source")' in source
    assert "text_area" in source
    assert "source.pack" in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-19"
    assert VERSION_INFO.build == 19

    print("Phase 2 result source-label test passed.")


if __name__ == "__main__":
    main()
