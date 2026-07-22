"""Structured result from a complete OpportunityLab search."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.discovery.discovery_run import DiscoveryRun
from src.models.opportunity import Opportunity


@dataclass(frozen=True)
class SearchRun:
    """Discovery, scoring, and filtering results for one search."""

    discovery: DiscoveryRun
    opportunities: list[Opportunity] = field(default_factory=list)
    filtered_count: int = 0
    filter_reasons: dict[str, int] = field(default_factory=dict)

    @property
    def query(self) -> str:
        return self.discovery.query

    @property
    def raw_result_count(self) -> int:
        return self.discovery.raw_result_count

    @property
    def unique_result_count(self) -> int:
        return self.discovery.opportunity_count

    @property
    def accepted_count(self) -> int:
        return len(self.opportunities)

    @property
    def source_count(self) -> int:
        return self.discovery.source_count

    @property
    def failed_source_count(self) -> int:
        return self.discovery.failed_source_count
