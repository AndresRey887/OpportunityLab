"""Manage tracked OpportunityLab opportunities."""

from __future__ import annotations

from src.tracking.tracked_opportunity import TrackedOpportunity
from src.tracking.tracking_store import TrackingStore


class TrackingService:
    def __init__(
        self,
        store: TrackingStore | None = None,
        timeline_service=None,
    ) -> None:
        self.store = store or TrackingStore()
        self.timeline_service = timeline_service
        self.records = self.store.load()

    def all(self, status: str | None = None) -> list[TrackedOpportunity]:
        records = self.records
        if status and status != "All":
            records = [record for record in records if record.status == status]
        return sorted(
            records,
            key=lambda record: record.updated_at,
            reverse=True,
        )

    def get(self, tracking_id: str) -> TrackedOpportunity:
        for record in self.records:
            if record.tracking_id == tracking_id:
                return record
        raise KeyError(tracking_id)

    def is_tracked(self, url: str) -> bool:
        normalized = str(url).strip().casefold()
        return bool(normalized) and any(
            record.url.casefold() == normalized
            for record in self.records
        )

    def track(self, opportunity) -> tuple[TrackedOpportunity, bool]:
        candidate = TrackedOpportunity.from_opportunity(opportunity)

        if candidate.url:
            for record in self.records:
                if record.url.casefold() == candidate.url.casefold():
                    return record, False

        self.records.append(candidate)
        self.save()
        self._record_event(
            candidate.tracking_id,
            "Tracking",
            "Opportunity added to tracking",
            candidate.title,
        )
        return candidate, True

    def update(
        self,
        tracking_id: str,
        *,
        status: str | None = None,
        rating: int | None = None,
        notes: str | None = None,
        follow_up_date: str | None = None,
    ) -> TrackedOpportunity:
        record = self.get(tracking_id)

        if status is not None:
            if status not in TrackedOpportunity.STATUSES:
                raise ValueError(status)
            record.status = status
        if rating is not None:
            record.rating = max(0, min(int(rating), 5))
        if notes is not None:
            record.notes = str(notes).strip()
        if follow_up_date is not None:
            record.follow_up_date = str(follow_up_date).strip()

        record.touch()
        self.save()
        changes = []
        if status is not None:
            changes.append(f"Status: {record.status}")
        if rating is not None:
            changes.append(f"Rating: {record.rating}/5")
        if notes is not None:
            changes.append("Notes updated")
        if follow_up_date is not None:
            changes.append(
                f"Follow-up: {record.follow_up_date or 'cleared'}"
            )
        if changes:
            self._record_event(
                tracking_id,
                "Tracking",
                "Tracked opportunity updated",
                " | ".join(changes),
            )
        return record

    def remove(self, tracking_id: str) -> None:
        record = self.get(tracking_id)
        self._record_event(
            tracking_id,
            "Tracking",
            "Opportunity removed from tracking",
            record.title,
        )
        self.records = [
            record
            for record in self.records
            if record.tracking_id != tracking_id
        ]
        self.save()

    def save(self) -> None:
        self.store.save(self.records)

    def _record_event(self, tracking_id, event_type, title, details=""):
        if self.timeline_service is not None:
            self.timeline_service.record(
                tracking_id,
                event_type,
                title,
                details,
            )
