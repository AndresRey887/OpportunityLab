"""Offline test for Phase 4 opportunity outcome tracking."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.opportunity import Opportunity
from src.outcomes.outcome_service import OutcomeService
from src.outcomes.outcome_store import OutcomeStore
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        successful, _ = tracking.track(
            Opportunity(
                title="Successful Product Trial",
                url="https://example.com/success",
                score=92,
            )
        )
        unsuccessful, _ = tracking.track(
            Opportunity(
                title="Unsuccessful Application",
                url="https://example.com/unsuccessful",
                score=65,
            )
        )

        store = OutcomeStore(root / "outcomes.json")
        outcomes = OutcomeService(store)
        success = outcomes.get_or_create(successful)
        failure = outcomes.get_or_create(unsuccessful)
        assert success.result == "Undecided"
        assert failure.result == "Undecided"

        outcomes.update(
            successful.tracking_id,
            result="Successful",
            outcome_date="2026-07-23",
            estimated_value="450.50",
            result_notes="Accepted into the product trial.",
            lessons_learned="Clear evidence improved the response.",
        )
        outcomes.update(
            unsuccessful.tracking_id,
            result="Unsuccessful",
            outcome_date="2026-07-22",
            estimated_value=0,
            result_notes="Application was declined.",
            lessons_learned="Apply earlier next time.",
        )

        summary = outcomes.summary()
        assert summary["recorded"] == 2
        assert summary["successful"] == 1
        assert summary["success_rate"] == 50
        assert summary["estimated_value"] == 450.5

        reloaded = OutcomeService(store)
        saved = reloaded.get(successful.tracking_id)
        assert saved.result == "Successful"
        assert saved.outcome_date == "2026-07-23"
        assert saved.lessons_learned == "Clear evidence improved the response."

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    tracking_window = (PROJECT_ROOT / "src/ui/tracking_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    outcome_window = (PROJECT_ROOT / "src/ui/outcome_window.py").read_text(
        encoding="utf-8"
    )
    assert "OutcomeService" in main_window
    assert 'text="Outcome"' in tracking_window
    assert "Success rate:" in pipeline_window
    assert "Save Outcome" in outcome_window
    assert "Lessons learned" in outcome_window
    assert VERSION_INFO.version == "0.22.0"
    assert VERSION_INFO.package == "Package-022A-01"
    assert VERSION_INFO.build == 1
    assert VERSION_INFO.codename == "Pathfinder"

    print("Phase 4 outcome tracking test passed.")


if __name__ == "__main__":
    main()
