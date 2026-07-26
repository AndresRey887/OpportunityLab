"""Score opportunities against the active nonprofit profile."""

from __future__ import annotations

import re


class ProfileOpportunityRule:
    FUNDING_TERMS = {
        "grant",
        "funding",
        "sponsorship",
        "donation",
        "donate",
        "community grant",
        "foundation",
        "in-kind",
        "in kind",
    }
    RELATIONSHIP_TERMS = {
        "community partner",
        "charity partner",
        "corporate giving",
        "social impact",
        "community support",
        "supports charities",
        "philanthropy",
    }
    ACTION_TERMS = {
        "apply",
        "applications open",
        "eligibility",
        "expression of interest",
        "contact us",
        "funding round",
    }
    CLOSED_TERMS = {
        "applications closed",
        "grant closed",
        "expired",
        "no longer accepting",
    }
    STOP_WORDS = {
        "about", "and", "for", "from", "into", "our", "the", "their",
        "this", "through", "with",
    }

    def __init__(self, profile_service=None) -> None:
        self.profile_service = profile_service

    def evaluate(self, opportunity) -> int:
        profile = (
            self.profile_service.active_profile
            if self.profile_service is not None
            else None
        )
        if profile is None or not profile.is_nonprofit:
            opportunity.add_rule_result("Nonprofit Profile Fit", 0)
            return 0

        text = f"{opportunity.title} {opportunity.snippet}".casefold()
        funding = self._contains_any(text, self.FUNDING_TERMS)
        relationship = self._contains_any(text, self.RELATIONSHIP_TERMS)
        action = self._contains_any(text, self.ACTION_TERMS)
        closed = self._contains_any(text, self.CLOSED_TERMS)

        points = 0
        if funding:
            points += 12
        if relationship:
            points += 8
        if action:
            points += 5
        if closed:
            points -= 12

        profile_terms = self._profile_terms(profile)
        matches = sum(term in text for term in profile_terms)
        points += min(matches * 2, 10)

        location = str(profile.service_area or "").strip().casefold()
        if location and location in text:
            points += 5

        if closed:
            classification = "Weak Lead"
        elif funding and action:
            classification = "Open Opportunity"
        elif funding:
            classification = "Funding Prospect"
        elif relationship:
            classification = "Relationship Lead"
        else:
            classification = "Weak Lead"

        points = max(-12, min(points, 35))
        opportunity.metadata["profile_fit_type"] = classification
        opportunity.metadata["profile_name"] = profile.name
        opportunity.add_rule_result("Nonprofit Profile Fit", points)
        return points

    def _profile_terms(self, profile) -> set[str]:
        words = re.findall(
            r"[a-z0-9]{4,}",
            " ".join(
                (
                    profile.mission,
                    profile.beneficiaries,
                    profile.support_needs,
                )
            ).casefold(),
        )
        return {word for word in words if word not in self.STOP_WORDS}

    @staticmethod
    def _contains_any(text: str, terms: set[str]) -> bool:
        return any(term in text for term in terms)
