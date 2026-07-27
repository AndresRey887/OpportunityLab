"""Offline integration test for the persistent Australia Only filter."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.filters.filter_engine import FilterEngine
from src.filters.filter_settings_store import FilterSettingsStore
from src.models.opportunity import Opportunity
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        settings = FilterSettingsStore(
            Path(directory) / "filter_settings.json"
        )
        engine = FilterEngine(settings)
        engine.set_australia_only(True)

        australian_domain = Opportunity(
            title="Community grants",
            url="https://example.org.au/grants",
            snippet="Applications are open.",
        )
        australian_text = Opportunity(
            title="Victorian charity partnership",
            url="https://example.com/community",
            snippet="Supporting organisations in Melbourne.",
        )
        unsupported_location = Opportunity(
            title="Community grant",
            url="https://example.com/grants",
            snippet="Applications are open.",
        )

        results = engine.process(
            [australian_domain, australian_text, unsupported_location]
        )
        assert results == [australian_domain, australian_text]
        assert engine.statistics.filtered == 1
        assert engine.statistics.reasons == {"Outside Australia": 1}

        reloaded = FilterEngine(settings)
        assert reloaded.is_australia_only()

    source = (
        PROJECT_ROOT / "src" / "core" / "search_service.py"
    ).read_text(encoding="utf-8")
    window = (
        PROJECT_ROOT / "src" / "ui" / "filter_window.py"
    ).read_text(encoding="utf-8")
    assert 'effective_query = f"{effective_query} Australia"' in source
    assert 'text="Australia Only"' in window
    assert "coming soon" not in window.casefold().split("australia only", 1)[1][:40]
    assert VERSION_INFO.version == "1.1.3"
    assert VERSION_INFO.package == "Package-110A-04"
    assert VERSION_INFO.build == 4
    print("Australia Only filter test passed.")


if __name__ == "__main__":
    main()
