"""Offline test for nonprofit supporter and donor prospects."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.opportunity import Opportunity
from src.profiles.sender_profile import SenderProfile
from src.rules.supporter_prospect_rule import SupporterProspectRule
from src.version import VERSION_INFO


class ProfileService:
    active_profile = SenderProfile(
        name="Wildlife Rescue",
        profile_type="Nonprofit",
        mission="Rescue injured wildlife",
        beneficiaries="Native animals",
        service_area="Victoria",
        support_needs="Veterinary equipment",
    )


def main() -> None:
    rule = SupporterProspectRule(ProfileService())
    strong = Opportunity(
        title="Our community charity partners",
        url="https://example.com.au/community",
        snippet=(
            "Our annual impact report explains how we supported native animal "
            "rescue through product donations. Contact our community "
            "partnerships team for partnership enquiries."
        ),
        source="Company Websites",
    )
    generic = Opportunity(
        title="Business community news",
        url="https://example.com.au/news",
        snippet="General company updates.",
        source="Serper",
    )

    assert rule.evaluate(strong) >= 35
    assert strong.metadata["supporter_prospect_type"] == "Contactable Supporter"
    assert strong.metadata["supporter_prospect_reasons"]
    assert rule.evaluate(generic) == 0
    assert "supporter_prospect_type" not in generic.metadata

    search_context = (
        PROJECT_ROOT / "src" / "profiles" / "profile_search_context.py"
    ).read_text(encoding="utf-8")
    details = (
        PROJECT_ROOT / "src" / "ui" / "details_panel.py"
    ).read_text(encoding="utf-8")
    assert "corporate giving" in search_context
    assert "Supporter prospect:" in details

    assert VERSION_INFO.version == "1.2.1"
    assert VERSION_INFO.package == "Package-110A-07A"
    assert VERSION_INFO.build == 10
    print("Supporter prospect test passed.")


if __name__ == "__main__":
    main()
