"""Offline test for filtering opportunities by discovery source."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.filters.filter_engine import FilterEngine
from src.models.opportunity import Opportunity
from src.version import VERSION_INFO


def opportunity(title: str, source: str) -> Opportunity:
    return Opportunity(
        title=title,
        url=f"https://example.com/{title.lower()}",
        snippet="Australian product testing opportunity.",
        source=source,
    )


def main() -> None:
    engine = FilterEngine()
    items = [
        opportunity("Reddit result", "Reddit"),
        opportunity("YouTube result", "YouTube"),
        opportunity("Company result", "Company Websites"),
    ]

    assert len(engine.process(items)) == 3

    engine.set_allowed_sources(["Reddit", "Company Websites"])
    accepted = engine.process(items)

    assert [item.source for item in accepted] == ["Reddit", "Company Websites"]
    assert engine.statistics.filtered == 1
    assert engine.statistics.reasons == {"Source not selected": 1}

    engine.clear_allowed_sources()
    assert len(engine.process(items)) == 3
    assert VERSION_INFO.package == "Package-020A-16"
    assert VERSION_INFO.build == 16

    print("Phase 2 source filter test passed.")


if __name__ == "__main__":
    main()
