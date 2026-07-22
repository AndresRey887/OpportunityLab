"""Offline test for Phase 2 opportunity deduplication."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.discovery.discovery_pipeline import DiscoveryPipeline
from src.discovery.search_source import SearchSource
from src.discovery.source_registry import SourceRegistry
from src.version import VERSION_INFO


class FirstSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("First Source")

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping tester"

        return [
            {
                "title": "Camping tester program",
                "link": (
                    "https://www.example.com.au/testing/camping/"
                    "?utm_source=newsletter&item=42"
                ),
                "snippet": "First copy.",
            },
            {
                "title": "Unique first-source result",
                "link": "https://example.com.au/unique",
                "snippet": "Unique result.",
            },
        ]


class SecondSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Second Source")

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping tester"

        return [
            {
                "title": "The same result with another title",
                "url": (
                    "https://example.com.au/testing/camping"
                    "?item=42&utm_medium=email#details"
                ),
                "description": "Duplicate copy.",
            },
            {
                "title": "Unique second-source result",
                "url": "https://other.example.org/opportunity",
                "description": "Another unique result.",
            },
        ]


def main() -> None:
    pipeline = DiscoveryPipeline(
        SourceRegistry(
            [
                FirstSource(),
                SecondSource(),
            ]
        )
    )

    pipeline.execute("camping tester")

    all_opportunities = pipeline.aggregate()
    unique_opportunities = pipeline.aggregate_unique()

    assert len(all_opportunities) == 4
    assert len(unique_opportunities) == 3

    assert unique_opportunities[0].title == "Camping tester program"
    assert unique_opportunities[0].source == "First Source"

    assert unique_opportunities[1].title == "Unique first-source result"
    assert unique_opportunities[2].title == "Unique second-source result"

    canonical = pipeline.deduplicator.canonical_url(
        "https://www.example.com.au/testing/camping/"
        "?utm_source=newsletter&item=42#top"
    )
    assert canonical == "https://example.com.au/testing/camping?item=42"

    assert VERSION_INFO.version == "0.20.0"
    assert VERSION_INFO.package == "Package-020A-07"
    assert VERSION_INFO.build == 7
    assert VERSION_INFO.codename == "Trailblazer"

    print("Phase 2 opportunity deduplication test passed.")


if __name__ == "__main__":
    main()
