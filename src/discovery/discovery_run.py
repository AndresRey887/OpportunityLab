"""Structured result returned by a complete discovery pipeline run."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.discovery.execution_result import SourceExecutionResult
from src.models.opportunity import Opportunity


@dataclass(frozen=True)
class DiscoveryRun:
    """All results produced by one discovery query."""

    query: str
    source_results: list[SourceExecutionResult] = field(default_factory=list)
    opportunities: list[Opportunity] = field(default_factory=list)

    @property
    def source_count(self) -> int:
        return len(self.source_results)

    @property
    def successful_source_count(self) -> int:
        return sum(result.succeeded for result in self.source_results)

    @property
    def failed_source_count(self) -> int:
        return self.source_count - self.successful_source_count

    @property
    def raw_result_count(self) -> int:
        return sum(result.result_count for result in self.source_results)

    @property
    def opportunity_count(self) -> int:
        return len(self.opportunities)

    @property
    def errors(self) -> dict[str, str]:
        return {
            result.source_name: result.error
            for result in self.source_results
            if result.error is not None
        }
