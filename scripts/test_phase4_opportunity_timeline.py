"""Offline test for the permanent Phase 4 opportunity timeline."""

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
from src.outcomes.outcome_service import OutcomeService
from src.outcomes.outcome_store import OutcomeStore
from src.responses.response_service import ResponseService
from src.responses.response_store import ResponseStore
from src.timeline.timeline_service import TimelineService
from src.timeline.timeline_store import TimelineStore
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO
from src.workflows.workflow_service import WorkflowService
from src.workflows.workflow_store import WorkflowStore


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        timeline_store = TimelineStore(root / "timeline.json")
        timeline = TimelineService(timeline_store)
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

        record, created = tracking.track(
            Opportunity(
                title="Timeline Test Opportunity",
                url="https://example.com/timeline",
                source="Company Websites",
                score=85,
            )
        )
        assert created
        tracking.update(record.tracking_id, status="Reviewing", rating=4)

        workflow = workflows.get_or_create(record)
        workflows.set_completed(
            record.tracking_id,
            workflow.items[0].item_id,
            True,
        )

        draft = responses.get_or_create_draft(record)
        template = responses.get_template_by_name("General Enquiry")
        responses.apply_template(draft, template, record)
        responses.save_draft(
            record.tracking_id,
            subject=draft.subject,
            body=draft.body,
        )

        contacts.get_or_create_contact(record)
        contacts.update_contact(
            record.tracking_id,
            contact_name="Alex Example",
            email="alex@example.com",
        )
        contacts.add_interaction(
            record.tracking_id,
            "Email",
            "Sent the first enquiry.",
            "2026-07-23",
        )

        outcomes.get_or_create(record)
        outcomes.update(
            record.tracking_id,
            result="Successful",
            outcome_date="2026-07-24",
            estimated_value=250,
            result_notes="Accepted.",
            lessons_learned="The early enquiry helped.",
        )
        manual = timeline.record(
            record.tracking_id,
            "Note",
            "Manual timeline note",
            "Remember this approach.",
        )

        events = timeline.for_opportunity(record.tracking_id)
        titles = {event.title for event in events}
        assert "Opportunity added to tracking" in titles
        assert "Tracked opportunity updated" in titles
        assert "Checklist created" in titles
        assert "Checklist action completed" in titles
        assert "Response template applied" in titles
        assert "Response draft saved" in titles
        assert "Contact details saved" in titles
        assert "Email interaction added" in titles
        assert "Outcome recorded: Successful" in titles
        assert "Manual timeline note" in titles

        reloaded = TimelineService(timeline_store)
        assert len(reloaded.for_opportunity(record.tracking_id)) == len(events)
        reloaded.remove(manual.event_id)
        assert len(reloaded.for_opportunity(record.tracking_id)) == len(events) - 1

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    tracking_window = (PROJECT_ROOT / "src/ui/tracking_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    timeline_window = (PROJECT_ROOT / "src/ui/timeline_window.py").read_text(
        encoding="utf-8"
    )
    assert "TimelineService" in main_window
    assert 'text="Timeline"' in tracking_window
    assert 'text="Timeline"' in pipeline_window
    assert "Add a timeline note" in timeline_window
    assert VERSION_INFO.package == "Package-022A-02"
    assert VERSION_INFO.build == 2

    print("Phase 4 opportunity timeline test passed.")


if __name__ == "__main__":
    main()
