"""Hide opportunities that clearly exclude the active profile location."""

from src.filters.filter import Filter


class ProfileEligibilityFilter(Filter):
    def __init__(self) -> None:
        super().__init__("Profile location ineligible")

    def accepts(self, opportunity) -> bool:
        metadata = getattr(opportunity, "metadata", {}) or {}
        return metadata.get("profile_eligibility_status") != "Ineligible"
