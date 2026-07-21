"""Multi-source execution pipeline for OpportunityLab discovery sources."""

from __future__ import annotations

from src.discovery.execution_result import SourceExecutionResult
from src.discovery.source_registry import SourceRegistry


class DiscoveryPipeline:
    """Execute every enabled source without allowing one failure to stop the rest."""

    def __init__(self, registry: SourceRegistry) -> None:
        self.registry = registry
        self.last_results: list[SourceExecutionResult] = []

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
            except Exception as error:  # A source failure must not stop other sources.
                results.append(
                    SourceExecutionResult(
                        source_name=source.name,
                        items=[],
                        error=str(error),
                    )
                )

        self.last_results = results
        return list(results)

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
