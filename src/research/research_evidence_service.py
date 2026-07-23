"""Manage sourced research evidence for company profiles."""

from __future__ import annotations

from src.research.research_evidence import ResearchEvidence
from src.research.research_evidence_store import ResearchEvidenceStore


class ResearchEvidenceService:
    def __init__(
        self,
        store: ResearchEvidenceStore | None = None,
    ) -> None:
        self.store = store or ResearchEvidenceStore()
        self.evidence = self.store.load()

    def for_company(
        self,
        company_id: str,
        category: str = "All",
    ) -> list[ResearchEvidence]:
        items = [
            item for item in self.evidence
            if item.company_id == company_id
        ]
        if category != "All":
            items = [item for item in items if item.category == category]
        return sorted(
            items,
            key=lambda item: (item.evidence_date, item.created_at),
            reverse=True,
        )

    def add(
        self,
        company_id: str,
        *,
        category: str,
        claim: str,
        source_url: str = "",
        source_title: str = "",
        evidence_date: str = "",
        confidence=3,
        notes: str = "",
    ) -> ResearchEvidence:
        item = ResearchEvidence(
            company_id=company_id,
            category=category,
            claim=claim,
            source_url=str(source_url).strip(),
            source_title=str(source_title).strip(),
            **({"evidence_date": evidence_date} if evidence_date else {}),
            confidence=int(confidence),
            notes=str(notes).strip(),
        )
        self.evidence.append(item)
        self.store.save(self.evidence)
        return item

    def remove(self, evidence_id: str) -> None:
        original_count = len(self.evidence)
        self.evidence = [
            item for item in self.evidence
            if item.evidence_id != evidence_id
        ]
        if len(self.evidence) == original_count:
            raise KeyError(evidence_id)
        self.store.save(self.evidence)

    def summary(self, company_id: str) -> dict[str, int]:
        items = self.for_company(company_id)
        return {
            "total": len(items),
            "high_confidence": sum(item.confidence >= 4 for item in items),
            "sourced": sum(bool(item.source_url) for item in items),
            "categories": len({item.category for item in items}),
        }
