"""Offline test for Australia-only geographic eligibility."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.filters.country_filter import CountryFilter
from src.models.opportunity import Opportunity
from src.version import VERSION_INFO


def main() -> None:
    rule = CountryFilter()
    rule.enabled = True

    foreign = Opportunity(
        title="Solomon Islands–Australia Community Partnerships Grant",
        url="https://www.dfat.gov.au/grants/solomon-islands",
        snippet="Funding community projects located in Solomon Islands.",
    )
    australian = Opportunity(
        title="Australian community partnership grants",
        url="https://example.org.au/grants",
        snippet="Open to Australian charities and not-for-profits.",
    )
    joint = Opportunity(
        title="Regional community grant",
        url="https://example.com/grants",
        snippet=(
            "Open to Australian organisations and organisations in "
            "New Zealand."
        ),
    )

    assert not rule.accepts(foreign)
    assert rule.accepts(australian)
    assert rule.accepts(joint)

    assert VERSION_INFO.version == "1.2.1"
    assert VERSION_INFO.package == "Package-110A-07A"
    assert VERSION_INFO.build == 10
    print("Australian geographic eligibility test passed.")


if __name__ == "__main__":
    main()
