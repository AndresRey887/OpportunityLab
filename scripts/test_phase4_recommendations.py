"""Offline test for explainable Phase 4 recommendations."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.learning.search_memory_service import SearchMemoryService
from src.models.opportunity import Opportunity
from src.outcomes.outcome_service import OutcomeService
from src.outcomes.outcome_store import OutcomeStore
from src.recommendations.recommendation_service import RecommendationService
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def learned_opportunity(title, url, score, query):
    item = Opportunity(
        title=title,
        url=url,
        source="Company Websites",
        score=score,
    )
    item.metadata["search_query"] = query
    return item


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        outcomes = OutcomeService(OutcomeStore(root / "outcomes.json"))

        first, _ = tracking.track(
            learned_opportunity(
                "Camping Equipment Supplier Partnership",
                "https://example.com/first",
                92,
                "camping equipment supplier",
            )
        )
        second, _ = tracking.track(
            learned_opportunity(
                "Outdoor Product Supplier",
                "https://example.com/second",
                88,
                "outdoor supplier",
            )
        )
        tracking.update(first.tracking_id, rating=5)
        tracking.update(second.tracking_id, rating=4)
        for record in (first, second):
            outcomes.get_or_create(record)
            outcomes.update(
                record.tracking_id,
                result="Successful",
                outcome_date="2026-07-23",
                estimated_value=200,
                result_notes="Successful supplier result.",
                lessons_learned="Supplier searches worked.",
            )

        memory = SearchMemoryService(tracking, outcomes)
        recommendations = RecommendationService(memory, outcomes)
        candidate = learned_opportunity(
            "Australian Outdoor Equipment Supplier",
            "https://new.example.com/supplier",
            90,
            "outdoor equipment supplier",
        )
        result = recommendations.evaluate(candidate)
        assert result.label == "Strong Match"
        assert result.match_score >= 75
        assert result.confidence >= 60
        assert result.evidence_count == 4
        assert any("Company Websites" in reason for reason in result.reasons)
        assert any(
            '"equipment"' in reason or '"supplier"' in reason
            for reason in result.reasons
        )
        assert any("Business & Supply" in reason for reason in result.reasons)
        assert any("Limited tracked history" in item for item in result.cautions)

        empty_tracking = TrackingService(TrackingStore(root / "empty.json"))
        empty_outcomes = OutcomeService(OutcomeStore(root / "empty_outcomes.json"))
        sparse = RecommendationService(
            SearchMemoryService(empty_tracking, empty_outcomes),
            empty_outcomes,
        ).evaluate(
            Opportunity(
                title="Unknown New Opportunity",
                url="https://unknown.example/new",
                source="Unknown Source",
                score=40,
            )
        )
        assert sparse.label == "Low Priority"
        assert sparse.confidence < result.confidence
        assert any("new to OpportunityLab" in item for item in sparse.cautions)

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    recommendation_window = (
        PROJECT_ROOT / "src/ui/recommendation_window.py"
    ).read_text(encoding="utf-8")
    assert "RecommendationService" in main_window
    assert "Why This Opportunity?" in main_window
    assert "open_selected_recommendation" in main_window
    assert "Match score" in recommendation_window
    assert "Confidence" in recommendation_window
    assert VERSION_INFO.package == "Package-022A-05"
    assert VERSION_INFO.build == 5

    print("Phase 4 recommendation test passed.")


if __name__ == "__main__":
    main()
