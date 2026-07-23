"""Full Phase 3 verification including safe backup and restore."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.backups.backup_service import BackupError, BackupService
from src.contacts.contact_service import ContactService
from src.models.opportunity import Opportunity
from src.pipeline.pipeline_service import PipelineService
from src.responses.response_service import ResponseService
from src.tracking.tracking_service import TrackingService
from src.version import VERSION_INFO
from src.workflows.workflow_service import WorkflowService


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        data = root / "data"
        data.mkdir()
        saved_files = {
            "tracked_opportunities.json": '[{"title": "Saved opportunity"}]',
            "opportunity_workflows.json": '[{"items": []}]',
            "response_templates.json": '[{"name": "Saved template"}]',
            "opportunity_drafts.json": '[{"subject": "Saved draft"}]',
            "opportunity_contacts.json": '[{"contact_name": "Saved contact"}]',
            "interaction_history.json": '[{"summary": "Saved interaction"}]',
            "search_schedules.json": '[{"query": "saved search"}]',
        }
        for name, content in saved_files.items():
            (data / name).write_text(content, encoding="utf-8")
        (data / "opportunities.db").write_bytes(b"SQLite test data")
        (data / "ignored.txt").write_text("not application data", encoding="utf-8")

        service = BackupService(data)
        backup_path = service.create_backup(root / "OpportunityLab-Backup.zip")
        assert backup_path.exists()
        with ZipFile(backup_path) as archive:
            names = set(archive.namelist())
            assert BackupService.MANIFEST_NAME in names
            assert "data/tracked_opportunities.json" in names
            assert "data/opportunities.db" in names
            assert "data/ignored.txt" not in names

        (data / "tracked_opportunities.json").write_text(
            "changed",
            encoding="utf-8",
        )
        (data / "opportunity_drafts.json").unlink()
        restored = service.restore_backup(backup_path)
        assert len(restored) == len(saved_files) + 1
        assert (
            data / "tracked_opportunities.json"
        ).read_text(encoding="utf-8") == saved_files["tracked_opportunities.json"]
        assert (
            data / "opportunity_drafts.json"
        ).read_text(encoding="utf-8") == saved_files["opportunity_drafts.json"]

        unsafe_path = root / "unsafe.zip"
        unsafe_name = "data/../outside.json"
        manifest = {
            "app": "OpportunityLab",
            "files": [unsafe_name],
        }
        with ZipFile(unsafe_path, "w", compression=ZIP_DEFLATED) as archive:
            archive.writestr(
                BackupService.MANIFEST_NAME,
                json.dumps(manifest),
            )
            archive.writestr(unsafe_name, "{}")
        try:
            service.restore_backup(unsafe_path)
        except BackupError:
            pass
        else:
            raise AssertionError("Unsafe backup entry was not rejected.")

    tracking = TrackingService()
    workflows = WorkflowService()
    responses = ResponseService()
    contacts = ContactService()
    pipeline = PipelineService(tracking, workflows, responses, contacts)
    assert isinstance(pipeline.stage_totals(), dict)
    assert responses.template_names()
    sample = Opportunity(title="Phase 3", url="https://example.com/phase3")
    assert sample.title == "Phase 3"

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    data_window = (PROJECT_ROOT / "src/ui/data_tools_window.py").read_text(
        encoding="utf-8"
    )
    assert "Data..." in main_window
    assert "open_data_tools" in main_window
    assert "Create Backup" in data_window
    assert "Restore Backup" in data_window
    assert VERSION_INFO.version == "0.21.0"
    assert VERSION_INFO.package == "Package-021A-08"
    assert VERSION_INFO.build == 8

    print("Phase 3 complete test passed.")


if __name__ == "__main__":
    main()
