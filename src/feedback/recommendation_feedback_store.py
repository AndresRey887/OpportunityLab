"""JSON persistence for recommendation feedback."""

from __future__ import annotations

import json
from pathlib import Path

from src.feedback.recommendation_feedback import RecommendationFeedback


class RecommendationFeedbackStore:
    def __init__(
        self,
        path: str | Path = "data/recommendation_feedback.json",
    ) -> None:
        self.path = Path(path)

    def load(self) -> list[RecommendationFeedback]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        feedback = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                feedback.append(RecommendationFeedback.from_dict(item))
            except (TypeError, ValueError):
                continue
        return feedback

    def save(self, feedback: list[RecommendationFeedback]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                [item.to_dict() for item in feedback],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary.replace(self.path)
