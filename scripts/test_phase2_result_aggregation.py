"""Offline test for Phase 2 discovery result aggregation."""

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


class WorkingSource(SearchSource):
    def __init__(self, name: str, items: list[dict[str, Any]]) -> None:
        super().__init__(name)
        self.items = items

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping product tester"
        return list(self.items)


class FailingSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Failing Source")

    def search(self, query: str) -> list[dict[str, Any]]:
        raise RuntimeError("offline source failure")


def main() -> None:
    registry = SourceRegistry(
        [
            WorkingSource(
                "First Source",
                [
                    {
                        "title": "First opportunity",
                        "link": "https://example.com/first",
                        "snippet": "First result.",
                    },
                    {
                        "title": "Second opportunity",
                        "link": "https://example.com/second",
                        "snippet": "Second result.",
                    },
                ],
            ),
            FailingSource(),
            WorkingSource(
                "Second Source",
                [
                    {
                        "title": "Third opportunity",
                        "link": "https://example.com/third",
                        "snippet": "Third result.",
                    }
                ],
            ),
        ]
    )

    pipeline = DiscoveryPipeline(registry)
    execution_results = pipeline.execute("camping product tester")
    aggregated = pipeline.aggregate()

    assert len(execution_results) == 3
    assert len(aggregated) == 3

    assert aggregated[0]["title"] == "First opportunity"
    assert aggregated[0]["source"] == "First Source"
    assert aggregated[1]["source"] == "First Source"
    assert aggregated[2]["title"] == "Third opportunity"
    assert aggregated[2]["source"] == "Second Source"

    assert all(item["source"] != "Failing Source" for item in aggregated)

    assert pipeline.statistics()["Failing Source"]["succeeded"] is False
    assert pipeline.statistics()["Failing Source"]["error"] == "offline source failure"

    assert VERSION_INFO.version == "0.20.0"
    assert VERSION_INFO.package == "Package-020A-05"
    assert VERSION_INFO.build == 5
    assert VERSION_INFO.codename == "Trailblazer"

    print("Phase 2 result aggregation test passed.")


if __name__ == "__main__":
    main()
