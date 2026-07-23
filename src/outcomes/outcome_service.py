"""Manage opportunity outcomes and calculate success totals."""

from __future__ import annotations

from src.outcomes.outcome_record import OutcomeRecord
from src.outcomes.outcome_store import OutcomeStore


class OutcomeService:
    def __init__(
        self,
        store: OutcomeStore | None = None,
        timeline_service=None,
    ) -> None:
        self.store = store or OutcomeStore()
        self.timeline_service = timeline_service
        self.records = self.store.load()

    def get_or_create(self, tracked_record) -> OutcomeRecord:
        for outcome in self.records:
            if outcome.tracking_id == tracked_record.tracking_id:
                return outcome
        outcome = OutcomeRecord(
            tracking_id=tracked_record.tracking_id,
            opportunity_title=tracked_record.title,
        )
        self.records.append(outcome)
        self.store.save(self.records)
        return outcome

    def get(self, tracking_id: str) -> OutcomeRecord:
        for outcome in self.records:
            if outcome.tracking_id == tracking_id:
                return outcome
        raise KeyError(tracking_id)

    def update(
        self,
        tracking_id: str,
        *,
        result: str,
        outcome_date: str,
        estimated_value,
        result_notes: str,
        lessons_learned: str,
    ) -> OutcomeRecord:
        outcome = self.get(tracking_id)
        if result not in OutcomeRecord.RESULTS:
            raise ValueError(result)
        outcome.result = result
        outcome.outcome_date = str(outcome_date).strip()
        try:
            outcome.estimated_value = max(0.0, float(estimated_value or 0))
        except (TypeError, ValueError):
            outcome.estimated_value = 0.0
        outcome.result_notes = str(result_notes).strip()
        outcome.lessons_learned = str(lessons_learned).strip()
        outcome.touch()
        self.store.save(self.records)
        if self.timeline_service is not None:
            self.timeline_service.record(
                tracking_id,
                "Outcome",
                f"Outcome recorded: {outcome.result}",
                outcome.result_notes,
                event_at=outcome.outcome_date or None,
            )
        return outcome

    def summary(self) -> dict[str, float | int]:
        decided = [
            record for record in self.records
            if record.result != "Undecided"
        ]
        successful = [
            record for record in decided
            if record.result == "Successful"
        ]
        success_rate = (
            round(len(successful) / len(decided) * 100)
            if decided else 0
        )
        return {
            "recorded": len(decided),
            "successful": len(successful),
            "success_rate": success_rate,
            "estimated_value": round(
                sum(record.estimated_value for record in successful),
                2,
            ),
        }
