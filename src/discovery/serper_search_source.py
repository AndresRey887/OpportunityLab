"""Serper implementation of the OpportunityLab discovery source interface."""

from __future__ import annotations

from typing import Any

from src.clients.serper_client import SerperClient
from src.discovery.search_source import SearchSource


class SerperSearchSource(SearchSource):
    """Use the existing Serper client as a named discovery source."""

    def __init__(self, client: SerperClient | None = None) -> None:
        super().__init__("Serper")
        self.client = client or SerperClient()

    def search(self, query: str) -> list[dict[str, Any]]:
        data = self.client.search(query)
        organic = data.get("organic", [])

        if not isinstance(organic, list):
            return []

        return [item for item in organic if isinstance(item, dict)]
