"""Offline smoke test for clickable scheduled result links."""

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

    assert "import webbrowser" in source
    assert 'text=f"Open: {title}"' in source
    assert "command=lambda link=url: self.open_result(link)" in source
    assert "def open_result(url)" in source
    assert "webbrowser.open(url)" in source
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-32"
    assert VERSION_INFO.build == 32
    print("Phase 2 scheduled result-link test passed.")


if __name__ == "__main__":
    main()
