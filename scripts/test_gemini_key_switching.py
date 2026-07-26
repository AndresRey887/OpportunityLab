"""Verify safe, persistent Gemini API key selection."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ai.gemini_key_service import GeminiKeyService
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        selection_file = Path(directory) / "selection.json"
        service = GeminiKeyService(
            selection_file=selection_file,
            primary_key="primary-secret",
            alternate_key="alternate-secret",
        )
        assert service.selected == "Primary"
        assert service.active_key == "primary-secret"
        assert service.status() == {
            "selected": "Primary",
            "primary_configured": True,
            "alternate_configured": True,
        }

        service.select("Alternate")
        assert service.active_key == "alternate-secret"
        saved = json.loads(selection_file.read_text(encoding="utf-8"))
        assert saved == {"selected": "Alternate"}
        assert "secret" not in selection_file.read_text(encoding="utf-8")

        reloaded = GeminiKeyService(
            selection_file=selection_file,
            primary_key="primary-secret",
            alternate_key="alternate-secret",
        )
        assert reloaded.selected == "Alternate"
        assert reloaded.active_key == "alternate-secret"

    provider_source = (PROJECT_ROOT / "src/ai/gemini_provider.py").read_text(
        encoding="utf-8"
    )
    controller_source = (PROJECT_ROOT / "src/ai/ai_controller.py").read_text(
        encoding="utf-8"
    )
    data_tools = (PROJECT_ROOT / "src/ui/data_tools_window.py").read_text(
        encoding="utf-8"
    )
    assert "key_service.active_key" in provider_source
    assert "select_gemini_key" in controller_source
    assert "Gemini API Key" in data_tools
    assert VERSION_INFO.version == "1.1.0"
    assert VERSION_INFO.package == "Package-110A-01"
    assert VERSION_INFO.build == 1
    print("Gemini key switching test passed.")


if __name__ == "__main__":
    main()
