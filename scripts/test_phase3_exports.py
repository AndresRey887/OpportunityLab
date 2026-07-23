"""Offline test for pipeline CSV and opportunity report exports."""

from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.contacts.contact_service import ContactService
from src.contacts.contact_store import ContactStore
from src.exports.export_service import ExportService
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
        record, _ = tracking.track(
            Opportunity(
                title="Australian Supplier Opportunity",
                url="https://example.com/supplier",
                source="Company Websites",
                score=92,
            )
        )
        tracking.update(
            record.tracking_id,
            status="Reviewing",
            rating=5,
            notes="Strong local fit.",
            follow_up_date="2026-07-30",
        )

        workflows = WorkflowService(WorkflowStore(root / "workflows.json"))
        workflow = workflows.get_or_create(record)
        workflows.set_completed(
            record.tracking_id,
            workflow.items[0].item_id,
            True,
        )

        responses = ResponseService(
            ResponseStore(root / "templates.json", root / "drafts.json")
        )
        responses.get_or_create_draft(record)
        responses.save_draft(
            record.tracking_id,
            subject="Supplier enquiry",
            body="Please send the supplier requirements.",
        )

        contacts = ContactService(
            ContactStore(root / "contacts.json", root / "history.json")
        )
        contacts.get_or_create_contact(record)
        contacts.update_contact(
            record.tracking_id,
            contact_name="Taylor Smith",
            organisation="Example Supply Co",
            email="taylor@example.com",
        )
        contacts.add_interaction(
            record.tracking_id,
            "Email",
            "Sent supplier enquiry.",
            "2026-07-23",
        )

        pipeline = PipelineService(
            tracking,
            workflows,
            responses,
            contacts,
        )
        exports = ExportService(
            pipeline,
            workflows,
            responses,
            contacts,
        )

        csv_path = exports.export_pipeline(root / "pipeline.csv")
        with csv_path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == 1
        assert rows[0]["Title"] == "Australian Supplier Opportunity"
        assert rows[0]["Priority"] == "High"
        assert rows[0]["Checklist Progress"] == "17%"
        assert rows[0]["Draft Saved"] == "Yes"

        report_path = exports.export_opportunity_report(
            record,
            root / exports.suggested_report_name(record.title),
        )
        report = report_path.read_text(encoding="utf-8")
        assert "OPPORTUNITYLAB OPPORTUNITY REPORT" in report
        assert "Taylor Smith" in report
        assert "Supplier enquiry" in report
        assert "[X] Review the full opportunity website" in report
        assert "Sent supplier enquiry." in report
        assert report_path.name == "Australian_Supplier_Opportunity_report.txt"

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    assert "ExportService" in main_window
    assert "Export CSV" in pipeline_window
    assert 'text="Report"' in pipeline_window
    assert VERSION_INFO.package == "Package-021A-07"
    assert VERSION_INFO.build == 7

    print("Phase 3 export test passed.")


if __name__ == "__main__":
    main()
