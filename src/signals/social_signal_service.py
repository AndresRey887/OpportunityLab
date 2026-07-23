"""Manage and summarise social and web signals."""

from __future__ import annotations

from collections import Counter

from src.signals.social_signal import SocialSignal
from src.signals.social_signal_store import SocialSignalStore


class SocialSignalService:
    def __init__(self, store: SocialSignalStore | None = None) -> None:
        self.store = store or SocialSignalStore()
        self.signals = self.store.load()

    def add(self, **values) -> SocialSignal:
        signal = SocialSignal(**values)
        self.signals.append(signal)
        self.store.save(self.signals)
        return signal

    def all(self, platform: str = "All", topic_id: str = "") -> list[SocialSignal]:
        items = self.signals
        if platform != "All":
            items = [item for item in items if item.platform == platform]
        if topic_id:
            items = [item for item in items if item.topic_id == topic_id]
        return sorted(
            items,
            key=lambda item: (item.signal_date, item.created_at),
            reverse=True,
        )

    def summary(self, topic_id: str = "") -> dict[str, object]:
        items = self.all(topic_id=topic_id)
        sentiments = Counter(item.sentiment for item in items)
        platforms = Counter(item.platform for item in items)
        return {
            "total": len(items),
            "positive": sentiments.get("Positive", 0),
            "negative": sentiments.get("Negative", 0),
            "average_strength": (
                round(sum(item.strength for item in items) / len(items), 1)
                if items else 0.0
            ),
            "top_platform": (
                platforms.most_common(1)[0][0] if platforms else "No data"
            ),
            "sourced": sum(bool(item.source_url) for item in items),
        }

    def remove(self, signal_id: str) -> None:
        before = len(self.signals)
        self.signals = [item for item in self.signals if item.signal_id != signal_id]
        if len(self.signals) == before:
            raise KeyError(signal_id)
        self.store.save(self.signals)
