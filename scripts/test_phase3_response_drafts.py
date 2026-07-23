"""Offline test for response templates and saved opportunity drafts."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.opportunity import Opportunity
from src.responses.response_service import ResponseService
from src.responses.response_store import ResponseStore
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        record, created = tracking.track(
            Opportunity(
                title="Australian Product Trial",
                url="https://example.com/product-trial",
                source="Company Websites",
                score=91,
            )
        )
        assert created

        store = ResponseStore(
            root / "templates.json",
            root / "drafts.json",
        )
        service = ResponseService(store)
        assert service.template_names() == [
            "General Enquiry",
            "Expression of Interest",
            "Follow-up",
        ]

        draft = service.get_or_create_draft(record)
        template = service.get_template_by_name("General Enquiry")
        service.apply_template(draft, template, record)
        assert "Australian Product Trial" in draft.subject
        assert record.url in draft.body

        service.save_draft(
            record.tracking_id,
            subject="Saved subject",
            body="Saved response body",
        )
        custom = service.add_template(
            "My Product Trial Reply",
            "Reply about {title}",
            "I found this through {source}.",
        )
        assert not custom.built_in

        reloaded = ResponseService(store)
        persisted = reloaded.get_or_create_draft(record)
        assert persisted.subject == "Saved subject"
        assert persisted.body == "Saved response body"
        assert "My Product Trial Reply" in reloaded.template_names()

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    tracking_window = (PROJECT_ROOT / "src/ui/tracking_window.py").read_text(
        encoding="utf-8"
    )
    draft_window = (PROJECT_ROOT / "src/ui/draft_window.py").read_text(
        encoding="utf-8"
    )
    assert "Draft Response" in main_window
    assert "open_selected_draft" in main_window
    assert 'text="Draft"' in tracking_window
    assert "Apply Template" in draft_window
    assert "Save Template" in draft_window
    assert "Copy Draft" in draft_window
    assert VERSION_INFO.package == "Package-021A-04"
    assert VERSION_INFO.build == 4

    print("Phase 3 response draft test passed.")


if __name__ == "__main__":
    main()
