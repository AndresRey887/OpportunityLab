"""Offline test for Phase 2 Opportunity model normalization."""

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
from src.models.opportunity import Opportunity
from src.version import VERSION_INFO


class TestSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Test Source")

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping opportunity"

        return [
            {
                "title": "Camping product tester",
                "link": "https://www.example.com.au/testing/camping",
                "snippet": "Applications are open.",
                "position": 1,
            },
            {
                "name": "Outdoor review program",
                "url": "https://reviews.example.org/program",
                "description": "Review outdoor equipment.",
                "position": 2,
            },
        ]


def main() -> None:
    pipeline = DiscoveryPipeline(SourceRegistry([TestSource()]))

    execution_results = pipeline.execute("camping opportunity")
    opportunities = pipeline.aggregate()

    assert len(execution_results) == 1
    assert len(opportunities) == 2
    assert all(isinstance(item, Opportunity) for item in opportunities)

    first = opportunities[0]
    assert first.title == "Camping product tester"
    assert first.url == "https://www.example.com.au/testing/camping"
    assert first.snippet == "Applications are open."
    assert first.source == "Test Source"
    assert first.domain == "example.com.au"
    assert first.metadata["raw_result"]["position"] == 1

    second = opportunities[1]
    assert second.title == "Outdoor review program"
    assert second.url == "https://reviews.example.org/program"
    assert second.snippet == "Review outdoor equipment."
    assert second.source == "Test Source"
    assert second.domain == "reviews.example.org"
    assert second.metadata["raw_result"]["position"] == 2

    statistics = pipeline.statistics()
    assert statistics["Test Source"]["succeeded"] is True
    assert statistics["Test Source"]["result_count"] == 2

    assert VERSION_INFO.version == "0.20.0"
    assert VERSION_INFO.package == "Package-020A-06"
    assert VERSION_INFO.build == 6
    assert VERSION_INFO.codename == "Trailblazer"

    print("Phase 2 opportunity normalization test passed.")


if __name__ == "__main__":
    main()
