"""A family of discoveries that appear to describe one opportunity."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DuplicateMatch:
    record: object
    confidence: int
    reasons: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DuplicateCluster:
    primary: object
    matches: tuple[DuplicateMatch, ...]

    @property
    def member_count(self) -> int:
        return 1 + len(self.matches)

    @property
    def highest_confidence(self) -> int:
        return max(
            (match.confidence for match in self.matches),
            default=0,
        )
