"""Verify Phase 5 services are created before their dependants."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.version import VERSION_INFO

source = (ROOT / "src/ui/main_window.py").read_text(encoding="utf-8")
evidence = source.index("self.research_evidence_service = ResearchEvidenceService()")
brief = source.index("self.discovery_brief_service = DiscoveryBriefService(")

assert evidence < brief
assert VERSION_INFO.package == "Package-023A-08A"
assert VERSION_INFO.build == 9

print("Phase 5 service order fix passed.")
