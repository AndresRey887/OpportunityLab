"""Score whether a result contains useful, actionable evidence."""

from __future__ import annotations

import re
from urllib.parse import urlparse


class EvidenceQualityRule:
    ACTION_TERMS = {
        "apply now",
        "apply online",
        "application form",
        "applications open",
        "contact us",
        "expressions of interest",
        "submit an application",
    }
    ELIGIBILITY_TERMS = {
        "eligibility",
        "eligible",
        "who can apply",
        "selection criteria",
        "assessment criteria",
    }
    DEADLINE_TERMS = {
        "closing date",
        "applications close",
        "deadline",
        "funding round closes",
    }
    CLOSED_TERMS = {
        "applications closed",
        "closed for applications",
        "grant closed",
        "expired",
        "no longer accepting",
    }
    GENERAL_CONTENT_TERMS = {
        "how to",
        "tips for",
        "podcast",
        "webinar",
        "explained",
        "news update",
    }

    def evaluate(self, opportunity) -> int:
        title = str(getattr(opportunity, "title", "") or "")
        snippet = str(getattr(opportunity, "snippet", "") or "")
        source = str(getattr(opportunity, "source", "") or "")
        url = str(getattr(opportunity, "url", "") or "")
        text = f"{title} {snippet}".casefold()
        domain = (urlparse(url).hostname or "").casefold()
        path = (urlparse(url).path or "").casefold()

        points = 0
        reasons = []

        is_video = (
            source.casefold() == "youtube"
            or domain.endswith("youtube.com")
            or domain == "youtu.be"
        )
        official_domain = (
            domain.endswith(".gov.au")
            or domain.endswith(".org.au")
            or source.casefold() == "company websites"
        )
        grant_page = any(
            term in f"{title.casefold()} {path}"
            for term in ("grant", "funding", "sponsor", "donat", "apply")
        )
        action = self._contains_any(text, self.ACTION_TERMS)
        eligibility = self._contains_any(text, self.ELIGIBILITY_TERMS)
        deadline = self._contains_any(text, self.DEADLINE_TERMS)
        closed = self._contains_any(text, self.CLOSED_TERMS)
        amount = bool(
            re.search(
                r"(?:\\$\\s?\\d[\\d,]*(?:\\.\\d+)?|"
                r"funding (?:of|up to)|grants? (?:of|up to|between))",
                text,
            )
        )

        if official_domain and grant_page:
            points += 20
            reasons.append("Official or organisation opportunity page.")
        if eligibility:
            points += 10
            reasons.append("Eligibility or assessment criteria found.")
        if amount:
            points += 10
            reasons.append("Funding amount found.")
        if deadline:
            points += 10
            reasons.append("Closing-date information found.")
        if action:
            points += 10
            reasons.append("Clear application or contact action found.")

        if is_video:
            points -= 20
            reasons.append("Video result without primary application evidence.")
        elif self._contains_any(text, self.GENERAL_CONTENT_TERMS):
            points -= 10
            reasons.append("General information rather than a direct opportunity.")

        if closed:
            points -= 25
            reasons.append("Opportunity appears closed or expired.")
        elif not action:
            points -= 10
            reasons.append("No clear application or contact action found.")

        points = max(-35, min(points, 60))
        if points >= 30:
            tier = "Strong Evidence"
        elif points >= 10:
            tier = "Useful Evidence"
        elif points >= 0:
            tier = "Limited Evidence"
        else:
            tier = "Weak Evidence"

        opportunity.metadata["evidence_quality_tier"] = tier
        opportunity.metadata["evidence_quality_points"] = points
        opportunity.metadata["evidence_quality_reasons"] = list(reasons)
        opportunity.add_rule_result(
            "Evidence Quality",
            points,
            " ".join(reasons),
        )
        return points

    @staticmethod
    def _contains_any(text: str, terms: set[str]) -> bool:
        return any(term in text for term in terms)
