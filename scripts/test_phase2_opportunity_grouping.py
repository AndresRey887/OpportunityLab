"""Offline test for opportunity grouping."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.grouping.opportunity_grouper import OpportunityGrouper
from src.models.opportunity import Opportunity
from src.version import VERSION_INFO


def item(title, url, source):
    return Opportunity(
        title=title,
        url=url,
        snippet="Australian opportunity.",
        source=source,
    )


def main() -> None:
    opportunities = [
        item("One", "https://www.reddit.com/r/testing/1", "Reddit"),
        item("Two", "https://reddit.com/r/testing/2", "Reddit"),
        item("Three", "https://youtube.com/watch?v=3", "YouTube"),
        item("Four", "not a URL", "Company Websites"),
    ]
    grouper = OpportunityGrouper()

    source_groups = grouper.group_by_source(opportunities)
    assert [(group.label, group.count) for group in source_groups] == [
        ("Reddit", 2),
        ("Company Websites", 1),
        ("YouTube", 1),
    ]

    domain_groups = grouper.group_by_domain(opportunities)
    assert domain_groups[0].label == "reddit.com"
    assert domain_groups[0].count == 2
    assert sum(group.count for group in domain_groups) == 4

    assert VERSION_INFO.window_title == "OpportunityLab 0.20.0"
    assert VERSION_INFO.package == "Package-020A-35"
    assert VERSION_INFO.build == 35
    print("Phase 2 opportunity grouping test passed.")


if __name__ == "__main__":
    main()
