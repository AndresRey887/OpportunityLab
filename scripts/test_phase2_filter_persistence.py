"""Offline test for persistent filter settings."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.filters.filter_engine import FilterEngine
from src.filters.filter_settings_store import FilterSettingsStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "filter_settings.json"
        first = FilterEngine(FilterSettingsStore(path))
        first.set_blocked_domains(["example.com", "shop.test"])
        first.set_blocked_keywords(["competition", "survey"])
        first.set_allowed_sources(["Reddit", "Company Websites"])

        second = FilterEngine(FilterSettingsStore(path))

        assert second.get_blocked_domains() == ["example.com", "shop.test"]
        assert second.get_blocked_keywords() == ["competition", "survey"]
        assert second.get_allowed_sources() == ["company websites", "reddit"]

    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-20"
    assert VERSION_INFO.build == 20
    print("Phase 2 filter persistence test passed.")


if __name__ == "__main__":
    main()
