"""High-level AI entry point for OpportunityLab.

Package-019B-03 centralises AI construction and task delegation so UI code
never needs to create providers, routers, registries, analyzers, or caches.
"""

from __future__ import annotations

from typing import Any

from src.ai.ai_task import AITask
from src.ai.gemini_provider import GeminiProvider
from src.ai.opportunity_analyzer import OpportunityAnalyzer
from src.core.app_logger import get_logger


logger = get_logger("AIController")


class AIController:
    """Single application-facing entry point for OpportunityLab AI work."""

    def __init__(
        self,
        analyzer: OpportunityAnalyzer | None = None,
    ) -> None:
        # Keep provider construction out of MainWindow. An analyzer may still
        # be injected by tests or future application bootstrap code.
        self.analyzer = (
            analyzer
            if analyzer is not None
            else OpportunityAnalyzer(
                provider=GeminiProvider()
            )
        )
        logger.info("Initialised")

    # ------------------------------------------------------------------
    # Primary features used by the UI
    # ------------------------------------------------------------------

    def analyze_opportunity(
        self,
        opportunity: Any,
        force: bool = False,
    ):
        """Return a structured analysis for an opportunity.

        Cached analysis is reused unless ``force`` is true.
        """
        logger.debug("Analysing opportunity; force=%s", force)
        return self.analyzer.analyze(
            opportunity,
            force=force,
        )

    def related_searches(
        self,
        context: Any,
        limit: int = 6,
    ) -> list[str]:
        """Return cleaned related-search suggestions for a context."""
        logger.debug("Generating up to %s related searches", limit)
        return self.analyzer.suggest_related_searches(
            context,
            limit=limit,
        )

    # Friendly aliases for concise UI calls.
    def analyze(
        self,
        opportunity: Any,
        force: bool = False,
    ):
        return self.analyze_opportunity(
            opportunity,
            force=force,
        )

    def suggest_related_searches(
        self,
        context: Any,
        limit: int = 6,
    ) -> list[str]:
        return self.related_searches(
            context,
            limit=limit,
        )

    # ------------------------------------------------------------------
    # General task routing
    # ------------------------------------------------------------------

    def run_task(
        self,
        task: str,
        context: Any = None,
        **kwargs,
    ):
        """Run any registered task through the shared AI architecture."""
        if task == AITask.OPPORTUNITY_ANALYSIS:
            force = bool(kwargs.pop("force", False))
            return self.analyze_opportunity(
                context,
                force=force,
            )

        if task == AITask.RELATED_SEARCHES:
            limit = kwargs.pop("limit", 6)
            return self.related_searches(
                context,
                limit=limit,
            )

        return self.analyzer.router.run(
            task,
            context=context,
            **kwargs,
        )

    def draft_email(self, context: Any, **kwargs):
        return self.run_task(
            AITask.DRAFT_EMAIL,
            context,
            **kwargs,
        )

    def draft_application(self, context: Any, **kwargs):
        return self.run_task(
            AITask.DRAFT_APPLICATION,
            context,
            **kwargs,
        )

    def create_checklist(self, context: Any, **kwargs):
        return self.run_task(
            AITask.CREATE_CHECKLIST,
            context,
            **kwargs,
        )

    def rewrite_text(self, context: Any, **kwargs):
        return self.run_task(
            AITask.REWRITE_TEXT,
            context,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Provider registration and diagnostics
    # ------------------------------------------------------------------

    def register_analysis_provider(
        self,
        provider: object,
        priority: int = 100,
    ):
        return self.analyzer.register_analysis_provider(
            provider,
            priority,
        )

    def register_related_search_provider(
        self,
        provider: object,
        priority: int = 50,
    ):
        return self.analyzer.register_related_search_provider(
            provider,
            priority,
        )

    def has_provider(self, task: str) -> bool:
        """Return whether an available provider exists for a task."""
        return self.analyzer.router.get_provider(task) is not None

    def get_task_status(self, task: str) -> list[dict]:
        """Return user-safe diagnostics for providers assigned to a task."""
        return self.analyzer.router.get_task_status(task)

    def get_all_provider_statuses(self) -> dict[str, list[dict]]:
        """Return diagnostics for every supported AI task."""
        return {
            task: self.get_task_status(task)
            for task in sorted(AITask.ALL)
        }

    # ------------------------------------------------------------------
    # Analysis cache control
    # ------------------------------------------------------------------

    def is_analysis_cached(self, opportunity: Any) -> bool:
        return self.analyzer.is_cached(opportunity)

    def get_cached_analysis(self, opportunity: Any):
        return self.analyzer.get_cached_analysis(opportunity)

    def remove_cached_analysis(self, opportunity: Any) -> bool:
        return self.analyzer.remove_cached_analysis(opportunity)

    def clear_analysis_cache(self) -> None:
        self.analyzer.clear_cache()
