"""Parse a generated email into editable subject and body fields."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GeneratedEmail:
    subject: str
    body: str

    @classmethod
    def parse(cls, text: str, fallback_subject: str = "") -> "GeneratedEmail":
        cleaned = str(text or "").strip()
        lines = cleaned.splitlines()
        subject = str(fallback_subject).strip()
        if lines and lines[0].strip().lower().startswith("subject:"):
            subject = lines.pop(0).split(":", 1)[1].strip()
            while lines and not lines[0].strip():
                lines.pop(0)
        return cls(subject=subject, body="\n".join(lines).strip())
