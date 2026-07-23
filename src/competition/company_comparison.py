"""Side-by-side intelligence summary for two companies."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyComparison:
    company: object
    competitor: object
    link: object
    company_evidence: dict[str, int]
    competitor_evidence: dict[str, int]
