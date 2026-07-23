"""Offline test for Phase 3 opportunity tracking and UI integration."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.opportunity import Opportunity
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "tracked.json"
        service = TrackingService(TrackingStore(path))
        opportunity = Opportunity(
            title="Australian camping equipment tester",
            url="https://example.com.au/testing/camping",
            snippet="Apply to test new camping equipment.",
            source="Company Websites",
            score=84,
        )

        record, created = service.track(opportunity)
        assert created is True
        assert service.is_tracked(opportunity.url) is True

        duplicate, duplicate_created = service.track(opportunity)
        assert duplicate_created is False
        assert duplicate.tracking_id == record.tracking_id

        service.update(
            record.tracking_id,
            status="Reviewing",
            rating=5,
            notes="Strong fit for current interests.",
            follow_up_date="2026-08-15",
        )

        reloaded = TrackingService(TrackingStore(path))
        saved = reloaded.get(record.tracking_id)
        assert saved.status == "Reviewing"
        assert saved.rating == 5
        assert saved.notes == "Strong fit for current interests."
        assert saved.follow_up_date == "2026-08-15"
        assert len(reloaded.all("Reviewing")) == 1

        reloaded.remove(record.tracking_id)
        assert TrackingService(TrackingStore(path)).all() == []

    main_source = (
        PROJECT_ROOT / "src" / "ui" / "main_window.py"
    ).read_text(encoding="utf-8")
    tracking_source = (
        PROJECT_ROOT / "src" / "ui" / "tracking_window.py"
    ).read_text(encoding="utf-8")

    assert 'text="Tracked..."' in main_source
    assert 'text="Track Opportunity"' in main_source
    assert "def track_selected_opportunity" in main_source
    assert "class TrackingWindow" in tracking_source
    assert "Save Details" in tracking_source
    assert VERSION_INFO.version == "0.21.0"
    assert VERSION_INFO.package == "Package-021A-01"
    assert VERSION_INFO.build == 1
    assert VERSION_INFO.codename == "Catalyst"
    print("Phase 3 opportunity tracking test passed.")


if __name__ == "__main__":
    main()
