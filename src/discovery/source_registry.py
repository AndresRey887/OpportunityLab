"""Registry for OpportunityLab discovery sources."""

from __future__ import annotations

from collections.abc import Iterable

from src.discovery.search_source import SearchSource


class SourceRegistry:
    """Store discovery sources and control which sources are enabled."""

    def __init__(self, sources: Iterable[SearchSource] | None = None) -> None:
        self._sources: dict[str, SearchSource] = {}
        self._enabled: set[str] = set()

        if sources is not None:
            for source in sources:
                self.register(source)

    def register(self, source: SearchSource, *, enabled: bool = True) -> None:
        """Register or replace a source by name."""
        self._sources[source.name] = source

        if enabled:
            self._enabled.add(source.name)
        else:
            self._enabled.discard(source.name)

    def unregister(self, name: str) -> None:
        """Remove a source from the registry."""
        self._sources.pop(name, None)
        self._enabled.discard(name)

    def enable(self, name: str) -> None:
        """Enable a registered source."""
        if name not in self._sources:
            raise KeyError(f"Unknown discovery source: {name}")
        self._enabled.add(name)

    def disable(self, name: str) -> None:
        """Disable a registered source without removing it."""
        if name not in self._sources:
            raise KeyError(f"Unknown discovery source: {name}")
        self._enabled.discard(name)

    def is_enabled(self, name: str) -> bool:
        """Return whether a registered source is enabled."""
        return name in self._enabled

    def get(self, name: str) -> SearchSource:
        """Return a registered source by name."""
        try:
            return self._sources[name]
        except KeyError as error:
            raise KeyError(f"Unknown discovery source: {name}") from error

    def all_sources(self) -> list[SearchSource]:
        """Return every registered source in registration order."""
        return list(self._sources.values())

    def enabled_sources(self) -> list[SearchSource]:
        """Return enabled sources in registration order."""
        return [
            source
            for name, source in self._sources.items()
            if name in self._enabled
        ]
