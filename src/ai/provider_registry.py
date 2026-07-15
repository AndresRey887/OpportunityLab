"""Registration and selection of OpportunityLab AI providers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from src.ai.ai_task import AITask


@dataclass
class ProviderRegistration:
    provider: object
    supported_tasks: set[str] = field(default_factory=set)
    priority: int = 100

    @property
    def name(self) -> str:
        return str(
            getattr(self.provider, "name", self.provider.__class__.__name__)
        )

    def supports(self, task: str) -> bool:
        return task in self.supported_tasks

    def is_available(self) -> bool:
        try:
            return bool(self.provider.is_available())
        except Exception:
            return False


class ProviderRegistry:
    """Stores providers and chooses the first available one by priority."""

    def __init__(self) -> None:
        self._registrations: list[ProviderRegistration] = []

    def register(
        self,
        provider: object,
        supported_tasks: Iterable[str],
        priority: int = 100,
    ) -> ProviderRegistration:
        if provider is None:
            raise ValueError("Cannot register an empty AI provider.")

        tasks = set(supported_tasks or [])
        if not tasks:
            raise ValueError("At least one supported AI task is required.")

        invalid_tasks = sorted(task for task in tasks if not AITask.is_valid(task))
        if invalid_tasks:
            raise ValueError("Unknown AI tasks: " + ", ".join(invalid_tasks))

        # One provider object may have several registrations over time. Merge
        # its task set instead of accidentally deleting unrelated capabilities.
        existing = self._find_registration(provider)
        if existing is not None:
            existing.supported_tasks.update(tasks)
            existing.priority = min(existing.priority, int(priority))
            self._sort()
            return existing

        registration = ProviderRegistration(
            provider=provider,
            supported_tasks=tasks,
            priority=int(priority),
        )
        self._registrations.append(registration)
        self._sort()
        return registration

    def unregister(self, provider: object) -> None:
        self._registrations = [
            item for item in self._registrations if item.provider is not provider
        ]

    def remove_task(self, provider: object, task: str) -> None:
        registration = self._find_registration(provider)
        if registration is None:
            return

        registration.supported_tasks.discard(task)
        if not registration.supported_tasks:
            self.unregister(provider)

    def get_available_provider(self, task: str):
        self._validate_task(task)
        for registration in self._registrations:
            if registration.supports(task) and registration.is_available():
                return registration.provider
        return None

    def get_registered_providers(self) -> list[ProviderRegistration]:
        return list(self._registrations)

    def get_providers_for_task(self, task: str) -> list[ProviderRegistration]:
        self._validate_task(task)
        return [item for item in self._registrations if item.supports(task)]

    def get_status_for_task(self, task: str) -> list[dict]:
        """Return diagnostics without exposing registry internals to the UI."""
        statuses = []
        for registration in self.get_providers_for_task(task):
            provider = registration.provider
            available = registration.is_available()
            try:
                message = str(provider.get_status_message())
            except Exception as error:
                message = f"Status check failed: {error}"

            statuses.append(
                {
                    "name": registration.name,
                    "priority": registration.priority,
                    "available": available,
                    "message": message,
                }
            )
        return statuses

    def _find_registration(self, provider: object):
        for registration in self._registrations:
            if registration.provider is provider:
                return registration
        return None

    def _sort(self) -> None:
        self._registrations.sort(key=lambda item: item.priority)

    @staticmethod
    def _validate_task(task: str) -> None:
        if not AITask.is_valid(task):
            raise ValueError(f"Unknown AI task: {task}")