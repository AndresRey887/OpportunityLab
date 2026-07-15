"""
Opportunity Analyzer

Coordinates opportunity analysis through the AI Router,
caches completed analysis results, and exposes related-search
generation through the local Ollama provider.
"""

from src.ai.ai_router import AIRouter
from src.ai.ai_task import AITask
from src.ai.analysis_cache import AnalysisCache
from src.ai.ollama_provider import OllamaProvider
from src.ai.opportunity_analysis import OpportunityAnalysis
from src.ai.provider_registry import ProviderRegistry


class OpportunityAnalyzer:
    """High-level interface for OpportunityLab AI tasks."""

    def __init__(
        self,
        provider=None,
        cache=None,
        router=None,
        registry=None,
        related_search_provider=None,
    ):
        self.memory_cache = {}

        self.persistent_cache = (
            cache
            if cache is not None
            else AnalysisCache()
        )

        self.registry = (
            registry
            if registry is not None
            else ProviderRegistry()
        )

        self.router = (
            router
            if router is not None
            else AIRouter(self.registry)
        )

        # Ensure an injected router uses the same registry owned here.
        self.router.set_registry(self.registry)

        if provider is not None:
            self.register_analysis_provider(provider)

        # Related Intelligence is intended to use the local Ollama
        # provider so it does not consume Gemini quota.
        if related_search_provider is None:
            related_search_provider = OllamaProvider()

        if related_search_provider is not None:
            self.register_related_search_provider(
                related_search_provider
            )

    def register_analysis_provider(
        self,
        provider,
        priority=100,
    ):
        """Register a provider for full opportunity analysis."""
        return self.registry.register(
            provider=provider,
            supported_tasks={
                AITask.OPPORTUNITY_ANALYSIS,
            },
            priority=priority,
        )

    def register_related_search_provider(
        self,
        provider,
        priority=50,
    ):
        """Register a provider for related-search generation."""
        return self.registry.register(
            provider=provider,
            supported_tasks={
                AITask.RELATED_SEARCHES,
            },
            priority=priority,
        )

    def set_provider(self, provider):
        """Replace the opportunity-analysis provider.

        Existing providers for other tasks, including Ollama related
        searches, remain registered.
        """
        existing_registrations = (
            self.registry.get_registered_providers()
        )

        new_registry = ProviderRegistry()

        for registration in existing_registrations:
            non_analysis_tasks = {
                task
                for task in registration.supported_tasks
                if task != AITask.OPPORTUNITY_ANALYSIS
            }

            if non_analysis_tasks:
                new_registry.register(
                    provider=registration.provider,
                    supported_tasks=non_analysis_tasks,
                    priority=registration.priority,
                )

        self.registry = new_registry
        self.router.set_registry(self.registry)

        if provider is not None:
            self.register_analysis_provider(provider)

    def has_provider(self):
        """Return whether opportunity analysis has an available provider."""
        return (
            self.router.get_provider(
                AITask.OPPORTUNITY_ANALYSIS
            )
            is not None
        )

    def has_related_search_provider(self):
        """Return whether related searches have an available provider."""
        return (
            self.router.get_provider(
                AITask.RELATED_SEARCHES
            )
            is not None
        )

    def suggest_related_searches(
        self,
        context,
        limit=6,
    ):
        """Generate related search phrases through the AI Router."""
        if context is None:
            context = ""

        text = str(context).strip()

        if not text:
            return []

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 6

        limit = max(1, min(limit, 10))

        result = self.router.run(
            task=AITask.RELATED_SEARCHES,
            context=text,
            limit=limit,
        )

        if isinstance(result, dict):
            if result.get("success") is False:
                raise RuntimeError(
                    result.get(
                        "message",
                        "No related-search provider is available.",
                    )
                )

            suggestions = result.get(
                "suggestions",
                [],
            )
        else:
            suggestions = result

        if suggestions is None:
            return []

        if isinstance(suggestions, str):
            suggestions = [
                line.strip()
                for line in suggestions.splitlines()
                if line.strip()
            ]

        if not isinstance(suggestions, (list, tuple)):
            raise TypeError(
                "The related-search provider returned an "
                "unsupported response."
            )

        cleaned = []
        seen = set()

        for suggestion in suggestions:
            value = str(suggestion).strip()

            if not value:
                continue

            key = value.casefold()

            if key in seen:
                continue

            seen.add(key)
            cleaned.append(value)

            if len(cleaned) >= limit:
                break

        return cleaned

    def get_cache_key(self, opportunity):
        if opportunity is None:
            return ""

        url = str(
            getattr(
                opportunity,
                "url",
                "",
            )
        ).strip().lower()

        if url:
            return url

        return str(
            getattr(
                opportunity,
                "title",
                "",
            )
        ).strip().lower()

    def is_cached(self, opportunity):
        return (
            self.get_cached_analysis(
                opportunity
            )
            is not None
        )

    def get_cached_analysis(self, opportunity):
        cache_key = self.get_cache_key(
            opportunity
        )

        if not cache_key:
            return None

        memory_result = self.memory_cache.get(
            cache_key
        )

        if memory_result is not None:
            return memory_result

        stored_result = self.persistent_cache.get(
            cache_key
        )

        if stored_result is not None:
            self.memory_cache[
                cache_key
            ] = stored_result

            return stored_result

        return None

    def remove_cached_analysis(self, opportunity):
        cache_key = self.get_cache_key(
            opportunity
        )

        if not cache_key:
            return False

        self.memory_cache.pop(
            cache_key,
            None,
        )

        return self.persistent_cache.remove(
            cache_key
        )

    def clear_cache(self):
        self.memory_cache.clear()
        self.persistent_cache.clear()

    def analyze(
        self,
        opportunity,
        force=False,
    ):
        if opportunity is None:
            return OpportunityAnalysis(
                summary="No opportunity was selected.",
                category="Unavailable",
                confidence=0,
                opportunity_value=0,
                recommended_action=(
                    "Select an opportunity first."
                ),
            )

        cache_key = self.get_cache_key(
            opportunity
        )

        if not force:
            cached_analysis = (
                self.get_cached_analysis(
                    opportunity
                )
            )

            if cached_analysis is not None:
                return cached_analysis

        try:
            analysis = self.router.run(
                task=AITask.OPPORTUNITY_ANALYSIS,
                context=opportunity,
            )

            if isinstance(analysis, dict):
                analysis = (
                    OpportunityAnalysis.from_dict(
                        analysis
                    )
                )

            if not isinstance(
                analysis,
                OpportunityAnalysis,
            ):
                return OpportunityAnalysis(
                    summary=(
                        "The selected AI provider returned "
                        "an unsupported response."
                    ),
                    category="Analysis error",
                    confidence=0,
                    opportunity_value=0,
                    recommended_action=(
                        "Check the AI provider implementation."
                    ),
                )

            if cache_key:
                self.memory_cache[
                    cache_key
                ] = analysis

                provider_name = str(
                    getattr(
                        analysis,
                        "provider",
                        "",
                    )
                )

                if not provider_name:
                    provider = self.router.get_provider(
                        AITask.OPPORTUNITY_ANALYSIS
                    )

                    provider_name = str(
                        getattr(
                            provider,
                            "name",
                            "",
                        )
                    )

                self.persistent_cache.save(
                    cache_key=cache_key,
                    opportunity=opportunity,
                    analysis=analysis,
                    provider_name=provider_name,
                )

            return analysis

        except Exception as error:
            return OpportunityAnalysis(
                summary=(
                    f"AI analysis failed: {error}"
                ),
                category="Analysis error",
                confidence=0,
                opportunity_value=0,
                recommended_action=(
                    "Check the provider connection, "
                    "quota and configuration."
                ),
            )