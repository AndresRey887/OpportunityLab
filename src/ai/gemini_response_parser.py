"""Safely read structured Gemini responses."""

from __future__ import annotations

import json


class GeminiResponseParser:
    @staticmethod
    def parse(response) -> dict:
        parsed = getattr(response, "parsed", None)
        if hasattr(parsed, "model_dump"):
            parsed = parsed.model_dump()
        if isinstance(parsed, dict):
            return parsed

        text = str(getattr(response, "text", "") or "").strip()
        if not text:
            raise ValueError("Gemini returned an empty response.")
        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("Gemini response was not a JSON object.")
        return data
