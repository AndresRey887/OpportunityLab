"""Offline test for profile-aware result score explanations."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.engine.opportunity_engine import OpportunityEngine
from src.models.opportunity import Opportunity
from src.profiles.sender_profile import SenderProfile
from src.version import VERSION_INFO


class ProfileService:
    active_profile = SenderProfile(
        profile_id="wildlife",
        name="Wildlife Rescue",
        profile_type="Nonprofit",
        mission="Rescue injured wildlife",
        beneficiaries="Native animals",
        service_area="Victoria",
        support_needs="Veterinary equipment",
    )


def main() -> None:
    opportunity = Opportunity(
        title="Victorian wildlife community grant applications open",
        url="https://example.org.au/grants",
        snippet=(
            "Funding for native animal rescue and veterinary equipment "
            "in Victoria. Check eligibility and apply."
        ),
    )
    OpportunityEngine(ProfileService()).score(opportunity)

    assert opportunity.metadata["profile_fit_type"] == "Open Opportunity"
    reasons = opportunity.metadata["profile_fit_reasons"]
    assert any("Funding" in reason for reason in reasons)
    assert any("application or contact" in reason for reason in reasons)
    assert any("Profile terms matched" in reason for reason in reasons)
    assert any("Service area matched" in reason for reason in reasons)

    rule = next(
        result
        for result in opportunity.rule_results
        if result["rule"] == "Nonprofit Profile Fit"
    )
    assert rule["points"] > 0
    assert rule["reason"]

    details_source = (
        PROJECT_ROOT / "src" / "ui" / "details_panel.py"
    ).read_text(encoding="utf-8")
    assert "Why This Result Matched" in details_source
    assert "profile_fit_reasons" in details_source

    assert VERSION_INFO.version == "1.1.4"
    assert VERSION_INFO.package == "Package-110A-05"
    assert VERSION_INFO.build == 5
    print("Result score explanations test passed.")


if __name__ == "__main__":
    main()
