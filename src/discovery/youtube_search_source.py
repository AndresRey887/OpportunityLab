"""YouTube discovery source backed by the existing Serper client."""

from __future__ import annotations

from typing import Any

from src.discovery.search_source import SearchSource


class YouTubeSearchSource(SearchSource):
    """Search YouTube results without requiring another API key."""

    def __init__(self, client: Any | None = None) -> None:
        super().__init__("YouTube")

        if client is None:
            from src.clients.serper_client import SerperClient

            client = SerperClient()

        self.client = client

    def search(self, query: str) -> list[dict[str, Any]]:
        youtube_query = f"site:youtube.com {query.strip()}".strip()
        data = self.client.search(youtube_query)
        organic = data.get("organic", [])

        if not isinstance(organic, list):
            return []

        return [item for item in organic if isinstance(item, dict)]
