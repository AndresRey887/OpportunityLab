"""Record feedback and find feedback relevant to new opportunities."""

from __future__ import annotations

import re

from src.feedback.recommendation_feedback import RecommendationFeedback
from src.feedback.recommendation_feedback_store import RecommendationFeedbackStore


class RecommendationFeedbackService:
    STOP_WORDS = {
        "a", "an", "and", "apply", "for", "from", "in", "join", "of", "on",
        "opportunity", "program", "the", "to", "with",
    }

    def __init__(
        self,
        store: RecommendationFeedbackStore | None = None,
    ) -> None:
        self.store = store or RecommendationFeedbackStore()
        self.feedback = self.store.load()

    def record(self, opportunity, helpful: bool, notes: str = ""):
        item = RecommendationFeedback(
            opportunity_key=RecommendationFeedback.key_for(opportunity),
            title=str(getattr(opportunity, "title", "")),
            source=str(getattr(opportunity, "source", "")),
            keywords=sorted(self.keywords_for(opportunity)),
            helpful=bool(helpful),
            notes=str(notes).strip(),
        )
        self.feedback.append(item)
        self.store.save(self.feedback)
        return item

    def matching(self, opportunity) -> list[RecommendationFeedback]:
        source = str(getattr(opportunity, "source", "")).casefold()
        keywords = self.keywords_for(opportunity)
        return [
            item for item in self.feedback
            if (
                (source and item.source.casefold() == source)
                or bool(keywords & set(item.keywords))
            )
        ]

    def influence(self, opportunity) -> dict[str, int]:
        matching = self.matching(opportunity)
        helpful = sum(item.helpful for item in matching)
        unhelpful = len(matching) - helpful
        adjustment = max(-12, min(12, (helpful - unhelpful) * 3))
        return {
            "matching": len(matching),
            "helpful": helpful,
            "unhelpful": unhelpful,
            "score_adjustment": adjustment,
        }

    @classmethod
    def keywords_for(cls, opportunity) -> set[str]:
        metadata = getattr(opportunity, "metadata", {})
        text = " ".join(
            (
                str(getattr(opportunity, "title", "")),
                str(getattr(opportunity, "snippet", "")),
                str(getattr(opportunity, "search_query", "")),
                str(metadata.get("search_query", "")),
            )
        )
        return {
            word for word in re.findall(r"[a-z0-9]+", text.casefold())
            if len(word) >= 3 and word not in cls.STOP_WORDS
        }
