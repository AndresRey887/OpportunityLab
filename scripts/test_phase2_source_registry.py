
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.discovery.source_registry import SourceRegistry
from src.discovery.search_source import SearchSource
class S(SearchSource):
    def __init__(self,n): super().__init__(n)
    def search(self,q): return []
r=SourceRegistry([S("A"),S("B"),S("C")])
assert r.enabled_names()==["A","B","C"]
r.disable("B")
assert r.enabled_names()==["A","C"]
assert r.disabled_names()==["B"]
r.set_enabled(["B"])
assert r.enabled_names()==["B"]
print("Phase 2 source registry management test passed.")
