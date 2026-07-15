"""
Search Service
Version: 0.5

Purpose:
Coordinates OpportunityLab discovery sources, scoring, and filtering.
"""

from __future__ import annotations

from collections.abc import Iterable

from src.core.service import Service
from src.discovery.search_source import SearchSource
from src.engine.opportunity_engine import OpportunityEngine
from src.filters.filter_engine import FilterEngine
from src.models.opportunity import Opportunity


class SearchService(Service):
    """Search one or more discovery sources and return scored opportunities."""

    def __init__(self, sources: Iterable[SearchSource] | None = None) -> None:
        super().__init__("SearchService")

        if sources is None:
            from src.discovery.serper_search_source import SerperSearchSource

            self.sources = [SerperSearchSource()]
        else:
            self.sources = list(sources)

        self.engine = OpportunityEngine()
        self.filter_engine = FilterEngine()
        self.statistics = self.filter_engine.statistics

    def initialize(self) -> None:
        print("[SEARCH] initialize() called")

    def search(self, query: str) -> list[Opportunity]:
        opportunities: list[Opportunity] = []

        for source in self.sources:
            for item in source.search(query):
                opportunity = Opportunity(
                    title=item.get("title", ""),
                    url=item.get("link", item.get("url", "")),
                    snippet=item.get("snippet", ""),
                    source=source.name,
                )

                opportunities.append(self.engine.score(opportunity))

        opportunities = self.filter_engine.process(opportunities)
        self.statistics = self.filter_engine.statistics

        return opportunities

    def start(self) -> None:
        super().start()
        print("[SEARCH] Search service started")

    def stop(self) -> None:
        super().stop()
        print("[SEARCH] Search service stopped")
