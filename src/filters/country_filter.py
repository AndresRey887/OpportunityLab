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
    AUSTRALIAN_ELIGIBILITY_TERMS = {
        "australian organisations",
        "australian organizations",
        "australian charities",
        "australian not-for-profits",
        "australian nonprofits",
        "eligible in australia",
        "open to australian",
        "applicants in australia",
        "available across australia",
        "australia-wide",
        "australia and new zealand",
    }
    FOREIGN_LOCATION_TERMS = {
        "solomon islands",
        "new zealand",
        "papua new guinea",
        "fiji",
        "vanuatu",
        "samoa",
        "tonga",
        "kiribati",
        "tuvalu",
        "nauru",
        "palau",
        "micronesia",
        "marshall islands",
        "timor-leste",
        "east timor",
        "indonesia",
        "malaysia",
        "singapore",
        "philippines",
        "vietnam",
        "thailand",
        "cambodia",
        "laos",
        "myanmar",
        "india",
        "pakistan",
        "bangladesh",
        "sri lanka",
        "nepal",
        "china",
        "japan",
        "south korea",
        "united states",
        "usa",
        "canada",
        "united kingdom",
        "england",
        "scotland",
        "wales",
        "ireland",
        "europe",
        "africa",
        "middle east",
    }

    def __init__(self) -> None:
        super().__init__("Outside Australia")
        self.country = "Australia"
        self.enabled = False

    def accepts(self, opportunity) -> bool:
        country = str(getattr(opportunity, "country", "") or "").casefold()
        if country:
            return country in {"australia", "au", "aus"}

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
        foreign_target = any(
            term in text for term in self.FOREIGN_LOCATION_TERMS
        )
        australian_eligibility = any(
            term in text for term in self.AUSTRALIAN_ELIGIBILITY_TERMS
        )
        if foreign_target and not australian_eligibility:
            return False

        domain = str(getattr(opportunity, "domain", "") or "").casefold()
        if domain == "au" or domain.endswith(".au"):
            return True

        return any(term in text for term in self.AUSTRALIAN_TERMS)
