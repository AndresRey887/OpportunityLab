"""Offline test that source filters also control source execution."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.search_service import SearchService
from src.discovery.search_source import SearchSource
from src.version import VERSION_INFO


class CountingSource(SearchSource):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.calls = 0

    def search(self, query: str) -> list[dict[str, Any]]:
        self.calls += 1
        return [
            {
                "title": f"{self.name} product testing opportunity",
                "link": f"https://example.com/{self.name.lower()}",
                "snippet": "Australian product testing opportunity.",
            }
        ]


def main() -> None:
    serper = CountingSource("Serper")
    reddit = CountingSource("Reddit")
    youtube = CountingSource("YouTube")
    service = SearchService(sources=[serper, reddit, youtube])

    service.filter_engine.set_allowed_sources(["Reddit", "YouTube"])
    results = service.search("camping testers")

    assert serper.calls == 0
    assert reddit.calls == 1
    assert youtube.calls == 1
    assert {item.source for item in results} == {"Reddit", "YouTube"}
    assert service.last_search_run is not None
    assert service.last_search_run.source_count == 2
    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-18"
    assert VERSION_INFO.build == 18

    print("Phase 2 selected-source execution test passed.")


if __name__ == "__main__":
    main()
