"""Offline regression test for the Phase 2 discovery-source foundation."""

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


class FakeSearchSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Offline Test Source")

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping product tester"
        return [
            {
                "title": "Australian camping equipment product testers wanted",
                "link": "https://example.com.au/product-testers",
                "snippet": "Apply to test upcoming camping equipment releases.",
            }
        ]


def main() -> None:
    service = SearchService(sources=[FakeSearchSource()])
    results = service.search("camping product tester")

    assert VERSION_INFO.version == "0.20.0"
    assert VERSION_INFO.package == "Package-020A-02"
    assert VERSION_INFO.codename == "Trailblazer"
    assert len(results) == 1
    assert results[0].source == "Offline Test Source"
    assert results[0].title == "Australian camping equipment product testers wanted"
    assert results[0].url == "https://example.com.au/product-testers"

    print("Phase 2 discovery-source foundation test passed.")


if __name__ == "__main__":
    main()
