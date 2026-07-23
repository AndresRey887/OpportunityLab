"""One actionable checklist item."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from uuid import uuid4


@dataclass
class ActionItem:
    text: str
    completed: bool = False
    item_id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        self.text = str(self.text).strip()
        if not self.text:
            raise ValueError("Checklist item text cannot be empty.")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ActionItem":
        return cls(
            item_id=str(data.get("item_id") or uuid4().hex),
            text=str(data.get("text", "")),
            completed=bool(data.get("completed", False)),
        )
