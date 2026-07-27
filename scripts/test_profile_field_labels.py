"""Offline source test for permanent sender-profile field labels."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    source = (
        PROJECT_ROOT / "src" / "ui" / "sender_profile_window.py"
    ).read_text(encoding="utf-8")
    assert 'text=placeholder' in source
    assert 'placeholder_text=f"Enter {placeholder.lower()} here"' in source
    assert '("address", "Address, for example Ballarat, Victoria")' in source
    assert VERSION_INFO.version == "1.2.1"
    assert VERSION_INFO.package == "Package-110A-07A"
    assert VERSION_INFO.build == 10
    print("Profile field labels test passed.")


if __name__ == "__main__":
    main()
