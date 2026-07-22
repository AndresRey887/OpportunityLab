"""Offline test for the complete Phase 2 discovery run result."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.discovery.discovery_pipeline import DiscoveryPipeline
from src.discovery.discovery_run import DiscoveryRun
from src.discovery.search_source import SearchSource
from src.discovery.source_registry import SourceRegistry
from src.version import VERSION_INFO


class PrimarySource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Primary")

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping product tester"
        return [
            {
                "title": "Camping tester program",
                "link": "https://example.com/testing?utm_source=test",
                "snippet": "First result.",
            },
            {
                "title": "Second result",
                "link": "https://example.com/second",
                "snippet": "Second result.",
            },
        ]


class DuplicateSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Duplicate")

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping product tester"
        return [
            {
                "title": "Duplicate result",
                "url": "https://www.example.com/testing",
                "description": "Duplicate copy.",
            }
        ]


class FailingSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Failing")

    def search(self, query: str) -> list[dict[str, Any]]:
        raise RuntimeError("source unavailable")


def main() -> None:
    pipeline = DiscoveryPipeline(
        SourceRegistry(
            [
                PrimarySource(),
                DuplicateSource(),
                FailingSource(),
            ]
        )
    )

    result = pipeline.run("camping product tester")

    assert isinstance(result, DiscoveryRun)
    assert pipeline.last_run is result
    assert result.query == "camping product tester"

    assert result.source_count == 3
    assert result.successful_source_count == 2
    assert result.failed_source_count == 1
    assert result.raw_result_count == 3

    assert result.opportunity_count == 2
    assert result.opportunities[0].title == "Camping tester program"
    assert result.opportunities[1].title == "Second result"

    assert result.errors == {"Failing": "source unavailable"}

    assert VERSION_INFO.package == "Package-020A-09"
    assert VERSION_INFO.build == 9

    print("Phase 2 discovery run test passed.")


if __name__ == "__main__":
    main()
