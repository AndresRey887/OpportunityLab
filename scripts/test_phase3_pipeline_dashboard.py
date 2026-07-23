"""Offline test for the Phase 3 opportunity pipeline dashboard."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.contacts.contact_service import ContactService
from src.contacts.contact_store import ContactStore
from src.models.opportunity import Opportunity
from src.pipeline.pipeline_service import PipelineService
from src.responses.response_service import ResponseService
from src.responses.response_store import ResponseStore
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO
from src.workflows.workflow_service import WorkflowService
from src.workflows.workflow_store import WorkflowStore


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        high, _ = tracking.track(
            Opportunity(
                title="High Priority Partnership",
                url="https://example.com/high",
                score=90,
            )
        )
        medium, _ = tracking.track(
            Opportunity(
                title="Medium Priority Trial",
                url="https://example.com/medium",
                score=70,
            )
        )
        tracking.update(high.tracking_id, status="Reviewing", rating=5)
        tracking.update(medium.tracking_id, status="New", rating=2)

        workflows = WorkflowService(WorkflowStore(root / "workflows.json"))
        workflow = workflows.get_or_create(high)
        workflows.set_completed(
            high.tracking_id,
            workflow.items[0].item_id,
            True,
        )

        responses = ResponseService(
            ResponseStore(root / "templates.json", root / "drafts.json")
        )
        draft = responses.get_or_create_draft(high)
        responses.save_draft(
            high.tracking_id,
            subject="Saved partnership draft",
            body="Draft content",
        )

        contacts = ContactService(
            ContactStore(root / "contacts.json", root / "history.json")
        )
        contacts.get_or_create_contact(high)
        contacts.add_interaction(
            high.tracking_id,
            "Email",
            "Initial enquiry sent.",
            "2026-07-23",
        )

        pipeline = PipelineService(
            tracking,
            workflows,
            responses,
            contacts,
        )
        totals = pipeline.stage_totals()
        assert totals["Reviewing"] == 1
        assert totals["New"] == 1
        assert sum(totals.values()) == 2

        items = pipeline.items()
        assert items[0].record.tracking_id == high.tracking_id
        assert items[0].priority_label == "High"
        assert items[0].checklist_percent == 17
        assert items[0].has_draft
        assert items[0].interaction_count == 1
        assert pipeline.items(stage="New")[0].record.tracking_id == medium.tracking_id
        assert len(pipeline.items(priority="High")) == 1

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    assert "Pipeline..." in main_window
    assert "open_pipeline_window" in main_window
    assert "Opportunity Pipeline" in pipeline_window
    assert "Checklist:" in pipeline_window
    assert "Interactions:" in pipeline_window
    assert VERSION_INFO.package == "Package-021A-06"
    assert VERSION_INFO.build == 6

    print("Phase 3 pipeline dashboard test passed.")


if __name__ == "__main__":
    main()
