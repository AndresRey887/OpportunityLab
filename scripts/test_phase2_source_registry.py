"""Offline test for Phase 2 source registration and enable controls."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.search_service import SearchService
from src.discovery.search_source import SearchSource
from src.discovery.source_registry import SourceRegistry
from src.version import VERSION_INFO


class FakeSearchSource(SearchSource):
    def __init__(self, name: str, title: str) -> None:
        super().__init__(name)
        self.title = title

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping product tester"
        return [
            {
                "title": self.title,
                "link": f"https://example.com.au/{self.name.lower().replace(' ', '-')}",
                "snippet": "Australian product testing opportunity.",
            }
        ]


def main() -> None:
    first = FakeSearchSource("First Source", "First opportunity")
    second = FakeSearchSource("Second Source", "Second opportunity")

    registry = SourceRegistry()
    registry.register(first)
    registry.register(second, enabled=False)

    service = SearchService(registry=registry)

    first_results = service.search("camping product tester")
    assert len(first_results) == 1
    assert first_results[0].source == "First Source"

    service.enable_source("Second Source")
    second_results = service.search("camping product tester")
    assert len(second_results) == 2
    assert {item.source for item in second_results} == {
        "First Source",
        "Second Source",
    }

    service.disable_source("First Source")
    third_results = service.search("camping product tester")
    assert len(third_results) == 1
    assert third_results[0].source == "Second Source"

    assert VERSION_INFO.version == "0.20.0"
    assert VERSION_INFO.package == "Package-020A-02"
    assert VERSION_INFO.build == 2
    assert VERSION_INFO.codename == "Trailblazer"

    print("Phase 2 source registry test passed.")


if __name__ == "__main__":
    main()
