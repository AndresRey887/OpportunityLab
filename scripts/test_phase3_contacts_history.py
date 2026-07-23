"""Offline test for opportunity contacts and interaction history."""

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
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        record, created = tracking.track(
            Opportunity(
                title="Regional Business Partnership",
                url="https://example.com/partnership",
                source="Company Websites",
                score=88,
            )
        )
        assert created

        store = ContactStore(
            root / "contacts.json",
            root / "history.json",
        )
        service = ContactService(store)
        contact = service.get_or_create_contact(record)
        assert contact.website == record.url

        service.update_contact(
            record.tracking_id,
            contact_name="Jordan Lee",
            organisation="Example Organisation",
            email="jordan@example.com",
            phone="03 5555 0100",
            notes="Primary opportunity contact",
        )
        service.add_interaction(
            record.tracking_id,
            "Email",
            "Sent an initial enquiry.",
            "2026-07-22",
        )
        latest = service.add_interaction(
            record.tracking_id,
            "Phone",
            "Discussed eligibility requirements.",
            "2026-07-23",
        )
        assert [item.interaction_type for item in service.history(record.tracking_id)] == [
            "Phone",
            "Email",
        ]

        reloaded = ContactService(store)
        saved = reloaded.get_contact(record.tracking_id)
        assert saved.contact_name == "Jordan Lee"
        assert saved.email == "jordan@example.com"
        assert len(reloaded.history(record.tracking_id)) == 2
        reloaded.remove_interaction(latest.entry_id)
        assert len(reloaded.history(record.tracking_id)) == 1

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    tracking_window = (PROJECT_ROOT / "src/ui/tracking_window.py").read_text(
        encoding="utf-8"
    )
    contact_window = (
        PROJECT_ROOT / "src/ui/contact_history_window.py"
    ).read_text(encoding="utf-8")
    assert "Contacts & History" in main_window
    assert "open_selected_contacts" in main_window
    assert 'text="Contacts"' in tracking_window
    assert "Save Contact" in contact_window
    assert "Add History" in contact_window
    assert VERSION_INFO.package == "Package-021A-05"
    assert VERSION_INFO.build == 5

    print("Phase 3 contacts and history test passed.")


if __name__ == "__main__":
    main()
