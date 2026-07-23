"""JSON persistence for opportunity action workflows."""

from __future__ import annotations

import json
from pathlib import Path

from src.workflows.opportunity_workflow import OpportunityWorkflow


class WorkflowStore:
    def __init__(self, path: str | Path = "data/opportunity_workflows.json") -> None:
        self.path = Path(path)

    def load(self) -> list[OpportunityWorkflow]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []

        workflows = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                workflows.append(OpportunityWorkflow.from_dict(item))
            except (TypeError, ValueError):
                continue
        return workflows

    def save(self, workflows: list[OpportunityWorkflow]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary_path.write_text(
            json.dumps(
                [workflow.to_dict() for workflow in workflows],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary_path.replace(self.path)
