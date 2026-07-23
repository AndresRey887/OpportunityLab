"""Offline test for Phase 5 product-launch monitoring."""

from __future__ import annotations

import sys
import tempfile
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.launches.product_launch_service import ProductLaunchService
from src.launches.product_launch_store import ProductLaunchStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        store = ProductLaunchStore(Path(directory) / "launches.json")
        service = ProductLaunchService(store)
        upcoming = service.add(product_name="Compact Camp Stove", company_name="Acme", stage="Pre-launch", launch_date="2026-08-05", category="Camping", source_url="https://example.com/stove")
        overdue = service.add(product_name="Delayed Tent Range", company_name="Rival", stage="Announced", launch_date="2026-07-20")
        released = service.add(product_name="Released Lantern", stage="Released", launch_date="2026-07-10")
        today = date(2026, 7, 23)
        assert service.upcoming(30, today) == [upcoming]
        assert service.overdue(today) == [overdue]
        summary = service.summary(today)
        assert summary["total"] == 3
        assert summary["upcoming_30"] == 1
        assert summary["overdue"] == 1
        assert summary["released"] == 1
        service.update_stage(overdue.launch_id, "Delayed")
        assert service.overdue(today) == []
        reloaded = ProductLaunchService(store)
        assert len(reloaded.launches) == 3
        reloaded.remove(released.launch_id)
        assert len(reloaded.launches) == 2

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(encoding="utf-8")
    pipeline = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(encoding="utf-8")
    window = (PROJECT_ROOT / "src/ui/product_launches_window.py").read_text(encoding="utf-8")
    assert "ProductLaunchService" in main_window
    assert 'text="Launches"' in pipeline
    assert "Add Launch" in window
    assert "Upcoming 30 days:" in window
    assert VERSION_INFO.package == "Package-023A-06"
    assert VERSION_INFO.build == 6
    print("Phase 5 product launches test passed.")


if __name__ == "__main__":
    main()
