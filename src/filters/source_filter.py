"""Filter opportunities by discovery source."""

from src.filters.filter import Filter


class SourceFilter(Filter):
    """Accept every source unless an allowed-source list is configured."""

    def __init__(self) -> None:
        super().__init__("Source filter")
        self.allowed_sources: set[str] = set()

    def accepts(self, opportunity) -> bool:
        if not self.allowed_sources:
            return True

        source = str(getattr(opportunity, "source", "")).strip().casefold()
        return source in self.allowed_sources

    def reason(self) -> str:
        return "Source not selected"

    def set_allowed_sources(self, sources) -> None:
        self.allowed_sources = {
            str(source).strip().casefold()
            for source in sources
            if str(source).strip()
        }

    def clear_allowed_sources(self) -> None:
        self.allowed_sources.clear()
