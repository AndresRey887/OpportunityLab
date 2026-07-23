"""Build learning profiles from tracked opportunities and their outcomes."""

from __future__ import annotations

import re
from collections import defaultdict

from src.learning.learning_profile import LearningProfile


class SearchMemoryService:
    STOP_WORDS = {
        "a", "an", "and", "apply", "australia", "australian", "for", "from",
        "in", "join", "of", "on", "opportunity", "program", "the", "to",
        "with",
    }
    TYPE_RULES = {
        "Product Testing": {"beta", "product", "sample", "test", "testing", "trial"},
        "Business & Supply": {
            "affiliate", "business", "distributor", "partner", "partnership",
            "supplier", "wholesale",
        },
        "Funding & Grants": {"fund", "funding", "grant", "rebate", "support"},
        "Tools & Woodworking": {
            "diy", "tool", "tools", "wood", "woodwork", "woodworking",
        },
        "Camping & Outdoors": {
            "camp", "camping", "fishing", "hiking", "outdoor", "outdoors",
        },
        "Technology": {
            "app", "device", "digital", "electronics", "gadget", "software",
            "technology",
        },
    }

    def __init__(self, tracking_service, outcome_service) -> None:
        self.tracking_service = tracking_service
        self.outcome_service = outcome_service

    def source_profiles(self) -> list[LearningProfile]:
        groups = defaultdict(list)
        for record in self.tracking_service.records:
            groups[record.source or "Unknown"].append(record)
        return self._profiles(groups)

    def keyword_profiles(self, limit: int = 12) -> list[LearningProfile]:
        groups = defaultdict(list)
        for record in self.tracking_service.records:
            text = f"{record.search_query} {record.title}"
            for keyword in set(self._keywords(text)):
                groups[keyword].append(record)
        return self._profiles(groups)[:max(1, int(limit))]

    def opportunity_type_profiles(self) -> list[LearningProfile]:
        groups = defaultdict(list)
        for record in self.tracking_service.records:
            words = set(self._keywords(
                f"{record.search_query} {record.title} {record.snippet}"
            ))
            matched = False
            for type_name, type_words in self.TYPE_RULES.items():
                if words & type_words:
                    groups[type_name].append(record)
                    matched = True
            if not matched:
                groups["Other"].append(record)
        return self._profiles(groups)

    def suggested_searches(self, limit: int = 5) -> list[str]:
        suggestions = []
        for profile in self.keyword_profiles(limit=20):
            if profile.average_rating >= 3 or profile.average_score >= 70:
                suggestions.append(profile.label)
        return suggestions[:max(1, int(limit))]

    def summary(self) -> dict[str, object]:
        source_profiles = self.source_profiles()
        keyword_profiles = self.keyword_profiles()
        type_profiles = self.opportunity_type_profiles()
        return {
            "tracked": len(self.tracking_service.records),
            "top_source": source_profiles[0].label if source_profiles else "Not enough data",
            "top_keyword": keyword_profiles[0].label if keyword_profiles else "Not enough data",
            "top_type": type_profiles[0].label if type_profiles else "Not enough data",
        }

    def _profiles(self, groups) -> list[LearningProfile]:
        profiles = [
            self._build_profile(label, records)
            for label, records in groups.items()
            if records
        ]
        return sorted(
            profiles,
            key=lambda item: (
                item.strength,
                item.tracked_count,
                item.average_rating,
                item.average_score,
            ),
            reverse=True,
        )

    def _build_profile(self, label, records) -> LearningProfile:
        outcomes = []
        for record in records:
            try:
                outcome = self.outcome_service.get(record.tracking_id)
            except KeyError:
                continue
            if outcome.result != "Undecided":
                outcomes.append(outcome)
        success_count = sum(
            outcome.result == "Successful" for outcome in outcomes
        )
        decided_count = len(outcomes)
        success_rate = (
            round(success_count / decided_count * 100)
            if decided_count else 0
        )
        average_score = round(
            sum(record.score for record in records) / len(records)
        )
        average_rating = round(
            sum(record.rating for record in records) / len(records),
            1,
        )
        strength = round(
            average_score * 0.45
            + average_rating * 10
            + success_rate * 0.35
            + min(len(records), 10) * 2
        )
        return LearningProfile(
            label=str(label),
            tracked_count=len(records),
            average_score=average_score,
            average_rating=average_rating,
            decided_count=decided_count,
            success_count=success_count,
            success_rate=success_rate,
            strength=strength,
        )

    @classmethod
    def _keywords(cls, text: str) -> list[str]:
        return [
            word for word in re.findall(r"[a-z0-9]+", str(text).casefold())
            if len(word) >= 3 and word not in cls.STOP_WORDS
        ]
