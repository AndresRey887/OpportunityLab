"""Offline test for Phase 5 company intelligence profiles."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.companies.company_intelligence_service import CompanyIntelligenceService
from src.companies.company_profile_store import CompanyProfileStore
from src.models.opportunity import Opportunity
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        first, _ = tracking.track(
            Opportunity(
                title="Acme Product Testing Program",
                url="https://www.acme.example/testing",
                source="Company Websites",
                score=90,
            )
        )
        second, _ = tracking.track(
            Opportunity(
                title="Acme Supplier Partnership",
                url="https://acme.example/partners",
                source="Serper",
                score=84,
            )
        )
        separate, _ = tracking.track(
            Opportunity(
                title="Other Organisation Grant",
                url="https://other.example/grant",
                source="Serper",
                score=72,
            )
        )

        store = CompanyProfileStore(root / "companies.json")
        companies = CompanyIntelligenceService(store)
        profile = companies.get_or_create(first)
        same_profile = companies.get_or_create(second)
        other_profile = companies.get_or_create(separate)
        assert profile.company_id == same_profile.company_id
        assert profile.domain == "acme.example"
        assert set(profile.linked_tracking_ids) == {
            first.tracking_id,
            second.tracking_id,
        }
        assert other_profile.company_id != profile.company_id
        assert len(companies.profiles) == 2

        companies.update(
            profile.company_id,
            name="Acme Australia",
            industry="Outdoor Products",
            location="Victoria, Australia",
            email="opportunities@acme.example",
            phone="03 5555 0200",
            description="Australian outdoor product company.",
            notes="Monitor product testing and supplier programs.",
            tags="outdoors, product testing, supplier",
        )
        reloaded = CompanyIntelligenceService(store)
        saved = reloaded.get(profile.company_id)
        assert saved.name == "Acme Australia"
        assert saved.industry == "Outdoor Products"
        assert saved.location == "Victoria, Australia"
        assert saved.tags == ["outdoors", "product testing", "supplier"]
        assert len(saved.linked_tracking_ids) == 2

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    company_window = (
        PROJECT_ROOT / "src/ui/company_profile_window.py"
    ).read_text(encoding="utf-8")
    assert "CompanyIntelligenceService" in main_window
    assert "Company Intelligence" in main_window
    assert 'text="Company"' in pipeline_window
    assert "Linked opportunities:" in company_window
    assert "Save Company" in company_window
    assert VERSION_INFO.version == "0.23.0"
    assert VERSION_INFO.package == "Package-023A-01"
    assert VERSION_INFO.build == 1
    assert VERSION_INFO.codename == "Discovery"

    print("Phase 5 company intelligence test passed.")


if __name__ == "__main__":
    main()
