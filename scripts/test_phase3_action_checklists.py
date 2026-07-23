"""Verify Phase 3 persistent action checklists."""

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.opportunity import Opportunity
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO
from src.workflows.workflow_service import WorkflowService
from src.workflows.workflow_store import WorkflowStore


def main() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        opportunity = Opportunity(
            title="Regional Supplier Opportunity",
            url="https://example.com/opportunity",
            snippet="A useful test opportunity.",
            source="Company Websites",
            score=87,
        )
        record, created = tracking.track(opportunity)
        assert created

        workflow_path = root / "workflows.json"
        workflows = WorkflowService(WorkflowStore(workflow_path))
        workflow = workflows.get_or_create(record)
        assert len(workflow.items) == 6
        assert workflow.completed_count == 0
        assert workflow.progress_percent == 0

        first_item = workflow.items[0]
        workflows.set_completed(record.tracking_id, first_item.item_id, True)
        assert workflow.completed_count == 1
        assert workflow.progress_percent == 17

        custom_item = workflows.add_item(
            record.tracking_id,
            "Telephone the opportunity contact",
        )
        assert len(workflow.items) == 7
        workflows.remove_item(record.tracking_id, custom_item.item_id)
        assert len(workflow.items) == 6

        reloaded = WorkflowService(WorkflowStore(workflow_path))
        persisted = reloaded.get(record.tracking_id)
        assert persisted.completed_count == 1
        assert persisted.items[0].completed

    project_root = Path(__file__).resolve().parents[1]
    main_window = (project_root / "src/ui/main_window.py").read_text(encoding="utf-8")
    tracking_window = (
        project_root / "src/ui/tracking_window.py"
    ).read_text(encoding="utf-8")
    checklist_window = (
        project_root / "src/ui/checklist_window.py"
    ).read_text(encoding="utf-8")

    assert "Create Checklist" in main_window
    assert "open_selected_checklist" in main_window
    assert 'text="Checklist"' in tracking_window
    assert "Add Action" in checklist_window
    assert "progress_percent" in checklist_window
    assert VERSION_INFO.package == "Package-021A-03"
    assert VERSION_INFO.build == 3

    print("Phase 3 action checklist test passed.")


if __name__ == "__main__":
    main()
