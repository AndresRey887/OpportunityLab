"""Identify companies with credible charity-support history."""

from __future__ import annotations

import re


class SupporterProspectRule:
    SUPPORT_TERMS = {
        "charity partner",
        "community partner",
        "corporate giving",
        "community investment",
        "supported charities",
        "supports charities",
        "donated to",
        "donation to",
        "sponsored",
        "sponsorship",
        "workplace giving",
        "matched giving",
        "philanthropy",
    }
    HISTORY_EVIDENCE_TERMS = {
        "annual report",
        "impact report",
        "community report",
        "case study",
        "media release",
        "our partners",
        "we donated",
        "we supported",
        "has donated",
        "has supported",
    }
    CONTACT_TERMS = {
        "community partnerships team",
        "partnership enquiries",
        "sponsorship request",
        "contact us",
        "expressions of interest",
        "apply for support",
        "request support",
    }
    SUPPORT_TYPE_TERMS = {
        "cash donation",
        "cash grant",
        "product donation",
        "donated products",
        "in-kind",
        "in kind",
        "pro bono",
        "employee volunteering",
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
            opportunity.add_rule_result(
                "Supporter Prospect",
                0,
                "No active nonprofit profile.",
            )
            return 0

        text = (
            f"{opportunity.title} {opportunity.snippet}"
        ).casefold()
        support = self._matches(text, self.SUPPORT_TERMS)
        history = self._matches(text, self.HISTORY_EVIDENCE_TERMS)
        contact = self._matches(text, self.CONTACT_TERMS)
        support_type = self._matches(text, self.SUPPORT_TYPE_TERMS)
        profile_matches = sorted(
            term for term in self._profile_terms(profile) if term in text
        )

        points = 0
        reasons = []
        if support:
            points += 15
            reasons.append("Public charity-support language found.")
        if history:
            points += 10
            reasons.append("Past-support or reporting evidence found.")
        if contact:
            points += 8
            reasons.append("A partnership or support contact path was found.")
        if support_type:
            points += 5
            reasons.append("Cash, product, service, or volunteer support found.")
        if profile_matches:
            points += min(len(profile_matches) * 2, 10)
            reasons.append(
                "Profile relevance: " + ", ".join(profile_matches[:5]) + "."
            )

        if support and history and contact:
            prospect_type = "Contactable Supporter"
        elif support and history:
            prospect_type = "Support History"
        elif support and profile_matches:
            prospect_type = "Relevant Supporter"
        elif support:
            prospect_type = "Possible Supporter"
        else:
            prospect_type = ""

        points = min(points, 43)
        if prospect_type:
            reasons.append(
                "Current availability is unconfirmed; verify before contact."
            )
            opportunity.metadata["supporter_prospect_type"] = prospect_type
            opportunity.metadata["supporter_prospect_reasons"] = list(reasons)
            opportunity.metadata["supporter_prospect_points"] = points

        opportunity.add_rule_result(
            "Supporter Prospect",
            points,
            " ".join(reasons) if reasons else "No supporter evidence found.",
        )
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
    def _matches(text: str, terms: set[str]) -> bool:
        return any(term in text for term in terms)
