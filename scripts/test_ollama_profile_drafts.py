"""Verify profile-aware Ollama drafting and generated email parsing."""

from __future__ import annotations

import sys
import types
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

if "requests" not in sys.modules:
    requests_stub = types.ModuleType("requests")
    requests_stub.RequestException = Exception
    sys.modules["requests"] = requests_stub

from src.ai.ai_task import AITask
from src.ai.ollama_provider import OllamaProvider
from src.ai.opportunity_analyzer import OpportunityAnalyzer
from src.responses.generated_email import GeneratedEmail
from src.version import VERSION_INFO


class CapturingOllama(OllamaProvider):
    def __init__(self):
        super().__init__()
        self.prompt = ""

    def _chat(self, prompt, temperature=0.3):
        self.prompt = prompt
        return (
            "Subject: Community partnership enquiry\n\n"
            "Hello,\n\nCould you provide more information?\n\n"
            "Kind regards,\nAlex Example\nCommunity Charity"
        )

    def is_available(self):
        return True


def main() -> None:
    provider = CapturingOllama()
    opportunity = SimpleNamespace(
        title="Volunteer Program",
        url="https://opportunity.example",
        snippet="Community participation opportunity.",
        score=80,
        ai_analysis=None,
    )
    profile = {
        "sender_name": "Alex Example",
        "organisation": "Community Charity",
        "organisation_website": "https://example.org",
        "charity_information": "Registered charity example",
        "profile_signature": "Alex Example\nCommunity Charity",
    }
    text = provider.draft_email(
        opportunity,
        tone="Warm and professional",
        profile_context=profile,
    )
    assert "Alex Example" in provider.prompt
    assert "Community Charity" in provider.prompt
    assert "https://example.org" in provider.prompt
    assert "Registered charity example" in provider.prompt
    assert "Warm and professional" in provider.prompt

    generated = GeneratedEmail.parse(text)
    assert generated.subject == "Community partnership enquiry"
    assert generated.body.startswith("Hello,")

    analyzer = OpportunityAnalyzer(
        provider=None,
        related_search_provider=provider,
    )
    registered = analyzer.registry.get_providers_for_task(AITask.DRAFT_EMAIL)
    assert registered and registered[0].provider is provider

    draft_ui = (PROJECT_ROOT / "src/ui/draft_window.py").read_text(
        encoding="utf-8"
    )
    assert "Generate with Ollama" in draft_ui
    assert "profile_context" in draft_ui
    assert VERSION_INFO.version == "1.1.4"
    assert VERSION_INFO.package == "Package-110A-05"
    assert VERSION_INFO.build == 5
    print("Ollama profile draft test passed.")


if __name__ == "__main__":
    main()
