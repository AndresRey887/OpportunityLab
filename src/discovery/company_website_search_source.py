"""Company-website discovery source backed by the existing Serper client."""

from __future__ import annotations

from typing import Any

from src.discovery.search_source import SearchSource


class CompanyWebsiteSearchSource(SearchSource):
    """Search the wider web while excluding Reddit and YouTube results."""

    def __init__(self, client: Any | None = None) -> None:
        super().__init__("Company Websites")

        if client is None:
            from src.clients.serper_client import SerperClient

            client = SerperClient()

        self.client = client

    def search(self, query: str) -> list[dict[str, Any]]:
        company_query = (
            f'{query.strip()} (apply OR opportunity OR "product testing") '
            "-site:reddit.com -site:youtube.com"
        ).strip()
        data = self.client.search(company_query)
        organic = data.get("organic", [])

        if not isinstance(organic, list):
            return []

        return [item for item in organic if isinstance(item, dict)]
