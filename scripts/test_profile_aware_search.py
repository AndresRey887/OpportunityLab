"""Verify nonprofit profiles expand searches and influence scoring."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.engine.opportunity_engine import OpportunityEngine
from src.models.opportunity import Opportunity
from src.profiles.profile_search_context import ProfileSearchContextService
from src.profiles.sender_profile_service import SenderProfileService
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        profiles = SenderProfileService(Path(directory) / "profiles.json")
        personal_query = ProfileSearchContextService(profiles).build(
            "woodworking equipment"
        )
        assert personal_query.effective_query == "woodworking equipment"
        assert not personal_query.expanded

        nonprofit = profiles.create("Youth Workshop")
        profiles.update(
            nonprofit.profile_id,
            profile_type="Nonprofit",
            mission="woodworking education",
            beneficiaries="young people",
            service_area="Victoria",
            support_needs="tools equipment cash",
            opportunity_types="grants, sponsorships, product donations",
            dgr_status="DGR endorsed",
        )
        context = ProfileSearchContextService(profiles).build(
            "woodworking equipment"
        )
        assert context.expanded
        assert "grants OR sponsorships" in context.effective_query
        assert "woodworking education" in context.effective_query
        assert "young people" in context.effective_query
        assert "Victoria" in context.effective_query

        opportunity = Opportunity(
            title="Applications open for Victorian community grants",
            url="https://example.org/grants",
            snippet=(
                "Funding for youth education and tools. Check eligibility "
                "and apply to the current community grant round."
            ),
            source="Official website",
        )
        OpportunityEngine(profiles).score(opportunity)
        profile_result = next(
            item for item in opportunity.rule_results
            if item["rule"] == "Nonprofit Profile Fit"
        )
        assert profile_result["points"] >= 17
        assert opportunity.metadata["profile_fit_type"] == "Open Opportunity"

    main_source = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    result_source = (PROJECT_ROOT / "src/ui/results_panel.py").read_text(
        encoding="utf-8"
    )
    assert "profile_service=self.sender_profile_service" in main_source
    assert "profile_fit_type" in result_source
    assert VERSION_INFO.version == "1.2.1"
    assert VERSION_INFO.package == "Package-110A-07A"
    assert VERSION_INFO.build == 10
    print("Profile-aware search test passed.")


if __name__ == "__main__":
    main()
