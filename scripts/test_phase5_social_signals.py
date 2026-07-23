"""Offline test for Phase 5 social-signal tracking."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.signals.social_signal_service import SocialSignalService
from src.signals.social_signal_store import SocialSignalStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        store = SocialSignalStore(Path(directory) / "signals.json")
        service = SocialSignalService(store)
        reddit = service.add(
            platform="Reddit",
            title="Camping testers discussing a new product",
            summary="Discussion volume and interest are increasing.",
            sentiment="Positive",
            strength=4,
            signal_date="2026-07-23",
            source_url="https://reddit.example/thread",
            topic_id="camping-topic",
        )
        youtube = service.add(
            platform="YouTube",
            title="Outdoor product preview",
            summary="A preview video received strong early engagement.",
            sentiment="Positive",
            strength=5,
            signal_date="2026-07-22",
            source_url="https://youtube.example/video",
            topic_id="camping-topic",
        )
        service.add(
            platform="News",
            title="Supply concern",
            summary="One supplier reported possible delivery delays.",
            sentiment="Negative",
            strength=2,
            signal_date="2026-07-21",
        )
        assert service.all()[0] == reddit
        assert service.all("YouTube") == [youtube]
        topic_summary = service.summary("camping-topic")
        assert topic_summary["total"] == 2
        assert topic_summary["positive"] == 2
        assert topic_summary["average_strength"] == 4.5
        assert topic_summary["sourced"] == 2

        reloaded = SocialSignalService(store)
        assert len(reloaded.signals) == 3
        assert reloaded.summary()["top_platform"] in {"Reddit", "YouTube", "News"}
        reloaded.remove(youtube.signal_id)
        assert len(reloaded.signals) == 2

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(encoding="utf-8")
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(encoding="utf-8")
    signals_window = (PROJECT_ROOT / "src/ui/social_signals_window.py").read_text(encoding="utf-8")
    assert "SocialSignalService" in main_window
    assert 'text="Signals"' in pipeline_window
    assert "Add Signal" in signals_window
    assert "Open Source" in signals_window
    assert VERSION_INFO.package == "Package-023A-05"
    assert VERSION_INFO.build == 5
    print("Phase 5 social signals test passed.")


if __name__ == "__main__":
    main()
