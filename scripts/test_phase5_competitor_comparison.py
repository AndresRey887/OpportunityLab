"""Offline test for Phase 5 competitor profiles and comparisons."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.companies.company_intelligence_service import CompanyIntelligenceService
from src.companies.company_profile_store import CompanyProfileStore
from src.competition.competitor_service import CompetitorService
from src.competition.competitor_store import CompetitorStore
from src.research.research_evidence_service import ResearchEvidenceService
from src.research.research_evidence_store import ResearchEvidenceStore
from src.version import VERSION_INFO


def record(title, url, tracking_id):
    return SimpleNamespace(title=title, url=url, tracking_id=tracking_id)


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        companies = CompanyIntelligenceService(
            CompanyProfileStore(root / "companies.json")
        )
        evidence = ResearchEvidenceService(
            ResearchEvidenceStore(root / "evidence.json")
        )
        competitor_store = CompetitorStore(root / "competitors.json")
        competitors = CompetitorService(competitor_store)

        acme = companies.get_or_create(
            record("Acme Opportunity", "https://acme.example", "track-acme")
        )
        rival = companies.get_or_create(
            record("Rival Opportunity", "https://rival.example", "track-rival")
        )
        companies.update(
            acme.company_id,
            name="Acme Outdoors",
            industry="Outdoor Products",
            location="Victoria",
        )
        companies.update(
            rival.company_id,
            name="Rival Camping",
            industry="Camping Equipment",
            location="New South Wales",
        )
        evidence.add(
            acme.company_id,
            category="Market",
            claim="Acme sells nationally.",
            confidence=5,
        )
        evidence.add(
            rival.company_id,
            category="Product",
            claim="Rival has a broad tent range.",
            confidence=4,
        )

        link, created = competitors.link(
            acme.company_id,
            rival.company_id,
            market_overlap="Camping and outdoor equipment",
            strength=4,
            notes="Compete for similar Australian customers.",
        )
        assert created
        updated, created_again = competitors.link(
            rival.company_id,
            acme.company_id,
            market_overlap="Outdoor retail",
            strength=5,
            notes="Strong direct competition.",
        )
        assert not created_again
        assert updated.link_id == link.link_id
        assert len(competitors.links) == 1
        assert updated.strength == 5

        comparisons = competitors.comparisons(
            acme.company_id,
            companies,
            evidence,
        )
        assert len(comparisons) == 1
        comparison = comparisons[0]
        assert comparison.company.company_id == acme.company_id
        assert comparison.competitor.company_id == rival.company_id
        assert comparison.company_evidence["total"] == 1
        assert comparison.competitor_evidence["high_confidence"] == 1
        assert comparison.link.market_overlap == "Outdoor retail"

        reloaded = CompetitorService(competitor_store)
        assert len(reloaded.for_company(acme.company_id)) == 1
        assert len(reloaded.for_company(rival.company_id)) == 1
        reloaded.remove(link.link_id)
        assert reloaded.for_company(acme.company_id) == []

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    company_window = (
        PROJECT_ROOT / "src/ui/company_profile_window.py"
    ).read_text(encoding="utf-8")
    comparison_window = (
        PROJECT_ROOT / "src/ui/company_comparison_window.py"
    ).read_text(encoding="utf-8")
    assert "CompetitorService" in main_window
    assert 'text="Competitors"' in company_window
    assert "Competitor Comparison" in comparison_window
    assert "Save Competitor" in comparison_window
    assert "Competitive strength:" in comparison_window
    assert VERSION_INFO.package == "Package-023A-03"
    assert VERSION_INFO.build == 3

    print("Phase 5 competitor comparison test passed.")


if __name__ == "__main__":
    main()
