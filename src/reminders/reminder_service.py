"""Create follow-up reminders from tracked opportunities."""

from __future__ import annotations

from datetime import date, timedelta

from src.reminders.follow_up_reminder import FollowUpReminder


class ReminderService:
    def __init__(self, tracking_service) -> None:
        self.tracking_service = tracking_service

    def all(self, today: date | None = None) -> list[FollowUpReminder]:
        current = today or date.today()
        reminders = []

        for record in self.tracking_service.all():
            if record.status == "Closed" or not record.follow_up_date:
                continue

            try:
                due_date = date.fromisoformat(record.follow_up_date)
            except ValueError:
                continue

            reminders.append(
                FollowUpReminder(
                    tracking_id=record.tracking_id,
                    title=record.title,
                    due_date=due_date,
                    days_until=(due_date - current).days,
                )
            )

        return sorted(
            reminders,
            key=lambda reminder: (reminder.due_date, reminder.title.casefold()),
        )

    def due(self, today: date | None = None) -> list[FollowUpReminder]:
        return [
            reminder
            for reminder in self.all(today)
            if reminder.days_until <= 0
        ]

    def upcoming(
        self,
        days: int = 7,
        today: date | None = None,
    ) -> list[FollowUpReminder]:
        current = today or date.today()
        end_date = current + timedelta(days=max(0, int(days)))
        return [
            reminder
            for reminder in self.all(current)
            if current < reminder.due_date <= end_date
        ]
