"""Record and retrieve chronological opportunity activity."""

from __future__ import annotations

from src.timeline.timeline_event import TimelineEvent
from src.timeline.timeline_store import TimelineStore


class TimelineService:
    def __init__(self, store: TimelineStore | None = None) -> None:
        self.store = store or TimelineStore()
        self.events = self.store.load()

    def record(
        self,
        tracking_id: str,
        event_type: str,
        title: str,
        details: str = "",
        *,
        event_at: str | None = None,
    ) -> TimelineEvent:
        event = TimelineEvent(
            tracking_id=tracking_id,
            event_type=event_type,
            title=title,
            details=details,
            **({"event_at": event_at} if event_at else {}),
        )
        self.events.append(event)
        self.store.save(self.events)
        return event

    def for_opportunity(self, tracking_id: str) -> list[TimelineEvent]:
        return sorted(
            (
                event for event in self.events
                if event.tracking_id == tracking_id
            ),
            key=lambda event: event.event_at,
            reverse=True,
        )

    def remove(self, event_id: str) -> None:
        original_count = len(self.events)
        self.events = [
            event for event in self.events
            if event.event_id != event_id
        ]
        if len(self.events) == original_count:
            raise KeyError(event_id)
        self.store.save(self.events)
