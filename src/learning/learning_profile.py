"""Performance profile for a source, keyword, or opportunity type."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningProfile:
    label: str
    tracked_count: int
    average_score: int
    average_rating: float
    decided_count: int
    success_count: int
    success_rate: int
    strength: int
