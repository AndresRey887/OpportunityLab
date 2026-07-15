"""Task routing for OpportunityLab AI providers."""

from __future__ import annotations

from typing import Any

from src.ai.ai_task import AITask
from src.ai.opportunity_analysis import OpportunityAnalysis


class AIRouter:
    """Select an available provider and invoke the task-specific method."""

    TASK_METHODS = {
        AITask.OPPORTUNITY_ANALYSIS: "analyze",
        AITask.RELATED_SEARCHES: "suggest_related_searches",
        AITask.DRAFT_EMAIL: "draft_email",
        AITask.DRAFT_APPLICATION: "draft_application",
        AITask.CREATE_CHECKLIST: "create_checklist",
        AITask.REWRITE_TEXT: "rewrite_text",
    }

    def __init__(self, registry=None) -> None:
        self.registry = registry

    def set_registry(self, registry) -> None:
        self.registry = registry

    def get_provider(self, task: str):
        self._validate_task(task)
        if self.registry is None:
            return None
        return self.registry.get_available_provider(task)

    def run(self, task: str, context: Any = None, **kwargs):
        self._validate_task(task)
        provider = self.get_provider(task)
        if provider is None:
            return self._provider_unavailable_result(task)

        method_name = self.TASK_METHODS[task]
        provider_method = getattr(provider, method_name, None)
        if not callable(provider_method):
            raise NotImplementedError(
                f"{provider.__class__.__name__} does not implement "
                f"{method_name}()."
            )

        try:
            return provider_method(context, **kwargs)
        except TypeError as error:
            # Preserve a clear contract error instead of hiding it behind a
            # generic provider failure message.
            raise TypeError(
                f"{provider.__class__.__name__}.{method_name}() could not "
                f"run task {task!r}: {error}"
            ) from error

    def get_task_status(self, task: str) -> list[dict]:
        self._validate_task(task)
        if self.registry is None:
            return []
        getter = getattr(self.registry, "get_status_for_task", None)
        if not callable(getter):
            return []
        return getter(task)

    @staticmethod
    def _validate_task(task: str) -> None:
        if not AITask.is_valid(task):
            raise ValueError(f"Unknown AI task: {task}")

    def _provider_unavailable_result(self, task: str):
        message = self._build_unavailable_message(task)

        if task == AITask.OPPORTUNITY_ANALYSIS:
            return OpportunityAnalysis(
                summary=message,
                category="Provider unavailable",
                confidence=0,
                opportunity_value=0,
                recommended_action=(
                    "Check the configured provider, connection, model and quota."
                ),
            )

        return {
            "success": False,
            "task": task,
            "message": message,
            "providers": self.get_task_status(task),
        }

    def _build_unavailable_message(self, task: str) -> str:
        statuses = self.get_task_status(task)
        if not statuses:
            return f"No AI provider is registered for the task: {task}."

        details = "; ".join(
            f"{item['name']}: {item['message']}" for item in statuses
        )
        return f"No available AI provider supports {task}. {details}"