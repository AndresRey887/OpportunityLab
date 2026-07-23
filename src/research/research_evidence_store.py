"""JSON persistence for structured research evidence."""

from __future__ import annotations

import json
from pathlib import Path

from src.research.research_evidence import ResearchEvidence


class ResearchEvidenceStore:
    def __init__(
        self,
        path: str | Path = "data/research_evidence.json",
    ) -> None:
        self.path = Path(path)

    def load(self) -> list[ResearchEvidence]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        evidence = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                evidence.append(ResearchEvidence.from_dict(item))
            except (TypeError, ValueError):
                continue
        return evidence

    def save(self, evidence: list[ResearchEvidence]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                [item.to_dict() for item in evidence],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary.replace(self.path)
