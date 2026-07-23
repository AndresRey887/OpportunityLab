"""Build stage totals and priority-sorted pipeline items."""

from __future__ import annotations

from datetime import date

from src.pipeline.pipeline_item import PipelineItem
from src.tracking.tracked_opportunity import TrackedOpportunity


class PipelineService:
    def __init__(
        self,
        tracking_service,
        workflow_service,
        response_service,
        contact_service,
    ) -> None:
        self.tracking_service = tracking_service
        self.workflow_service = workflow_service
        self.response_service = response_service
        self.contact_service = contact_service

    def stage_totals(self) -> dict[str, int]:
        totals = {status: 0 for status in TrackedOpportunity.STATUSES}
        for record in self.tracking_service.records:
            totals[record.status] = totals.get(record.status, 0) + 1
        return totals

    def items(
        self,
        *,
        stage: str = "All",
        priority: str = "All",
    ) -> list[PipelineItem]:
        records = self.tracking_service.records
        if stage != "All":
            records = [record for record in records if record.status == stage]

        items = [self._build_item(record) for record in records]
        if priority != "All":
            items = [
                item for item in items
                if item.priority_label == priority
            ]
        return sorted(
            items,
            key=lambda item: (
                item.priority_score,
                item.record.rating,
                item.record.score,
                item.record.updated_at,
            ),
            reverse=True,
        )

    def _build_item(self, record) -> PipelineItem:
        checklist_percent = 0
        try:
            checklist_percent = self.workflow_service.get(
                record.tracking_id
            ).progress_percent
        except KeyError:
            pass

        has_draft = any(
            draft.tracking_id == record.tracking_id
            and bool(draft.subject or draft.body)
            for draft in self.response_service.drafts
        )
        interaction_count = len(
            self.contact_service.history(record.tracking_id)
        )

        priority_score = record.score + record.rating * 20
        if self._follow_up_due(record.follow_up_date):
            priority_score += 25

        if priority_score >= 145:
            priority_label = "High"
        elif priority_score >= 90:
            priority_label = "Medium"
        else:
            priority_label = "Low"

        return PipelineItem(
            record=record,
            priority_score=priority_score,
            priority_label=priority_label,
            checklist_percent=checklist_percent,
            has_draft=has_draft,
            interaction_count=interaction_count,
        )

    @staticmethod
    def _follow_up_due(value: str) -> bool:
        if not value:
            return False
        try:
            return date.fromisoformat(value) <= date.today()
        except ValueError:
            return False
