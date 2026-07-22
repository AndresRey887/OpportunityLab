"""
Search Service
Version: 0.13
Purpose: Coordinates OpportunityLab discovery sources, scoring, and filtering.
"""

from __future__ import annotations

from collections.abc import Iterable

from src.core.search_run import SearchRun
from src.core.service import Service
from src.discovery.discovery_pipeline import DiscoveryPipeline
from src.discovery.discovery_run import DiscoveryRun
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
            from src.discovery.company_website_search_source import (
                CompanyWebsiteSearchSource,
            )
            from src.discovery.reddit_search_source import RedditSearchSource
            from src.discovery.serper_search_source import SerperSearchSource
            from src.discovery.youtube_search_source import YouTubeSearchSource

            serper_source = SerperSearchSource()
            self.registry = SourceRegistry(
                [
                    serper_source,
                    RedditSearchSource(client=serper_source.client),
                    YouTubeSearchSource(client=serper_source.client),
                    CompanyWebsiteSearchSource(client=serper_source.client),
                ]
            )

        self.pipeline = DiscoveryPipeline(self.registry)
        self.engine = OpportunityEngine()
        self.filter_engine = FilterEngine()
        self.statistics = self.filter_engine.statistics
        self.source_statistics: dict[
            str, dict[str, int | str | bool | None]
        ] = {}
        self.last_discovery_run: DiscoveryRun | None = None
        self.last_search_run: SearchRun | None = None

    @property
    def sources(self) -> list[SearchSource]:
        """Return all registered sources for backward compatibility."""
        return self.registry.all_sources()

    def register_source(
        self,
        source: SearchSource,
        *,
        enabled: bool = True,
    ) -> None:
        self.registry.register(source, enabled=enabled)

    def enable_source(self, name: str) -> None:
        self.registry.enable(name)

    def disable_source(self, name: str) -> None:
        self.registry.disable(name)

    def initialize(self) -> None:
        print("[SEARCH] initialize() called")

    def search(
        self,
        query: str,
        source_names: Iterable[str] | None = None,
    ) -> list[Opportunity]:
        """Run selected discovery sources, score unique results, and filter."""

        discovery_run = self.pipeline.run(query, source_names=source_names)
        self.last_discovery_run = discovery_run

        scored_opportunities = [
            self.engine.score(opportunity)
            for opportunity in discovery_run.opportunities
        ]
        self.source_statistics = self.pipeline.statistics()

        filtered_opportunities = self.filter_engine.process(scored_opportunities)
        self.statistics = self.filter_engine.statistics

        self.last_search_run = SearchRun(
            discovery=discovery_run,
            opportunities=list(filtered_opportunities),
            filtered_count=self.statistics.filtered,
            filter_reasons=dict(self.statistics.reasons),
        )
        return filtered_opportunities

    def start(self) -> None:
        super().start()
        print("[SEARCH] Search service started")

    def stop(self) -> None:
        super().stop()
        print("[SEARCH] Search service stopped")
