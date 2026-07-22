"""Group OpportunityLab results by useful discovery attributes."""

from __future__ import annotations

from collections.abc import Iterable
from urllib.parse import urlparse

from src.grouping.opportunity_group import OpportunityGroup
from src.models.opportunity import Opportunity


class OpportunityGrouper:
    def group_by_source(
        self,
        opportunities: Iterable[Opportunity],
    ) -> list[OpportunityGroup]:
        return self._group(
            opportunities,
            key_function=lambda item: str(item.source).strip() or "Unknown Source",
        )

    def group_by_domain(
        self,
        opportunities: Iterable[Opportunity],
    ) -> list[OpportunityGroup]:
        return self._group(
            opportunities,
            key_function=self._domain,
        )

    @staticmethod
    def _domain(opportunity: Opportunity) -> str:
        try:
            hostname = urlparse(opportunity.url).hostname or ""
        except ValueError:
            hostname = ""

        hostname = hostname.casefold()
        if hostname.startswith("www."):
            hostname = hostname[4:]

        return hostname or "Unknown Website"

    @staticmethod
    def _group(
        opportunities: Iterable[Opportunity],
        key_function,
    ) -> list[OpportunityGroup]:
        grouped: dict[str, OpportunityGroup] = {}

        for opportunity in opportunities:
            label = key_function(opportunity)
            key = label.casefold()

            if key not in grouped:
                grouped[key] = OpportunityGroup(key=key, label=label)

            grouped[key].opportunities.append(opportunity)

        return sorted(
            grouped.values(),
            key=lambda group: (-group.count, group.label.casefold()),
        )
