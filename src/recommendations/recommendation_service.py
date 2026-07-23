"""Score opportunities using current quality and learned history."""

from __future__ import annotations

import re

from src.recommendations.opportunity_recommendation import (
    OpportunityRecommendation,
)


class RecommendationService:
    def __init__(
        self,
        search_memory_service,
        outcome_service,
        feedback_service=None,
    ) -> None:
        self.memory = search_memory_service
        self.outcome_service = outcome_service
        self.feedback_service = feedback_service

    def evaluate(self, opportunity) -> OpportunityRecommendation:
        source_profile = self._source_profile(
            getattr(opportunity, "source", "")
        )
        keywords = self._keywords(
            " ".join(
                (
                    str(getattr(opportunity, "title", "")),
                    str(getattr(opportunity, "snippet", "")),
                    str(
                        getattr(opportunity, "search_query", "")
                        or getattr(opportunity, "metadata", {}).get(
                            "search_query",
                            "",
                        )
                    ),
                )
            )
        )
        keyword_profile = self._best_matching_profile(
            self.memory.keyword_profiles(limit=50),
            keywords,
        )
        type_profile = self._type_profile(keywords)

        current_score = max(
            0,
            min(int(getattr(opportunity, "score", 0) or 0), 100),
        )
        match_score = current_score * 0.45
        if source_profile:
            match_score += min(source_profile.strength, 100) * 0.20
        if keyword_profile:
            match_score += min(keyword_profile.strength, 100) * 0.20
        if type_profile:
            match_score += min(type_profile.strength, 100) * 0.15
        feedback = (
            self.feedback_service.influence(opportunity)
            if self.feedback_service is not None
            else {
                "matching": 0,
                "helpful": 0,
                "unhelpful": 0,
                "score_adjustment": 0,
            }
        )
        match_score += feedback["score_adjustment"]
        match_score = round(max(0, min(match_score, 100)))

        reasons = [f"Current opportunity quality score is {current_score}/100."]
        if source_profile:
            reasons.append(
                f"{source_profile.label} has produced "
                f"{source_profile.tracked_count} tracked result(s) with an "
                f"average rating of {source_profile.average_rating}/5."
            )
            if source_profile.decided_count:
                reasons.append(
                    f"This source has a {source_profile.success_rate}% success "
                    f"rate across recorded outcomes."
                )
        if keyword_profile:
            reasons.append(
                f'The learned keyword "{keyword_profile.label}" has a '
                f"strength score of {keyword_profile.strength}."
            )
        if type_profile:
            reasons.append(
                f"{type_profile.label} is the strongest matching opportunity "
                f"type from previous results."
            )
        if feedback["helpful"] > feedback["unhelpful"]:
            reasons.append(
                f"{feedback['helpful']} helpful feedback response(s) support "
                f"similar recommendations."
            )

        decided_count = sum(
            outcome.result != "Undecided"
            for outcome in self.outcome_service.records
        )
        tracked_count = len(self.memory.tracking_service.records)
        evidence_count = tracked_count + decided_count + feedback["matching"]
        confidence = 15
        confidence += min(tracked_count * 7, 35)
        confidence += min(decided_count * 10, 30)
        confidence += 8 if source_profile else 0
        confidence += 4 if keyword_profile else 0
        confidence += 3 if type_profile else 0
        confidence += min(feedback["matching"] * 3, 10)
        confidence = min(confidence, 95)

        cautions = []
        if tracked_count < 5:
            cautions.append(
                "Limited tracked history: confidence will improve as more "
                "opportunities are rated."
            )
        if decided_count < 3:
            cautions.append(
                "Few completed outcomes are available for success learning."
            )
        if (
            source_profile
            and source_profile.decided_count
            and source_profile.success_rate == 0
        ):
            cautions.append(
                f"{source_profile.label} has no successful recorded outcomes yet."
            )
        if current_score < 50:
            cautions.append("The current opportunity quality score is below 50.")
        if not source_profile and not keyword_profile:
            cautions.append(
                "This source and wording are new to OpportunityLab."
            )
        if feedback["unhelpful"] > feedback["helpful"]:
            cautions.append(
                f"{feedback['unhelpful']} unhelpful feedback response(s) lower "
                f"the score for similar recommendations."
            )

        if match_score >= 75:
            label = "Strong Match"
        elif match_score >= 60:
            label = "Worth Reviewing"
        elif match_score >= 45:
            label = "Possible Fit"
        else:
            label = "Low Priority"

        return OpportunityRecommendation(
            label=label,
            match_score=match_score,
            confidence=confidence,
            reasons=tuple(reasons),
            cautions=tuple(cautions),
            evidence_count=evidence_count,
        )

    def _source_profile(self, source):
        source_key = str(source).casefold()
        return next(
            (
                profile for profile in self.memory.source_profiles()
                if profile.label.casefold() == source_key
            ),
            None,
        )

    @staticmethod
    def _best_matching_profile(profiles, keywords):
        matching = [
            profile for profile in profiles
            if profile.label.casefold() in keywords
        ]
        return matching[0] if matching else None

    def _type_profile(self, keywords):
        matching_names = {
            type_name
            for type_name, type_words in self.memory.TYPE_RULES.items()
            if keywords & type_words
        }
        return next(
            (
                profile
                for profile in self.memory.opportunity_type_profiles()
                if profile.label in matching_names
            ),
            None,
        )

    @classmethod
    def _keywords(cls, text):
        return set(re.findall(r"[a-z0-9]+", str(text).casefold()))
