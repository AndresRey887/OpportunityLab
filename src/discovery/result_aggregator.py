"""Aggregate raw results returned by OpportunityLab discovery sources."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from src.discovery.discovery_result import DiscoveryBatchResult, SourceExecutionResult


class ResultAggregator:
    """Combine source outputs while preserving source-level statistics."""

    def aggregate(
        self,
        source_results: Iterable[SourceExecutionResult],
    ) -> DiscoveryBatchResult:
        """Merge valid dictionaries and remove duplicate links.

        The first occurrence of a link is retained. Results without a usable
        link are kept because they cannot be safely identified as duplicates.
        Each returned item receives a ``source`` value when it does not already
        contain one.
        """

        executions = tuple(source_results)
        combined: list[dict[str, Any]] = []
        seen_links: set[str] = set()
        duplicate_count = 0

        for execution in executions:
            for raw_item in execution.results:
                if not isinstance(raw_item, dict):
                    continue

                item = dict(raw_item)
                item.setdefault("source", execution.source_name)

                link = self._normalise_link(item)
                if link:
                    if link in seen_links:
                        duplicate_count += 1
                        continue
                    seen_links.add(link)

                combined.append(item)

        return DiscoveryBatchResult(
            results=combined,
            source_results=executions,
            duplicate_count=duplicate_count,
        )

    @staticmethod
    def _normalise_link(item: dict[str, Any]) -> str:
        """Return a stable lowercase link key when one is available."""

        value = item.get("link") or item.get("url")
        if not isinstance(value, str):
            return ""
        return value.strip().rstrip("/").lower()
