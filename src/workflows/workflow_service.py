"""Manage persistent opportunity action checklists."""

from __future__ import annotations

from src.workflows.action_item import ActionItem
from src.workflows.opportunity_workflow import OpportunityWorkflow
from src.workflows.workflow_store import WorkflowStore


class WorkflowService:
    DEFAULT_ACTIONS = (
        "Review the full opportunity website",
        "Confirm eligibility and location requirements",
        "Record the closing date or response deadline",
        "Prepare the required contact or application details",
        "Submit or contact the organisation",
        "Set a follow-up date",
    )

    def __init__(self, store: WorkflowStore | None = None) -> None:
        self.store = store or WorkflowStore()
        self.workflows = self.store.load()

    def get(self, tracking_id: str) -> OpportunityWorkflow:
        for workflow in self.workflows:
            if workflow.tracking_id == tracking_id:
                return workflow
        raise KeyError(tracking_id)

    def get_or_create(self, record) -> OpportunityWorkflow:
        try:
            return self.get(record.tracking_id)
        except KeyError:
            workflow = OpportunityWorkflow(
                tracking_id=record.tracking_id,
                title=record.title,
                items=[ActionItem(text=text) for text in self.DEFAULT_ACTIONS],
            )
            self.workflows.append(workflow)
            self.save()
            return workflow

    def add_item(self, tracking_id: str, text: str) -> ActionItem:
        workflow = self.get(tracking_id)
        item = ActionItem(text=text)
        workflow.items.append(item)
        workflow.touch()
        self.save()
        return item

    def set_completed(
        self,
        tracking_id: str,
        item_id: str,
        completed: bool,
    ) -> None:
        workflow = self.get(tracking_id)
        for item in workflow.items:
            if item.item_id == item_id:
                item.completed = bool(completed)
                workflow.touch()
                self.save()
                return
        raise KeyError(item_id)

    def remove_item(self, tracking_id: str, item_id: str) -> None:
        workflow = self.get(tracking_id)
        original_count = len(workflow.items)
        workflow.items = [item for item in workflow.items if item.item_id != item_id]
        if len(workflow.items) == original_count:
            raise KeyError(item_id)
        workflow.touch()
        self.save()

    def save(self) -> None:
        self.store.save(self.workflows)
