"""
Search Service
Version: 0.6

Purpose:
Coordinates OpportunityLab discovery sources, scoring, and filtering.
"""

from __future__ import annotations

from collections.abc import Iterable

from src.core.service import Service
from src.discovery.search_source import SearchSource
from src.discovery.source_registry import SourceRegistry
from src.engine.opportunity_engine import OpportunityEngine
from src.filters.filter_engine import FilterEngine
from src.models.opportunity import Opportunity


class SearchService(Service):
    """Search enabled discovery sources and return scored opportunities."""

    def __init__(
        self,
        sources: Iterable[SearchSource] | None = None,
        registry: SourceRegistry | None = None,
    ) -> None:
        super().__init__("SearchService")

        if registry is not None and sources is not None:
            raise ValueError("Provide either sources or registry, not both.")

        if registry is not None:
            self.registry = registry
        elif sources is not None:
            self.registry = SourceRegistry(sources)
        else:
            from src.discovery.serper_search_source import SerperSearchSource

            self.registry = SourceRegistry([SerperSearchSource()])

        self.engine = OpportunityEngine()
        self.filter_engine = FilterEngine()
        self.statistics = self.filter_engine.statistics

    @property
    def sources(self) -> list[SearchSource]:
        """Return all registered sources for backward compatibility."""
        return self.registry.all_sources()

    def register_source(self, source: SearchSource, *, enabled: bool = True) -> None:
        """Register a discovery source with this search service."""
        self.registry.register(source, enabled=enabled)

    def enable_source(self, name: str) -> None:
        """Enable a registered discovery source."""
        self.registry.enable(name)

    def disable_source(self, name: str) -> None:
        """Disable a registered discovery source."""
        self.registry.disable(name)

    def initialize(self) -> None:
        print("[SEARCH] initialize() called")

    def search(self, query: str) -> list[Opportunity]:
        opportunities: list[Opportunity] = []

        for source in self.registry.enabled_sources():
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
