"""Optional filter for results classified as weak evidence."""

from src.filters.filter import Filter


class WeakEvidenceFilter(Filter):
    def __init__(self) -> None:
        super().__init__("Weak evidence")
        self.enabled = False

    def accepts(self, opportunity) -> bool:
        metadata = getattr(opportunity, "metadata", {}) or {}
        return metadata.get("evidence_quality_tier") != "Weak Evidence"
