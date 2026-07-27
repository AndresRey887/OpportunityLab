"""Read opportunity webpages and verify profile-location eligibility."""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser

import requests


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts = []
        self.ignored_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg"}:
            self.ignored_depth += 1
        elif tag in {"p", "div", "li", "br", "tr", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg"}:
            self.ignored_depth = max(0, self.ignored_depth - 1)

    def handle_data(self, data):
        if not self.ignored_depth:
            self.parts.append(data)

    def text(self) -> str:
        return " ".join("".join(self.parts).split())


class PageEvidenceService:
    ELIGIBILITY_TERMS = {
        "eligible",
        "eligibility",
        "who can apply",
        "applicant",
        "applications are open to",
        "available to",
    }
    LOCATION_RESTRICTION_TERMS = {
        "eligible area",
        "local government area",
        " lga",
        "council area",
        "must be based in",
        "must be located in",
        "located within",
        "residents of",
        "operating in",
        "organisations in",
        "organizations in",
    }
    NATIONAL_TERMS = {
        "across australia",
        "australia-wide",
        "anywhere in australia",
        "throughout australia",
        "nationally",
        "australian organisations",
        "australian organizations",
        "australian charities",
        "all australian states",
    }

    def __init__(self, timeout_seconds=8, max_workers=6) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_workers = max_workers

    def verify_all(self, opportunities, profile, limit=20):
        ordered = sorted(
            opportunities,
            key=lambda item: getattr(item, "score", 0),
            reverse=True,
        )
        selected = ordered[:max(0, int(limit))]
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.verify, opportunity, profile): opportunity
                for opportunity in selected
            }
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as error:
                    self._unverified(
                        futures[future],
                        profile,
                        f"Page verification failed: {error}",
                    )

        for opportunity in ordered[len(selected):]:
            self._unverified(
                opportunity,
                profile,
                "Not checked at the selected search depth.",
            )
        return opportunities

    def verify(self, opportunity, profile):
        profile_location = self._profile_location(profile)
        opportunity.metadata["profile_location"] = profile_location
        if not profile_location:
            return self._unverified(
                opportunity,
                profile,
                "Add an address or service area to the active profile.",
            )

        url = str(getattr(opportunity, "url", "") or "").strip()
        if not url or "youtube.com" in url or "reddit.com" in url:
            return self._unverified(
                opportunity,
                profile,
                "The result does not provide a suitable official webpage.",
            )

        response = requests.get(
            url,
            headers={"User-Agent": "OpportunityLab/1.1"},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        content_type = str(response.headers.get("Content-Type", "")).casefold()
        if "html" not in content_type and "text" not in content_type:
            return self._unverified(
                opportunity,
                profile,
                "The webpage format could not be read automatically.",
            )

        parser = _TextExtractor()
        parser.feed(response.text[:750_000])
        page_text = parser.text()[:25_000]
        excerpts = self._eligibility_excerpts(page_text)
        status, reason = self._classify(profile_location, excerpts)

        opportunity.metadata["page_evidence_text"] = page_text[:12_000]
        opportunity.metadata["page_evidence_excerpts"] = excerpts
        opportunity.metadata["profile_eligibility_status"] = status
        opportunity.metadata["profile_eligibility_reason"] = reason

        if status == "Eligible":
            opportunity.score = min(100, opportunity.score + 8)
            opportunity.add_rule_result(
                "Profile Location Eligibility",
                8,
                reason,
            )
        elif status == "Ineligible":
            opportunity.score = max(0, opportunity.score - 50)
            opportunity.add_rule_result(
                "Profile Location Eligibility",
                -50,
                reason,
            )
        else:
            opportunity.add_rule_result(
                "Profile Location Eligibility",
                0,
                reason,
            )
        return opportunity

    def _unverified(self, opportunity, profile, reason):
        opportunity.metadata["profile_location"] = self._profile_location(profile)
        opportunity.metadata["profile_eligibility_status"] = "Unverified"
        opportunity.metadata["profile_eligibility_reason"] = reason
        opportunity.metadata.setdefault("page_evidence_text", "")
        opportunity.metadata.setdefault("page_evidence_excerpts", [])
        return opportunity

    def _classify(self, profile_location, excerpts):
        if not excerpts:
            return "Unverified", "No clear location eligibility text was found."

        location = profile_location.casefold()
        tokens = {
            token
            for token in re.findall(r"[a-z]{4,}", location)
            if token not in {
                "australia",
                "australian",
                "regional",
                "service",
                "area",
            }
        }
        joined = " ".join(excerpts).casefold()
        restricted = [
            excerpt
            for excerpt in excerpts
            if any(
                term in f" {excerpt.casefold()}"
                for term in self.LOCATION_RESTRICTION_TERMS
            )
        ]
        if restricted:
            restricted_text = " ".join(restricted).casefold()
            if tokens and any(token in restricted_text for token in tokens):
                return "Eligible", f"Page eligibility matches {profile_location}."
            if any(term in restricted_text for term in self.NATIONAL_TERMS):
                return "Eligible", f"Page eligibility includes {profile_location}."
            return (
                "Ineligible",
                (
                    f"Location rules do not include {profile_location}: "
                    f"{restricted[0][:280]}"
                ),
            )
        if any(term in joined for term in self.NATIONAL_TERMS):
            return "Eligible", f"Page eligibility includes {profile_location}."
        if tokens and any(token in joined for token in tokens):
            return "Eligible", f"Page eligibility matches {profile_location}."
        return "Unverified", "Location eligibility is unclear on the webpage."

    def _eligibility_excerpts(self, text):
        chunks = re.split(r"(?<=[.!?])\s+|\s*[|•]\s*", text)
        excerpts = []
        for chunk in chunks:
            cleaned = " ".join(chunk.split())
            lowered = cleaned.casefold()
            if (
                20 <= len(cleaned) <= 600
                and (
                    any(term in lowered for term in self.ELIGIBILITY_TERMS)
                    or any(
                        term in f" {lowered}"
                        for term in self.LOCATION_RESTRICTION_TERMS
                    )
                )
            ):
                excerpts.append(cleaned)
            if len(excerpts) >= 12:
                break
        return excerpts

    @staticmethod
    def _profile_location(profile) -> str:
        parts = [
            str(getattr(profile, "address", "") or "").strip(),
            str(getattr(profile, "service_area", "") or "").strip(),
        ]
        unique = []
        for part in parts:
            if part and part.casefold() not in {item.casefold() for item in unique}:
                unique.append(part)
        return ", ".join(unique)
