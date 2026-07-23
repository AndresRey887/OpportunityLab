"""JSON persistence for templates and opportunity drafts."""

from __future__ import annotations

import json
from pathlib import Path

from src.responses.opportunity_draft import OpportunityDraft
from src.responses.response_template import ResponseTemplate


class ResponseStore:
    def __init__(
        self,
        template_path: str | Path = "data/response_templates.json",
        draft_path: str | Path = "data/opportunity_drafts.json",
    ) -> None:
        self.template_path = Path(template_path)
        self.draft_path = Path(draft_path)

    def load_templates(self) -> list[ResponseTemplate]:
        return self._load(self.template_path, ResponseTemplate.from_dict)

    def load_drafts(self) -> list[OpportunityDraft]:
        return self._load(self.draft_path, OpportunityDraft.from_dict)

    def save_templates(self, templates: list[ResponseTemplate]) -> None:
        self._save(self.template_path, [item.to_dict() for item in templates])

    def save_drafts(self, drafts: list[OpportunityDraft]) -> None:
        self._save(self.draft_path, [item.to_dict() for item in drafts])

    @staticmethod
    def _load(path: Path, factory) -> list:
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        result = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                result.append(factory(item))
            except (TypeError, ValueError):
                continue
        return result

    @staticmethod
    def _save(path: Path, data: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(path.suffix + ".tmp")
        temporary_path.write_text(
            json.dumps(data, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temporary_path.replace(path)
