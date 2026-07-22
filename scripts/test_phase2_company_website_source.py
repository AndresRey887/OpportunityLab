"""Offline test for the company-website discovery source."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.discovery.company_website_search_source import CompanyWebsiteSearchSource
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
                    "title": "Join our Australian product testing panel",
                    "link": "https://example.com.au/product-testing",
                    "snippet": "Apply to test new camping products.",
                },
                None,
            ]
        }


def main() -> None:
    client = FakeSerperClient()
    source = CompanyWebsiteSearchSource(client=client)
    results = source.search("camping product testers")
    registry = SourceRegistry([source])

    assert source.name == "Company Websites"
    assert client.query == (
        'camping product testers (apply OR opportunity OR "product testing") '
        "-site:reddit.com -site:youtube.com"
    )
    assert len(results) == 1
    assert results[0]["link"] == "https://example.com.au/product-testing"
    assert registry.enabled_names() == ["Company Websites"]
    assert VERSION_INFO.package == "Package-020A-15"
    assert VERSION_INFO.build == 15

    print("Phase 2 company-website source test passed.")


if __name__ == "__main__":
    main()
