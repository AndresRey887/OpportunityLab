"""Offline smoke test for collapsible result groups."""

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

    assert "self.collapsed_groups = set()" in source
    assert "command=lambda group_key=key: self.toggle_group(group_key)" in source
    assert "def toggle_group(self, key)" in source
    assert "card_area.pack_forget()" in source
    assert 'marker = "▶"' in source
    assert 'marker = "▼"' in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-37"
    assert VERSION_INFO.build == 37
    print("Phase 2 collapsible result-group test passed.")


if __name__ == "__main__":
    main()
