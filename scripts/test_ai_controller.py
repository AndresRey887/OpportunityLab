"""No-network smoke test for AIController delegation."""

from __future__ import annotations

import sys
import types
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# AIController supports analyzer injection. Stub provider-construction modules
# so this delegation test never imports an SDK or attempts network setup.
gemini_module = types.ModuleType("src.ai.gemini_provider")
opportunity_analyzer_module = types.ModuleType("src.ai.opportunity_analyzer")


class StubGeminiProvider:
    pass


class StubOpportunityAnalyzer:
    pass


gemini_module.GeminiProvider = StubGeminiProvider
opportunity_analyzer_module.OpportunityAnalyzer = StubOpportunityAnalyzer
sys.modules["src.ai.gemini_provider"] = gemini_module
sys.modules["src.ai.opportunity_analyzer"] = opportunity_analyzer_module

from src.ai.ai_controller import AIController  # noqa: E402


class FakeAnalyzer:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def analyze(self, opportunity, force=False):
        self.calls.append(("analyze", opportunity, force))
        return {"summary": "test analysis"}

    def suggest_related_searches(self, context, limit=6):
        self.calls.append(("related", context, limit))
        return [f"{context} suggestion"]

    def get_cached_analysis(self, opportunity):
        self.calls.append(("cache", opportunity))
        return "cached-result"


def main() -> None:
    analyzer = FakeAnalyzer()
    controller = AIController(analyzer=analyzer)

    analysis = controller.analyze("opportunity", force=True)
    related = controller.suggest_related_searches("camping", limit=4)
    cached = controller.get_cached_analysis("opportunity")

    assert analysis == {"summary": "test analysis"}
    assert related == ["camping suggestion"]
    assert cached == "cached-result"
    assert analyzer.calls == [
        ("analyze", "opportunity", True),
        ("related", "camping", 4),
        ("cache", "opportunity"),
    ]

    print("AIController delegation smoke test passed.")


if __name__ == "__main__":
    main()
