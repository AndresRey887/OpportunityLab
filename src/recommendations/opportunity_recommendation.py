"""Explainable recommendation for one opportunity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OpportunityRecommendation:
    label: str
    match_score: int
    confidence: int
    reasons: tuple[str, ...]
    cautions: tuple[str, ...]
    evidence_count: int
