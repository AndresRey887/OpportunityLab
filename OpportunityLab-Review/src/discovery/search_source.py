"""Base interface for OpportunityLab discovery sources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SearchSource(ABC):
    """A source capable of returning raw web-search result dictionaries."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def search(self, query: str) -> list[dict[str, Any]]:
        """Return raw result dictionaries for a search query."""
        raise NotImplementedError
