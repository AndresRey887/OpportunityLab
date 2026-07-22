"""Offline test for structured SearchRun results."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.search_run import SearchRun
from src.core.search_service import SearchService
from src.discovery.search_source import SearchSource
from src.version import VERSION_INFO


class TestSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Test")

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping tester"
        return [
            {
                "title": "Camping product tester",
                "link": "https://example.org/testing",
                "snippet": "Australian product testing opportunity.",
            },
            {
                "title": "Survey giveaway",
                "link": "https://example.org/giveaway",
                "snippet": "Competition survey giveaway.",
            },
        ]


def main() -> None:
    service = SearchService(sources=[TestSource()])
    results = service.search("camping tester")

    assert len(results) == 1
    assert service.last_search_run is not None
    assert isinstance(service.last_search_run, SearchRun)

    run = service.last_search_run
    assert run.query == "camping tester"
    assert run.raw_result_count == 2
    assert run.unique_result_count == 2
    assert run.accepted_count == 1
    assert run.filtered_count == 1
    assert run.source_count == 1
    assert run.failed_source_count == 0
    assert sum(run.filter_reasons.values()) == 1
    assert run.opportunities[0].title == "Camping product tester"

    assert VERSION_INFO.package == "Package-020A-12"
    assert VERSION_INFO.build == 12

    print("Phase 2 SearchRun test passed.")


if __name__ == "__main__":
    main()
