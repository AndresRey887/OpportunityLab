"""Offline test for webpage and profile-location eligibility checks."""

from __future__ import annotations

import sys
import types
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if "requests" not in sys.modules:
    sys.modules["requests"] = types.SimpleNamespace(get=lambda *args, **kwargs: None)

from src.filters.profile_eligibility_filter import ProfileEligibilityFilter
from src.models.opportunity import Opportunity
from src.profiles.sender_profile import SenderProfile
from src.research.page_evidence_service import PageEvidenceService
from src.version import VERSION_INFO


class Response:
    headers = {"Content-Type": "text/html"}

    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        return None


def main() -> None:
    profile = SenderProfile(
        name="Ballarat Charity",
        profile_type="Nonprofit",
        address="Ballarat, Victoria",
        service_area="Ballarat and regional Victoria",
    )
    service = PageEvidenceService()

    excluded = Opportunity(
        title="Community Organisation Partnerships Program",
        url="https://example.org.au/grants",
        score=60,
    )
    included = Opportunity(
        title="Victorian community grants",
        url="https://example.org.au/victoria",
        score=30,
    )

    original_get = sys.modules["requests"].get
    try:
        sys.modules["requests"].get = lambda *args, **kwargs: Response(
            "<html><body>Eligible Area: Townsville Local Government Area. "
            "Eligible not-for-profit organisations may apply.</body></html>"
        )
        service.verify(excluded, profile)

        sys.modules["requests"].get = lambda *args, **kwargs: Response(
            "<html><body>Eligible organisations across Australia may apply. "
            "Victorian charities are welcome.</body></html>"
        )
        service.verify(included, profile)
    finally:
        sys.modules["requests"].get = original_get

    assert excluded.metadata["profile_eligibility_status"] == "Ineligible"
    assert excluded.score == 10
    assert included.metadata["profile_eligibility_status"] == "Eligible"
    assert included.score == 38

    location_filter = ProfileEligibilityFilter()
    assert not location_filter.accepts(excluded)
    assert location_filter.accepts(included)

    gemini_source = (
        PROJECT_ROOT / "src" / "ai" / "gemini_provider.py"
    ).read_text(encoding="utf-8")
    assert "Extracted official webpage evidence:" in gemini_source
    assert "Active profile location:" in gemini_source

    assert VERSION_INFO.version == "1.2.1"
    assert VERSION_INFO.package == "Package-110A-07A"
    assert VERSION_INFO.build == 10
    print("Page eligibility verification test passed.")


if __name__ == "__main__":
    main()
