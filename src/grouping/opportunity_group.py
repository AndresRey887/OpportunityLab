"""A named group of OpportunityLab results."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.models.opportunity import Opportunity


@dataclass
class OpportunityGroup:
    key: str
    label: str
    opportunities: list[Opportunity] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.opportunities)
