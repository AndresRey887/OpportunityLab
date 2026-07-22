"""Offline test for the Reddit discovery source."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.discovery.reddit_search_source import RedditSearchSource
from src.discovery.source_registry import SourceRegistry
from src.version import VERSION_INFO


class FakeSerperClient:
    def __init__(self) -> None:
        self.query = ""

    def search(self, query: str) -> dict[str, Any]:
        self.query = query
        return {
            "organic": [
                {
                    "title": "Australian camping gear testers",
                    "link": "https://www.reddit.com/r/CampingGear/",
                    "snippet": "A discussion about product testing.",
                },
                "ignored non-dictionary result",
            ]
        }


def main() -> None:
    client = FakeSerperClient()
    source = RedditSearchSource(client=client)
    results = source.search("camping product testers")
    registry = SourceRegistry([source])

    assert source.name == "Reddit"
    assert client.query == "site:reddit.com camping product testers"
    assert len(results) == 1
    assert results[0]["link"].startswith("https://www.reddit.com/")
    assert registry.enabled_names() == ["Reddit"]
    assert VERSION_INFO.package == "Package-020A-13"
    assert VERSION_INFO.build == 13

    print("Phase 2 Reddit source test passed.")


if __name__ == "__main__":
    main()
