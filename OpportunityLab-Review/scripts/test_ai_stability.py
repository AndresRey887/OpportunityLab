"""Small no-network smoke test for Package-019B AI routing."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.ai.ai_provider import AIProvider
from src.ai.ai_router import AIRouter
from src.ai.ai_task import AITask
from src.ai.provider_registry import ProviderRegistry


class FakeRelatedProvider(AIProvider):
    def __init__(self) -> None:
        super().__init__("Fake Related Provider")
        self.available = True

    def suggest_related_searches(
        self,
        context,
        limit: int = 6,
    ) -> list[str]:
        return [
            f"{context} idea {index}"
            for index in range(1, limit + 1)
        ]


class OfflineProvider(AIProvider):
    def __init__(self) -> None:
        super().__init__("Offline Provider")
        self.available = False
        self.last_error = "deliberately offline for test"


def main() -> None:
    registry = ProviderRegistry()

    offline = OfflineProvider()
    fake = FakeRelatedProvider()

    registry.register(
        offline,
        {AITask.RELATED_SEARCHES},
        priority=10,
    )

    registry.register(
        fake,
        {AITask.RELATED_SEARCHES},
        priority=20,
    )

    router = AIRouter(registry)

    result = router.run(
        AITask.RELATED_SEARCHES,
        "camping tools",
        limit=3,
    )

    expected = [
        "camping tools idea 1",
        "camping tools idea 2",
        "camping tools idea 3",
    ]

    assert result == expected, (
        "AI routing smoke test failed.\n"
        f"Expected: {expected!r}\n"
        f"Received: {result!r}"
    )

    print("Package-019B AI stability smoke test passed.")


if __name__ == "__main__":
    main()