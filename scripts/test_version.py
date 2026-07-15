"""No-network smoke test for OpportunityLab version information."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    assert VERSION_INFO.app_name == "OpportunityLab"
    assert VERSION_INFO.version == "0.19.0"
    assert VERSION_INFO.package == "Package-019B-08"
    assert VERSION_INFO.build == 8
    assert VERSION_INFO.codename == "Prospector"
    assert VERSION_INFO.status == "Development"
    assert VERSION_INFO.window_title == "OpportunityLab 0.19.0"
    assert "Package-019B-08" in VERSION_INFO.full_label
    assert "Build 8" in VERSION_INFO.full_label

    print("Version information smoke test passed.")


if __name__ == "__main__":
    main()
