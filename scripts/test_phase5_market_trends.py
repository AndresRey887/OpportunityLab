"""Offline test for Phase 5 market topics and trend observations."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.trends.trend_service import TrendService
from src.trends.trend_store import TrendStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        store = TrendStore(
            root / "topics.json",
            root / "observations.json",
        )
        service = TrendService(store)
        topic = service.add_topic(
            "Australian Camping Equipment Demand",
            category="Consumer Interest",
            keywords="camping, outdoor equipment, tents",
            notes="Watch seasonal demand and new product interest.",
        )
        assert topic.keywords == ["camping", "outdoor equipment", "tents"]

        earlier = service.add_observation(
            topic.topic_id,
            direction="Rising",
            strength=4,
            summary="Search interest increased before spring.",
            observation_date="2026-07-22",
            source_title="Camping Search Report",
            source_url="https://example.com/camping-report",
        )
        latest = service.add_observation(
            topic.topic_id,
            direction="Emerging",
            strength=5,
            summary="Compact camping products are gaining attention.",
            observation_date="2026-07-23",
            source_title="Outdoor Product Brief",
            source_url="https://example.com/product-brief",
        )
        assert service.for_topic(topic.topic_id) == [latest, earlier]
        summary = service.summary(topic.topic_id)
        assert summary["observations"] == 2
        assert summary["latest_direction"] == "Emerging"
        assert summary["average_strength"] == 4.5
        assert summary["momentum"] == 9.0
        assert summary["sourced"] == 2

        reloaded = TrendService(store)
        assert len(reloaded.topics) == 1
        assert len(reloaded.for_topic(topic.topic_id)) == 2
        reloaded.remove_observation(earlier.observation_id)
        assert reloaded.summary(topic.topic_id)["observations"] == 1
        reloaded.remove_topic(topic.topic_id)
        assert reloaded.topics == []
        assert reloaded.observations == []

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    market_window = (PROJECT_ROOT / "src/ui/market_trends_window.py").read_text(
        encoding="utf-8"
    )
    topic_window = (PROJECT_ROOT / "src/ui/trend_topic_window.py").read_text(
        encoding="utf-8"
    )
    assert "TrendService" in main_window
    assert 'text="Trends"' in pipeline_window
    assert "Add Topic" in market_window
    assert "Add Observation" in topic_window
    assert "Momentum:" in topic_window
    assert VERSION_INFO.package == "Package-023A-04"
    assert VERSION_INFO.build == 4

    print("Phase 5 market trends test passed.")


if __name__ == "__main__":
    main()
