"""Result models for OpportunityLab discovery-source execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceExecutionResult:
    """Results and timing information from one discovery source."""

    source_name: str
    results: list[dict[str, Any]] = field(default_factory=list)
    elapsed_seconds: float = 0.0
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        """Return True when the source completed without an error."""

        return self.error is None

    @property
    def result_count(self) -> int:
        """Return the number of valid result dictionaries produced."""

        return len(self.results)


@dataclass(frozen=True)
class DiscoveryBatchResult:
    """Aggregated results and statistics for one multi-source search."""

    results: list[dict[str, Any]]
    source_results: tuple[SourceExecutionResult, ...]
    duplicate_count: int = 0

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
    def total_elapsed_seconds(self) -> float:
        return sum(result.elapsed_seconds for result in self.source_results)
