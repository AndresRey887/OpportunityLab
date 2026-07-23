"""Summarise decision accuracy, patterns, outcomes, and evidence gaps."""

from __future__ import annotations

from collections import Counter

from src.review.decision_pattern import DecisionPattern


class DecisionReviewService:
    def __init__(
        self,
        memory_service,
        outcome_service,
        feedback_service,
        duplicate_cluster_service,
    ) -> None:
        self.memory = memory_service
        self.outcomes = outcome_service
        self.feedback = feedback_service
        self.clusters = duplicate_cluster_service

    def summary(self) -> dict[str, int | float]:
        tracked = self.memory.tracking_service.records
        decided = [
            outcome for outcome in self.outcomes.records
            if outcome.result != "Undecided"
        ]
        successful = [
            outcome for outcome in decided
            if outcome.result == "Successful"
        ]
        feedback_total = len(self.feedback.feedback)
        helpful = sum(item.helpful for item in self.feedback.feedback)
        duplicate_families = len(self.clusters.find_clusters(tracked))
        return {
            "tracked": len(tracked),
            "decided": len(decided),
            "successful": len(successful),
            "success_rate": (
                round(len(successful) / len(decided) * 100)
                if decided else 0
            ),
            "feedback_total": feedback_total,
            "helpful_feedback": helpful,
            "recommendation_accuracy": (
                round(helpful / feedback_total * 100)
                if feedback_total else 0
            ),
            "duplicate_families": duplicate_families,
            "average_rating": (
                round(sum(item.rating for item in tracked) / len(tracked), 1)
                if tracked else 0.0
            ),
        }

    def outcome_totals(self) -> dict[str, int]:
        totals = Counter(outcome.result for outcome in self.outcomes.records)
        return {
            result: totals.get(result, 0)
            for result in (
                "Undecided",
                "Successful",
                "Unsuccessful",
                "Withdrawn",
                "Expired",
            )
        }

    def strong_patterns(self, limit: int = 8) -> list[DecisionPattern]:
        patterns = self._all_patterns()
        strong = [
            pattern for pattern in patterns
            if (
                pattern.average_rating >= 3.5
                or pattern.success_rate >= 60
                or pattern.strength >= 85
            )
        ]
        return sorted(
            strong,
            key=lambda item: (
                item.strength,
                item.success_rate,
                item.tracked_count,
            ),
            reverse=True,
        )[:limit]

    def weak_patterns(self, limit: int = 8) -> list[DecisionPattern]:
        patterns = self._all_patterns()
        weak = [
            pattern for pattern in patterns
            if (
                pattern.average_rating <= 2
                or (
                    pattern.decided_count
                    and pattern.success_rate <= 25
                )
            )
        ]
        return sorted(
            weak,
            key=lambda item: (
                item.average_rating,
                item.success_rate,
                -item.tracked_count,
            ),
        )[:limit]

    def evidence_gaps(self) -> list[str]:
        summary = self.summary()
        gaps = []
        if summary["tracked"] < 10:
            gaps.append(
                f"Only {summary['tracked']} opportunities are tracked; "
                "10 or more will make patterns more reliable."
            )
        if summary["decided"] < 5:
            gaps.append(
                f"Only {summary['decided']} completed outcomes are recorded; "
                "record at least 5 to improve success learning."
            )
        if summary["feedback_total"] < 5:
            gaps.append(
                f"Only {summary['feedback_total']} recommendation feedback "
                "responses are recorded; use Helpful or Not Helpful more often."
            )
        for profile in self.memory.source_profiles():
            if profile.tracked_count >= 2 and profile.decided_count == 0:
                gaps.append(
                    f"{profile.label} has {profile.tracked_count} tracked "
                    "results but no completed outcomes."
                )
        if not gaps:
            gaps.append(
                "No major evidence gaps detected. Continue recording outcomes "
                "and recommendation feedback."
            )
        return gaps

    def lessons(self, limit: int = 8) -> list[str]:
        records = sorted(
            (
                outcome for outcome in self.outcomes.records
                if outcome.lessons_learned
            ),
            key=lambda item: item.updated_at,
            reverse=True,
        )
        return [
            f"{outcome.opportunity_title}: {outcome.lessons_learned}"
            for outcome in records[:limit]
        ]

    def _all_patterns(self) -> list[DecisionPattern]:
        groups = (
            ("Source", self.memory.source_profiles()),
            ("Keyword", self.memory.keyword_profiles()),
            ("Type", self.memory.opportunity_type_profiles()),
        )
        patterns = []
        for category, profiles in groups:
            patterns.extend(
                DecisionPattern(
                    category=category,
                    label=profile.label,
                    strength=profile.strength,
                    tracked_count=profile.tracked_count,
                    average_score=profile.average_score,
                    average_rating=profile.average_rating,
                    success_rate=profile.success_rate,
                    decided_count=profile.decided_count,
                )
                for profile in profiles
            )
        return patterns
