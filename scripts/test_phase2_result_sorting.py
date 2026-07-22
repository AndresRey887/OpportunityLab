"""Offline smoke test for result sorting controls."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    panel_source = (
        PROJECT_ROOT / "src" / "ui" / "results_panel.py"
    ).read_text(encoding="utf-8")
    main_source = (
        PROJECT_ROOT / "src" / "ui" / "main_window.py"
    ).read_text(encoding="utf-8")

    assert 'self.sort_mode = ctk.StringVar(value="Score: High")' in panel_source
    assert 'values=["Score: High", "Score: Low", "Title"]' in panel_source
    assert "def show_opportunities" in panel_source
    assert "def _ordered_opportunities" in panel_source
    assert "key=lambda item: (-item.score" in panel_source
    assert "self.results.show_opportunities(opportunities)" in main_source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-39"
    assert VERSION_INFO.build == 39
    print("Phase 2 result sorting test passed.")


if __name__ == "__main__":
    main()
