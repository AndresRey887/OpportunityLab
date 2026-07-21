"""Offline test for the Phase 2 multi-source execution pipeline."""

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


class WorkingSource(SearchSource):
    def __init__(self, name: str, title: str) -> None:
        super().__init__(name)
        self.title = title

    def search(self, query: str) -> list[dict[str, Any]]:
        assert query == "camping product tester"
        return [
            {
                "title": self.title,
                "link": f"https://example.com/{self.name.lower().replace(' ', '-')}",
                "snippet": "Australian product testing opportunity.",
            }
        ]


class FailingSource(SearchSource):
    def __init__(self) -> None:
        super().__init__("Failing Source")

    def search(self, query: str) -> list[dict[str, Any]]:
        raise RuntimeError("offline source failure")


def main() -> None:
    service = SearchService(
        sources=[
            WorkingSource("First Source", "First opportunity"),
            FailingSource(),
            WorkingSource("Second Source", "Second opportunity"),
        ]
    )

    results = service.search("camping product tester")

    assert len(results) == 2
    assert {item.source for item in results} == {"First Source", "Second Source"}

    assert service.source_statistics["First Source"]["succeeded"] is True
    assert service.source_statistics["First Source"]["result_count"] == 1
    assert service.source_statistics["Failing Source"]["succeeded"] is False
    assert service.source_statistics["Failing Source"]["result_count"] == 0
    assert service.source_statistics["Failing Source"]["error"] == "offline source failure"
    assert service.source_statistics["Second Source"]["succeeded"] is True

    assert VERSION_INFO.version == "0.20.0"
    assert VERSION_INFO.package == "Package-020A-03"
    assert VERSION_INFO.build == 3
    assert VERSION_INFO.codename == "Trailblazer"

    print("Phase 2 multi-source pipeline test passed.")


if __name__ == "__main__":
    main()
