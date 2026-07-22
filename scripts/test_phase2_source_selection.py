"""Offline test for selecting discovery sources per search."""

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


class TrackingSource(SearchSource):
    def __init__(self, name: str, url: str) -> None:
        super().__init__(name)
        self.url = url
        self.calls = 0

    def search(self, query: str) -> list[dict[str, Any]]:
        self.calls += 1
        return [
            {
                "title": f"{self.name} result",
                "link": self.url,
                "snippet": query,
            }
        ]


def main() -> None:
    first = TrackingSource("First", "https://example.com/first")
    second = TrackingSource("Second", "https://example.com/second")
    disabled = TrackingSource("Disabled", "https://example.com/disabled")

    service = SearchService(sources=[first, second, disabled])
    service.disable_source("Disabled")

    results = service.search(
        "selected query",
        source_names=["Second"],
    )

    assert first.calls == 0
    assert second.calls == 1
    assert disabled.calls == 0

    assert len(results) == 1
    assert results[0].title == "Second result"
    assert results[0].source == "Second"

    assert service.source_statistics == {
        "Second": {
            "succeeded": True,
            "result_count": 1,
            "error": None,
        }
    }

    selected = service.registry.selected_sources(
        ["Second", "First", "Second"]
    )
    assert [source.name for source in selected] == ["Second", "First"]

    try:
        service.search("bad query", source_names=["Missing"])
    except KeyError as error:
        assert str(error).strip("'") == "Missing"
    else:
        raise AssertionError("Unknown source name should raise KeyError.")

    assert VERSION_INFO.package == "Package-020A-11"
    assert VERSION_INFO.build == 11

    print("Phase 2 source selection test passed.")


if __name__ == "__main__":
    main()
