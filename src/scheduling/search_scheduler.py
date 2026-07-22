"""Manage persistent OpportunityLab search schedules."""

from __future__ import annotations

from datetime import datetime

from src.scheduling.search_schedule import SearchSchedule
from src.scheduling.search_schedule_store import SearchScheduleStore


class SearchScheduler:
    def __init__(self, store: SearchScheduleStore | None = None) -> None:
        self.store = store or SearchScheduleStore()
        self.schedules = self.store.load()

    def all(self) -> list[SearchSchedule]:
        return list(self.schedules)

    def add(self, schedule: SearchSchedule) -> None:
        if any(item.schedule_id == schedule.schedule_id for item in self.schedules):
            raise ValueError(f"Schedule already exists: {schedule.schedule_id}")

        if schedule.next_run_at is None:
            schedule.schedule_next()

        self.schedules.append(schedule)
        self.save()

    def get(self, schedule_id: str) -> SearchSchedule:
        for schedule in self.schedules:
            if schedule.schedule_id == schedule_id:
                return schedule
        raise KeyError(schedule_id)

    def remove(self, schedule_id: str) -> None:
        self.get(schedule_id)
        self.schedules = [
            schedule
            for schedule in self.schedules
            if schedule.schedule_id != schedule_id
        ]
        self.save()

    def set_enabled(self, schedule_id: str, enabled: bool) -> None:
        schedule = self.get(schedule_id)
        schedule.enabled = bool(enabled)
        self.save()

    def due(self, now: datetime | None = None) -> list[SearchSchedule]:
        return [
            schedule
            for schedule in self.schedules
            if schedule.is_due(now)
        ]

    def mark_ran(self, schedule_id: str, now: datetime | None = None) -> None:
        schedule = self.get(schedule_id)
        schedule.mark_ran(now)
        self.save()

    def save(self) -> None:
        self.store.save(self.schedules)
