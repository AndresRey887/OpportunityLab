"""One strong or weak learned decision pattern."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionPattern:
    category: str
    label: str
    strength: int
    tracked_count: int
    average_score: int
    average_rating: float
    success_rate: int
    decided_count: int
