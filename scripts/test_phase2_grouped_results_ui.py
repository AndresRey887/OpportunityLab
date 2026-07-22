"""Offline smoke test for source-grouped result cards."""

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

    assert "self.group_frames = {}" in source
    assert "def _group_for(self, source)" in source
    assert 'text=f"{label} (0)"' in source
    assert "self.group_counts[key] += 1" in source
    assert "group = self._group_for" in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-36"
    assert VERSION_INFO.build == 36
    print("Phase 2 grouped results UI test passed.")


if __name__ == "__main__":
    main()
