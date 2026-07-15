"""Base contract for OpportunityLab AI providers."""

from __future__ import annotations

from typing import Any


class AIProvider:
    """Common provider interface used by the AI router and registry."""

    def __init__(self, name: str = "AI Provider") -> None:
        self.name = str(name).strip() or self.__class__.__name__
        self.available = False
        self.last_error = ""

    def is_available(self) -> bool:
        """Return whether the provider can currently accept work."""
        return bool(self.available)

    def get_status_message(self) -> str:
        """Return a short user-facing status message."""
        if self.is_available():
            return f"{self.name} is available."

        if self.last_error:
            return f"{self.name} is unavailable: {self.last_error}"

        return f"{self.name} is unavailable."

    def analyze(self, opportunity: Any):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement analyze()."
        )

    def suggest_related_searches(self, context: Any, limit: int = 6):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement "
            "suggest_related_searches()."
        )

    def draft_email(self, context: Any, **kwargs):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement draft_email()."
        )

    def draft_application(self, context: Any, **kwargs):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement "
            "draft_application()."
        )

    def create_checklist(self, context: Any, **kwargs):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement create_checklist()."
        )

    def rewrite_text(self, context: Any, **kwargs):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement rewrite_text()."
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name!r}, available={self.available!r})"
        )