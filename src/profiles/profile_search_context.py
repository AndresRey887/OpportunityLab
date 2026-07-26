"""Build search intent from the active Personal or Nonprofit profile."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileSearchContext:
    original_query: str
    effective_query: str
    profile_name: str
    profile_type: str
    expanded: bool


class ProfileSearchContextService:
    DEFAULT_NONPROFIT_TERMS = (
        'grant OR sponsorship OR "community partnership" '
        'OR donation OR "in-kind support"'
    )

    def __init__(self, profile_service=None) -> None:
        self.profile_service = profile_service

    def build(self, query: str) -> ProfileSearchContext:
        original = self._clean(query)
        if self.profile_service is None:
            return self._plain(original)
        profile = self.profile_service.active_profile
        if not profile.is_nonprofit:
            return self._plain(original, profile)

        opportunity_terms = self._opportunity_terms(profile.opportunity_types)
        context_terms = [
            self._clean(profile.mission),
            self._clean(profile.beneficiaries),
            self._clean(profile.service_area),
            self._clean(profile.support_needs),
        ]
        parts = [
            original,
            f"({opportunity_terms})",
            *[term for term in context_terms if term],
        ]
        effective = " ".join(parts)[:500].strip()
        return ProfileSearchContext(
            original_query=original,
            effective_query=effective,
            profile_name=profile.name,
            profile_type=profile.profile_type,
            expanded=effective != original,
        )

    def _plain(self, query, profile=None) -> ProfileSearchContext:
        return ProfileSearchContext(
            original_query=query,
            effective_query=query,
            profile_name=getattr(profile, "name", "Personal"),
            profile_type=getattr(profile, "profile_type", "Personal"),
            expanded=False,
        )

    def _opportunity_terms(self, value: str) -> str:
        requested = [
            self._clean(item)
            for item in re.split(r"[,;]", str(value or ""))
            if self._clean(item)
        ]
        if not requested:
            return self.DEFAULT_NONPROFIT_TERMS
        return " OR ".join(f'"{item}"' if " " in item else item for item in requested)

    @staticmethod
    def _clean(value: object) -> str:
        return " ".join(str(value or "").replace('"', "").split())
