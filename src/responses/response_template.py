"""Reusable response template."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from uuid import uuid4


@dataclass
class ResponseTemplate:
    name: str
    subject: str
    body: str
    template_id: str = field(default_factory=lambda: uuid4().hex)
    built_in: bool = False

    def __post_init__(self) -> None:
        self.name = str(self.name).strip()
        self.subject = str(self.subject).strip()
        self.body = str(self.body).strip()
        if not self.name:
            raise ValueError("Template name cannot be empty.")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ResponseTemplate":
        return cls(
            template_id=str(data.get("template_id") or uuid4().hex),
            name=str(data.get("name", "")),
            subject=str(data.get("subject", "")),
            body=str(data.get("body", "")),
            built_in=bool(data.get("built_in", False)),
        )
