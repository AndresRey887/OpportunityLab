
from __future__ import annotations
from collections.abc import Iterable
from src.discovery.search_source import SearchSource

class SourceRegistry:
    def __init__(self,sources:Iterable[SearchSource]|None=None)->None:
        self._sources={}
        self._enabled=set()
        if sources:
            for s in sources:
                self.register(s)
    def register(self,source:SearchSource,*,enabled:bool=True)->None:
        self._sources[source.name]=source
        if enabled:self._enabled.add(source.name)
        else:self._enabled.discard(source.name)
    def unregister(self,name:str)->None:
        self._sources.pop(name,None);self._enabled.discard(name)
    def enable(self,name:str)->None:
        if name not in self._sources: raise KeyError(name)
        self._enabled.add(name)
    def disable(self,name:str)->None:
        if name not in self._sources: raise KeyError(name)
        self._enabled.discard(name)
    def enabled_names(self)->list[str]:
        return sorted(self._enabled)
    def disabled_names(self)->list[str]:
        return sorted(set(self._sources)-self._enabled)
    def set_enabled(self,names:list[str])->None:
        self._enabled={n for n in names if n in self._sources}
    def enabled_sources(self):
        return [self._sources[n] for n in self._sources if n in self._enabled]
