"""Consolidated verification for OpportunityLab Phase 4 Pathfinder."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clustering.duplicate_cluster_service import DuplicateClusterService
from src.clustering.duplicate_decision_store import DuplicateDecisionStore
from src.contacts.contact_service import ContactService
from src.contacts.contact_store import ContactStore
from src.feedback.recommendation_feedback_service import (
    RecommendationFeedbackService,
)
from src.feedback.recommendation_feedback_store import RecommendationFeedbackStore
from src.learning.search_memory_service import SearchMemoryService
from src.models.opportunity import Opportunity
from src.outcomes.outcome_service import OutcomeService
from src.outcomes.outcome_store import OutcomeStore
from src.recommendations.recommendation_service import RecommendationService
from src.responses.response_service import ResponseService
from src.responses.response_store import ResponseStore
from src.review.decision_review_service import DecisionReviewService
from src.review.learning_export_service import LearningExportService
from src.timeline.timeline_service import TimelineService
from src.timeline.timeline_store import TimelineStore
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO
from src.workflows.workflow_service import WorkflowService
from src.workflows.workflow_store import WorkflowStore


def make_opportunity(title, url, source, score, query):
    item = Opportunity(
        title=title,
        url=url,
        source=source,
        score=score,
    )
    item.metadata["search_query"] = query
    return item


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        timeline = TimelineService(TimelineStore(root / "timeline.json"))
        tracking = TrackingService(
            TrackingStore(root / "tracked.json"),
            timeline,
        )
        workflows = WorkflowService(
            WorkflowStore(root / "workflows.json"),
            timeline,
        )
        responses = ResponseService(
            ResponseStore(root / "templates.json", root / "drafts.json"),
            timeline,
        )
        contacts = ContactService(
            ContactStore(root / "contacts.json", root / "history.json"),
            timeline,
        )
        outcomes = OutcomeService(
            OutcomeStore(root / "outcomes.json"),
            timeline,
        )
        feedback = RecommendationFeedbackService(
            RecommendationFeedbackStore(root / "feedback.json")
        )
        clusters = DuplicateClusterService(
            DuplicateDecisionStore(root / "duplicates.json")
        )

        primary, _ = tracking.track(
            make_opportunity(
                "Acme Outdoor Product Testing Australia",
                "https://acme.example/testing",
                "Company Websites",
                93,
                "outdoor product testing",
            )
        )
        related, _ = tracking.track(
            make_opportunity(
                "Join Acme Australian Outdoor Product Test",
                "https://acme.example/news/testing",
                "Serper",
                86,
                "outdoor product testing",
            )
        )
        weak, _ = tracking.track(
            make_opportunity(
                "Unknown Software Listing",
                "https://reddit.example/unknown",
                "Reddit",
                42,
                "software beta",
            )
        )
        tracking.update(primary.tracking_id, rating=5, status="Reviewing")
        tracking.update(related.tracking_id, rating=4)
        tracking.update(weak.tracking_id, rating=1)

        workflow = workflows.get_or_create(primary)
        workflows.set_completed(
            primary.tracking_id,
            workflow.items[0].item_id,
            True,
        )
        draft = responses.get_or_create_draft(primary)
        responses.apply_template(
            draft,
            responses.get_template_by_name("General Enquiry"),
            primary,
        )
        responses.save_draft(
            primary.tracking_id,
            subject=draft.subject,
            body=draft.body,
        )
        contacts.get_or_create_contact(primary)
        contacts.update_contact(
            primary.tracking_id,
            contact_name="Casey Example",
            email="casey@example.com",
        )
        contacts.add_interaction(
            primary.tracking_id,
            "Email",
            "Sent an enquiry.",
            "2026-07-23",
        )

        for record, result, lesson in (
            (primary, "Successful", "Product testing searches performed well."),
            (weak, "Unsuccessful", "The listing did not contain enough detail."),
        ):
            outcomes.get_or_create(record)
            outcomes.update(
                record.tracking_id,
                result=result,
                outcome_date="2026-07-23",
                estimated_value=350 if result == "Successful" else 0,
                result_notes="Pathfinder test outcome",
                lessons_learned=lesson,
            )

        assert clusters.find_clusters(tracking.records)
        memory = SearchMemoryService(tracking, outcomes)
        feedback.record(primary, True, "Good recommendation.")
        recommendation = RecommendationService(
            memory,
            outcomes,
            feedback,
        ).evaluate(
            make_opportunity(
                "Outdoor Product Testing Trial",
                "https://new.example/trial",
                "Company Websites",
                90,
                "outdoor product testing",
            )
        )
        assert recommendation.label in ("Strong Match", "Worth Reviewing")
        assert recommendation.confidence > 40
        assert recommendation.reasons

        review = DecisionReviewService(
            memory,
            outcomes,
            feedback,
            clusters,
        )
        assert review.summary()["tracked"] == 3
        assert review.summary()["decided"] == 2
        assert review.strong_patterns()
        assert review.weak_patterns()
        assert review.lessons()

        learning_export = LearningExportService(
            review,
            memory,
            outcomes,
            feedback,
            clusters,
        )
        export_path = learning_export.export(root / "pathfinder-learning.json")
        exported = json.loads(export_path.read_text(encoding="utf-8"))
        assert exported["application"] == "OpportunityLab"
        assert exported["version"] == "0.22.0"
        assert exported["decision_summary"]["tracked"] == 3
        assert exported["source_profiles"]
        assert exported["keyword_profiles"]
        assert exported["opportunity_type_profiles"]
        assert exported["outcomes"]
        assert exported["recommendation_feedback"]
        assert exported["duplicate_families"]

        titles = {
            event.title
            for event in timeline.for_opportunity(primary.tracking_id)
        }
        assert "Opportunity added to tracking" in titles
        assert "Checklist action completed" in titles
        assert "Response draft saved" in titles
        assert "Contact details saved" in titles
        assert "Outcome recorded: Successful" in titles

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    review_window = (
        PROJECT_ROOT / "src/ui/decision_review_window.py"
    ).read_text(encoding="utf-8")
    assert "LearningExportService" in main_window
    assert 'text="Clusters"' in pipeline_window
    assert 'text="Memory"' in pipeline_window
    assert 'text="Review"' in pipeline_window
    assert "Export Learning" in review_window
    assert VERSION_INFO.version == "0.22.0"
    assert VERSION_INFO.package == "Package-022A-08"
    assert VERSION_INFO.build == 8
    assert VERSION_INFO.codename == "Pathfinder"

    print("Phase 4 complete test passed.")


if __name__ == "__main__":
    main()
