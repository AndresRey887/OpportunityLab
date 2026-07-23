"""Offline test for persistent recommendation feedback learning."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.feedback.recommendation_feedback_service import (
    RecommendationFeedbackService,
)
from src.feedback.recommendation_feedback_store import RecommendationFeedbackStore
from src.learning.search_memory_service import SearchMemoryService
from src.models.opportunity import Opportunity
from src.outcomes.outcome_service import OutcomeService
from src.outcomes.outcome_store import OutcomeStore
from src.recommendations.recommendation_service import RecommendationService
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        outcomes = OutcomeService(OutcomeStore(root / "outcomes.json"))
        memory = SearchMemoryService(tracking, outcomes)
        feedback_store = RecommendationFeedbackStore(root / "feedback.json")
        feedback = RecommendationFeedbackService(feedback_store)
        service = RecommendationService(memory, outcomes, feedback)

        candidate = Opportunity(
            title="Camping Equipment Product Trial",
            url="https://example.com/camping-trial",
            source="Company Websites",
            score=70,
        )
        candidate.metadata["search_query"] = "camping equipment trial"

        baseline = service.evaluate(candidate)
        feedback.record(candidate, True, "This was a useful recommendation.")
        feedback.record(candidate, True)
        positive = service.evaluate(candidate)
        assert positive.match_score == baseline.match_score + 6
        assert positive.confidence > baseline.confidence
        assert positive.evidence_count == baseline.evidence_count + 2
        assert any(
            "helpful feedback" in reason
            for reason in positive.reasons
        )

        for _ in range(5):
            feedback.record(candidate, False, "Not a useful fit.")
        negative = service.evaluate(candidate)
        assert negative.match_score < baseline.match_score
        assert any(
            "unhelpful feedback" in caution
            for caution in negative.cautions
        )

        similar = Opportunity(
            title="Outdoor Camping Trial",
            url="https://another.example.com/trial",
            source="Company Websites",
            score=70,
        )
        influence = feedback.influence(similar)
        assert influence["matching"] == 7
        assert influence["helpful"] == 2
        assert influence["unhelpful"] == 5

        reloaded = RecommendationFeedbackService(feedback_store)
        assert len(reloaded.feedback) == 7
        assert reloaded.influence(similar) == influence

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    recommendation_window = (
        PROJECT_ROOT / "src/ui/recommendation_window.py"
    ).read_text(encoding="utf-8")
    assert "RecommendationFeedbackService" in main_window
    assert 'text="Helpful"' in recommendation_window
    assert 'text="Not Helpful"' in recommendation_window
    assert "Optional feedback note" in recommendation_window
    assert VERSION_INFO.package == "Package-022A-06"
    assert VERSION_INFO.build == 6

    print("Phase 4 recommendation feedback test passed.")


if __name__ == "__main__":
    main()
