"""Multi-source execution pipeline for OpportunityLab discovery sources."""

from __future__ import annotations

from src.discovery.discovery_run import DiscoveryRun
from src.discovery.execution_result import SourceExecutionResult
from src.discovery.opportunity_deduplicator import OpportunityDeduplicator
from src.discovery.result_aggregator import ResultAggregator
from src.discovery.source_registry import SourceRegistry
from src.models.opportunity import Opportunity


class DiscoveryPipeline:
    """Execute enabled sources and prepare normalized discovery results."""

    def __init__(
        self,
        registry: SourceRegistry,
        aggregator: ResultAggregator | None = None,
        deduplicator: OpportunityDeduplicator | None = None,
    ) -> None:
        self.registry = registry
        self.aggregator = aggregator or ResultAggregator()
        self.deduplicator = deduplicator or OpportunityDeduplicator()
        self.last_results: list[SourceExecutionResult] = []
        self.last_run: DiscoveryRun | None = None

    def execute(self, query: str) -> list[SourceExecutionResult]:
        results: list[SourceExecutionResult] = []

        for source in self.registry.enabled_sources():
            try:
                raw_items = source.search(query)
                items = [item for item in raw_items if isinstance(item, dict)]

                results.append(
                    SourceExecutionResult(
                        source_name=source.name,
                        items=items,
                    )
                )
            except Exception as error:
                results.append(
                    SourceExecutionResult(
                        source_name=source.name,
                        items=[],
                        error=str(error),
                    )
                )

        self.last_results = results
        return list(results)

    def aggregate(
        self,
        execution_results: list[SourceExecutionResult] | None = None,
    ) -> list[Opportunity]:
        """Return normalized Opportunity objects from source execution results."""

        results = self.last_results if execution_results is None else execution_results
        return self.aggregator.aggregate(results)

    def aggregate_unique(
        self,
        execution_results: list[SourceExecutionResult] | None = None,
    ) -> list[Opportunity]:
        """Return normalized opportunities with duplicates removed."""

        opportunities = self.aggregate(execution_results)
        return self.deduplicator.deduplicate(opportunities)

    def run(self, query: str) -> DiscoveryRun:
        """Execute, normalize, and deduplicate one complete discovery query."""

        source_results = self.execute(query)
        opportunities = self.aggregate_unique(source_results)

        discovery_run = DiscoveryRun(
            query=query,
            source_results=list(source_results),
            opportunities=list(opportunities),
        )
        self.last_run = discovery_run
        return discovery_run

    def statistics(self) -> dict[str, dict[str, int | str | bool | None]]:
        """Return lightweight statistics for the most recent execution."""

        return {
            result.source_name: {
                "succeeded": result.succeeded,
                "result_count": result.result_count,
                "error": result.error,
            }
            for result in self.last_results
        }
