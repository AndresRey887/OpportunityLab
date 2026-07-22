"""Aggregate raw discovery-source results into one normalized collection."""

from __future__ import annotations

from typing import Any

from src.discovery.execution_result import SourceExecutionResult


class ResultAggregator:
    """Combine successful source results while preserving source identity."""

    def aggregate(
        self,
        execution_results: list[SourceExecutionResult],
    ) -> list[dict[str, Any]]:
        aggregated: list[dict[str, Any]] = []

        for execution_result in execution_results:
            if not execution_result.succeeded:
                continue

            for raw_item in execution_result.items:
                item = dict(raw_item)
                item["source"] = execution_result.source_name
                aggregated.append(item)

        return aggregated
