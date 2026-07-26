"""Verify structured and malformed Gemini responses are handled safely."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ai.gemini_response_parser import GeminiResponseParser
from src.version import VERSION_INFO


def main() -> None:
    structured = SimpleNamespace(
        parsed={"summary": "Structured result"},
        text="not needed",
    )
    assert GeminiResponseParser.parse(structured) == {
        "summary": "Structured result"
    }

    fenced = SimpleNamespace(
        parsed=None,
        text='```json\n{"summary": "Fenced result"}\n```',
    )
    assert GeminiResponseParser.parse(fenced) == {
        "summary": "Fenced result"
    }

    malformed = SimpleNamespace(
        parsed=None,
        text='{"summary": "unterminated',
    )
    try:
        GeminiResponseParser.parse(malformed)
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("Malformed Gemini JSON was accepted.")

    provider_source = (PROJECT_ROOT / "src/ai/gemini_provider.py").read_text(
        encoding="utf-8"
    )
    assert "GeminiResponseParser.parse(response)" in provider_source
    assert "max_output_tokens=4096" in provider_source
    assert "incomplete structured response" in provider_source
    assert VERSION_INFO.package == "Package-110A-02"
    assert VERSION_INFO.build == 2
    print("Gemini response parsing test passed.")


if __name__ == "__main__":
    main()
