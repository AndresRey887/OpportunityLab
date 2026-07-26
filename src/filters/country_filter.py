"""Filter discovery results to opportunities with Australian evidence."""

from __future__ import annotations

from src.filters.filter import Filter


class CountryFilter(Filter):
    AUSTRALIAN_TERMS = {
        "australia",
        "australian",
        "victoria",
        "victorian",
        "new south wales",
        "queensland",
        "south australia",
        "western australia",
        "tasmania",
        "northern territory",
        "australian capital territory",
        "melbourne",
        "sydney",
        "brisbane",
        "adelaide",
        "perth",
        "hobart",
        "darwin",
        "canberra",
    }

    def __init__(self) -> None:
        super().__init__("Outside Australia")
        self.country = "Australia"
        self.enabled = False

    def accepts(self, opportunity) -> bool:
        country = str(getattr(opportunity, "country", "") or "").casefold()
        if country:
            return country in {"australia", "au", "aus"}

        domain = str(getattr(opportunity, "domain", "") or "").casefold()
        if domain == "au" or domain.endswith(".au"):
            return True

        metadata = getattr(opportunity, "metadata", {}) or {}
        metadata_country = str(metadata.get("country", "") or "").casefold()
        if metadata_country:
            return metadata_country in {"australia", "au", "aus"}

        text = " ".join(
            (
                str(getattr(opportunity, "title", "") or ""),
                str(getattr(opportunity, "snippet", "") or ""),
                str(metadata.get("location", "") or ""),
            )
        ).casefold()
        return any(term in text for term in self.AUSTRALIAN_TERMS)
