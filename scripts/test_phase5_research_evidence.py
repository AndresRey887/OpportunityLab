"""Offline test for structured Phase 5 company research evidence."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.research.research_evidence_service import ResearchEvidenceService
from src.research.research_evidence_store import ResearchEvidenceStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        store = ResearchEvidenceStore(root / "evidence.json")
        service = ResearchEvidenceService(store)
        company_id = "company-acme"

        overview = service.add(
            company_id,
            category="Company Overview",
            claim="Acme operates an Australian outdoor products division.",
            source_url="https://acme.example/about",
            source_title="About Acme",
            evidence_date="2026-07-23",
            confidence=5,
            notes="Confirmed on the official website.",
        )
        launch = service.add(
            company_id,
            category="Product Launch",
            claim="A new camping range is planned for spring.",
            source_url="https://acme.example/news/spring-range",
            source_title="Spring Range Announcement",
            evidence_date="2026-07-22",
            confidence=4,
        )
        service.add(
            "another-company",
            category="Market",
            claim="Separate company evidence.",
            confidence=2,
        )

        items = service.for_company(company_id)
        assert [item.evidence_id for item in items] == [
            overview.evidence_id,
            launch.evidence_id,
        ]
        assert service.for_company(company_id, "Product Launch") == [launch]
        summary = service.summary(company_id)
        assert summary == {
            "total": 2,
            "high_confidence": 2,
            "sourced": 2,
            "categories": 2,
        }

        reloaded = ResearchEvidenceService(store)
        assert len(reloaded.for_company(company_id)) == 2
        saved = reloaded.for_company(company_id)[0]
        assert saved.source_title == "About Acme"
        assert saved.confidence == 5
        assert saved.notes == "Confirmed on the official website."
        reloaded.remove(launch.evidence_id)
        assert len(reloaded.for_company(company_id)) == 1

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    company_window = (
        PROJECT_ROOT / "src/ui/company_profile_window.py"
    ).read_text(encoding="utf-8")
    evidence_window = (
        PROJECT_ROOT / "src/ui/research_evidence_window.py"
    ).read_text(encoding="utf-8")
    assert "ResearchEvidenceService" in main_window
    assert "Research Evidence" in company_window
    assert "Add Evidence" in evidence_window
    assert "Open Source" in evidence_window
    assert "Confidence:" in evidence_window
    assert VERSION_INFO.package == "Package-023A-02"
    assert VERSION_INFO.build == 2

    print("Phase 5 research evidence test passed.")


if __name__ == "__main__":
    main()
