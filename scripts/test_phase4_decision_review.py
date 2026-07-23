"""Offline test for the Phase 4 decision-review dashboard."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clustering.duplicate_cluster_service import DuplicateClusterService
from src.clustering.duplicate_decision_store import DuplicateDecisionStore
from src.feedback.recommendation_feedback_service import (
    RecommendationFeedbackService,
)
from src.feedback.recommendation_feedback_store import RecommendationFeedbackStore
from src.learning.search_memory_service import SearchMemoryService
from src.models.opportunity import Opportunity
from src.outcomes.outcome_service import OutcomeService
from src.outcomes.outcome_store import OutcomeStore
from src.review.decision_review_service import DecisionReviewService
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def make_opportunity(title, url, source, score, query):
    item = Opportunity(title=title, url=url, source=source, score=score)
    item.metadata["search_query"] = query
    return item


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        outcomes = OutcomeService(OutcomeStore(root / "outcomes.json"))
        feedback = RecommendationFeedbackService(
            RecommendationFeedbackStore(root / "feedback.json")
        )
        clusters = DuplicateClusterService(
            DuplicateDecisionStore(root / "duplicates.json")
        )

        strong, _ = tracking.track(
            make_opportunity(
                "Outdoor Supplier Partnership",
                "https://company.example/strong",
                "Company Websites",
                92,
                "outdoor supplier",
            )
        )
        weak, _ = tracking.track(
            make_opportunity(
                "Unknown Software Beta",
                "https://reddit.example/weak",
                "Reddit",
                45,
                "software beta",
            )
        )
        tracking.update(strong.tracking_id, rating=5)
        tracking.update(weak.tracking_id, rating=1)

        for record, result, lesson in (
            (strong, "Successful", "Direct supplier searches worked well."),
            (weak, "Unsuccessful", "The listing lacked clear requirements."),
        ):
            outcomes.get_or_create(record)
            outcomes.update(
                record.tracking_id,
                result=result,
                outcome_date="2026-07-23",
                estimated_value=300 if result == "Successful" else 0,
                result_notes="Recorded result",
                lessons_learned=lesson,
            )

        for _ in range(4):
            feedback.record(strong, True)
        feedback.record(weak, False)

        memory = SearchMemoryService(tracking, outcomes)
        review = DecisionReviewService(
            memory,
            outcomes,
            feedback,
            clusters,
        )
        summary = review.summary()
        assert summary["tracked"] == 2
        assert summary["decided"] == 2
        assert summary["successful"] == 1
        assert summary["success_rate"] == 50
        assert summary["recommendation_accuracy"] == 80
        assert summary["feedback_total"] == 5

        strong_patterns = review.strong_patterns()
        weak_patterns = review.weak_patterns()
        assert any(
            pattern.label == "Company Websites"
            for pattern in strong_patterns
        )
        assert any(pattern.label == "Reddit" for pattern in weak_patterns)
        assert any("Only 2 opportunities" in gap for gap in review.evidence_gaps())
        assert any(
            "Direct supplier searches worked well." in lesson
            for lesson in review.lessons()
        )
        assert review.outcome_totals()["Successful"] == 1
        assert review.outcome_totals()["Unsuccessful"] == 1

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    review_window = (
        PROJECT_ROOT / "src/ui/decision_review_window.py"
    ).read_text(encoding="utf-8")
    assert "DecisionReviewService" in main_window
    assert 'text="Review"' in pipeline_window
    assert "Recommendation Accuracy" in review_window
    assert "Evidence Gaps" in review_window
    assert VERSION_INFO.package == "Package-022A-07"
    assert VERSION_INFO.build == 7

    print("Phase 4 decision review test passed.")


if __name__ == "__main__":
    main()
