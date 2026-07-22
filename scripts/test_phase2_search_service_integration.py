"""Offline test for SearchService integration with the discovery pipeline."""

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


class FirstSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("First")

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping tester"
        return [
            {
                "title": "Camping tester",
                "link": "https://example.com/test?utm_source=first",
                "snippet": "Original result.",
            },
            {
                "title": "Unique result",
                "link": "https://example.com/unique",
                "snippet": "Unique result.",
            },
        ]


class DuplicateSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Duplicate")

    def search(self, query: str) -> list[dict[str, Any]]:
        return [
            {
                "title": "Duplicate title",
                "url": "https://www.example.com/test",
                "description": "Duplicate result.",
            }
        ]


class DisabledSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Disabled")
        self.was_called = False

    def search(self, query: str) -> list[dict[str, Any]]:
        self.was_called = True
        return []


def main() -> None:
    disabled = DisabledSource()
    service = SearchService(
        sources=[
            FirstSource(),
            DuplicateSource(),
            disabled,
        ]
    )
    service.disable_source("Disabled")

    assert [source.name for source in service.sources] == [
        "First",
        "Duplicate",
        "Disabled",
    ]
    assert service.registry.is_enabled("First") is True
    assert service.registry.is_enabled("Disabled") is False

    opportunities = service.search("camping tester")

    assert disabled.was_called is False
    assert len(opportunities) == 2

    assert opportunities[0].title == "Camping tester"
    assert opportunities[0].source == "First"
    assert opportunities[1].title == "Unique result"

    assert service.last_discovery_run is not None
    assert service.last_discovery_run.raw_result_count == 3
    assert service.last_discovery_run.opportunity_count == 2

    assert service.source_statistics["First"]["result_count"] == 2
    assert service.source_statistics["Duplicate"]["result_count"] == 1
    assert "Disabled" not in service.source_statistics

    assert VERSION_INFO.package == "Package-020A-10"
    assert VERSION_INFO.build == 10

    print("Phase 2 SearchService integration test passed.")


if __name__ == "__main__":
    main()
