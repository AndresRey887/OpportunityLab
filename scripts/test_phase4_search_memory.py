"""Offline test for Phase 4 search-memory learning profiles."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.learning.search_memory_service import SearchMemoryService
from src.models.opportunity import Opportunity
from src.outcomes.outcome_service import OutcomeService
from src.outcomes.outcome_store import OutcomeStore
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def opportunity(title, url, source, score, query):
    item = Opportunity(
        title=title,
        url=url,
        source=source,
        score=score,
    )
    item.metadata["search_query"] = query
    return item


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        outcomes = OutcomeService(OutcomeStore(root / "outcomes.json"))

        first, _ = tracking.track(
            opportunity(
                "Australian Camping Equipment Supplier",
                "https://example.com/supplier-one",
                "Company Websites",
                92,
                "camping equipment supplier",
            )
        )
        second, _ = tracking.track(
            opportunity(
                "Outdoor Product Supplier Partnership",
                "https://example.org/supplier-two",
                "Company Websites",
                86,
                "outdoor product supplier",
            )
        )
        third, _ = tracking.track(
            opportunity(
                "Local Software Beta Test",
                "https://reddit.example.net/beta",
                "Reddit",
                55,
                "software beta testing",
            )
        )
        tracking.update(first.tracking_id, rating=5)
        tracking.update(second.tracking_id, rating=4)
        tracking.update(third.tracking_id, rating=1)
        assert first.search_query == "camping equipment supplier"

        for record, result in (
            (first, "Successful"),
            (second, "Successful"),
            (third, "Unsuccessful"),
        ):
            outcomes.get_or_create(record)
            outcomes.update(
                record.tracking_id,
                result=result,
                outcome_date="2026-07-23",
                estimated_value=100 if result == "Successful" else 0,
                result_notes="Test result",
                lessons_learned="Test lesson",
            )

        memory = SearchMemoryService(tracking, outcomes)
        sources = memory.source_profiles()
        assert sources[0].label == "Company Websites"
        assert sources[0].tracked_count == 2
        assert sources[0].success_rate == 100
        assert sources[-1].label == "Reddit"
        assert sources[-1].success_rate == 0

        keywords = {profile.label: profile for profile in memory.keyword_profiles()}
        assert keywords["supplier"].tracked_count == 2
        assert keywords["supplier"].success_rate == 100

        types = {profile.label: profile for profile in memory.opportunity_type_profiles()}
        assert types["Business & Supply"].tracked_count == 2
        assert types["Product Testing"].tracked_count >= 1

        summary = memory.summary()
        assert summary["tracked"] == 3
        assert summary["top_source"] == "Company Websites"
        assert "supplier" in memory.suggested_searches()

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    memory_window = (PROJECT_ROOT / "src/ui/search_memory_window.py").read_text(
        encoding="utf-8"
    )
    assert "SearchMemoryService" in main_window
    assert 'text="Memory"' in pipeline_window
    assert "Search Memory" in memory_window
    assert "Use Search" in memory_window
    assert VERSION_INFO.package == "Package-022A-04"
    assert VERSION_INFO.build == 4

    print("Phase 4 search memory test passed.")


if __name__ == "__main__":
    main()
