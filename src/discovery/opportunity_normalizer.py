"""Convert raw discovery dictionaries into Opportunity model objects."""

from __future__ import annotations

from typing import Any

from src.models.opportunity import Opportunity


class OpportunityNormalizer:
    """Build a consistent Opportunity object from source-specific raw data."""

    TITLE_KEYS = ("title", "name", "headline")
    URL_KEYS = ("url", "link", "href")
    SNIPPET_KEYS = ("snippet", "description", "summary", "text")

    def normalize(
        self,
        raw_item: dict[str, Any],
        *,
        source_name: str,
    ) -> Opportunity:
        opportunity = Opportunity(
            title=self._first_text(raw_item, self.TITLE_KEYS),
            url=self._first_text(raw_item, self.URL_KEYS),
            snippet=self._first_text(raw_item, self.SNIPPET_KEYS),
            source=source_name,
        )

        opportunity.metadata["raw_result"] = dict(raw_item)
        return opportunity

    @staticmethod
    def _first_text(
        raw_item: dict[str, Any],
        keys: tuple[str, ...],
    ) -> str:
        for key in keys:
            value = raw_item.get(key)
            if value is None:
                continue

            text = str(value).strip()
            if text:
                return text

        return ""
