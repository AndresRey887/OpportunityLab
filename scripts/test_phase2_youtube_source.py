"""Offline test for the YouTube discovery source."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.discovery.source_registry import SourceRegistry
from src.discovery.youtube_search_source import YouTubeSearchSource
from src.version import VERSION_INFO


class FakeSerperClient:
    def __init__(self) -> None:
        self.query = ""

    def search(self, query: str) -> dict[str, Any]:
        self.query = query
        return {
            "organic": [
                {
                    "title": "Camping equipment testing opportunities",
                    "link": "https://www.youtube.com/watch?v=example",
                    "snippet": "A video covering Australian testing programs.",
                },
                123,
            ]
        }


def main() -> None:
    client = FakeSerperClient()
    source = YouTubeSearchSource(client=client)
    results = source.search("camping product testers")
    registry = SourceRegistry([source])

    assert source.name == "YouTube"
    assert client.query == "site:youtube.com camping product testers"
    assert len(results) == 1
    assert results[0]["link"].startswith("https://www.youtube.com/")
    assert registry.enabled_names() == ["YouTube"]
    assert VERSION_INFO.package == "Package-020A-14"
    assert VERSION_INFO.build == 14

    print("Phase 2 YouTube source test passed.")


if __name__ == "__main__":
    main()
