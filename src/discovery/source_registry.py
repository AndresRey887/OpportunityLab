"""Registry for OpportunityLab discovery sources."""

from __future__ import annotations

from collections.abc import Iterable

from src.discovery.search_source import SearchSource


class SourceRegistry:
    """Store discovery sources and control which sources are enabled."""

    def __init__(
        self,
        sources: Iterable[SearchSource] | None = None,
    ) -> None:
        self._sources: dict[str, SearchSource] = {}
        self._enabled: set[str] = set()

        if sources is not None:
            for source in sources:
                self.register(source)

    def register(
        self,
        source: SearchSource,
        *,
        enabled: bool = True,
    ) -> None:
        self._sources[source.name] = source

        if enabled:
            self._enabled.add(source.name)
        else:
            self._enabled.discard(source.name)

    def unregister(self, name: str) -> None:
        self._sources.pop(name, None)
        self._enabled.discard(name)

    def get(self, name: str) -> SearchSource:
        try:
            return self._sources[name]
        except KeyError as error:
            raise KeyError(name) from error

    def all_sources(self) -> list[SearchSource]:
        return list(self._sources.values())

    def all_names(self) -> list[str]:
        return list(self._sources)

    def enabled_sources(self) -> list[SearchSource]:
        return [
            source
            for name, source in self._sources.items()
            if name in self._enabled
        ]

    def enabled_names(self) -> list[str]:
        return [
            name
            for name in self._sources
            if name in self._enabled
        ]

    def disabled_names(self) -> list[str]:
        return [
            name
            for name in self._sources
            if name not in self._enabled
        ]

    def is_enabled(self, name: str) -> bool:
        if name not in self._sources:
            raise KeyError(name)

        return name in self._enabled

    def enable(self, name: str) -> None:
        if name not in self._sources:
            raise KeyError(name)

        self._enabled.add(name)

    def disable(self, name: str) -> None:
        if name not in self._sources:
            raise KeyError(name)

        self._enabled.discard(name)

    def set_enabled(self, names: Iterable[str]) -> None:
        requested = set(names)
        self._enabled = {
            name
            for name in self._sources
            if name in requested
        }
