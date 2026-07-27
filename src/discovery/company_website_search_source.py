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
        base_query = " ".join(query.strip().split())[:350]
        company_query = (
            f'{base_query} '
            '(apply OR grant OR sponsorship OR partnership OR support) '
            "-site:reddit.com -site:youtube.com"
        ).strip()
        data = self.client.search(company_query)
        organic = data.get("organic", [])

        if not isinstance(organic, list):
            return []

        return [item for item in organic if isinstance(item, dict)]
