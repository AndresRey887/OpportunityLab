"""Offline smoke test for the result-grouping selector."""

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

    assert "self.group_mode = ctk.StringVar(value=\"Source\")" in source
    assert 'values=["Source", "Website"]' in source
    assert "command=self.change_grouping" in source
    assert "def change_grouping" in source
    assert "self.grouper.group_by_domain([opportunity])" in source
    assert "for opportunity in self.opportunities" in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-38"
    assert VERSION_INFO.build == 38
    print("Phase 2 grouping selector test passed.")


if __name__ == "__main__":
    main()
