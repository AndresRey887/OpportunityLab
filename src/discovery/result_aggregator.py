"""Aggregate discovery-source results into normalized opportunities."""

from __future__ import annotations

from src.discovery.execution_result import SourceExecutionResult
from src.discovery.opportunity_normalizer import OpportunityNormalizer
from src.models.opportunity import Opportunity


class ResultAggregator:
    """Combine successful source results into Opportunity model objects."""

    def __init__(
        self,
        normalizer: OpportunityNormalizer | None = None,
    ) -> None:
        self.normalizer = normalizer or OpportunityNormalizer()

    def aggregate(
        self,
        execution_results: list[SourceExecutionResult],
    ) -> list[Opportunity]:
        aggregated: list[Opportunity] = []

        for execution_result in execution_results:
            if not execution_result.succeeded:
                continue

            for raw_item in execution_result.items:
                aggregated.append(
                    self.normalizer.normalize(
                        raw_item,
                        source_name=execution_result.source_name,
                    )
                )

        return aggregated
