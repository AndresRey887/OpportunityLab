"""Manage competitor links and create side-by-side comparisons."""

from __future__ import annotations

from src.competition.company_comparison import CompanyComparison
from src.competition.competitor_link import CompetitorLink
from src.competition.competitor_store import CompetitorStore


class CompetitorService:
    def __init__(self, store: CompetitorStore | None = None) -> None:
        self.store = store or CompetitorStore()
        self.links = self.store.load()

    def link(
        self,
        company_id: str,
        competitor_company_id: str,
        *,
        market_overlap: str = "",
        strength=3,
        notes: str = "",
    ) -> tuple[CompetitorLink, bool]:
        existing = self.find_link(company_id, competitor_company_id)
        if existing:
            existing.market_overlap = str(market_overlap).strip()
            existing.strength = max(1, min(int(strength), 5))
            existing.notes = str(notes).strip()
            self.store.save(self.links)
            return existing, False
        link = CompetitorLink(
            company_id=company_id,
            competitor_company_id=competitor_company_id,
            market_overlap=market_overlap,
            strength=int(strength),
            notes=notes,
        )
        self.links.append(link)
        self.store.save(self.links)
        return link, True

    def for_company(self, company_id: str) -> list[CompetitorLink]:
        return [
            link for link in self.links
            if (
                link.company_id == company_id
                or link.competitor_company_id == company_id
            )
        ]

    def find_link(
        self,
        first_company_id: str,
        second_company_id: str,
    ) -> CompetitorLink | None:
        target = {first_company_id, second_company_id}
        return next(
            (
                link for link in self.links
                if {
                    link.company_id,
                    link.competitor_company_id,
                } == target
            ),
            None,
        )

    def comparisons(
        self,
        company_id: str,
        company_service,
        evidence_service,
    ) -> list[CompanyComparison]:
        company = company_service.get(company_id)
        comparisons = []
        for link in self.for_company(company_id):
            competitor_id = (
                link.competitor_company_id
                if link.company_id == company_id
                else link.company_id
            )
            try:
                competitor = company_service.get(competitor_id)
            except KeyError:
                continue
            comparisons.append(
                CompanyComparison(
                    company=company,
                    competitor=competitor,
                    link=link,
                    company_evidence=evidence_service.summary(company_id),
                    competitor_evidence=evidence_service.summary(competitor_id),
                )
            )
        return sorted(
            comparisons,
            key=lambda item: (item.link.strength, item.competitor.name),
            reverse=True,
        )

    def remove(self, link_id: str) -> None:
        original_count = len(self.links)
        self.links = [
            link for link in self.links
            if link.link_id != link_id
        ]
        if len(self.links) == original_count:
            raise KeyError(link_id)
        self.store.save(self.links)
