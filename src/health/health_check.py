"""One system-health diagnostic result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthCheck:
    name: str
    status: str
    message: str
    category: str

    STATUSES = ("Passed", "Warning", "Failed")

    def __post_init__(self) -> None:
        if self.status not in self.STATUSES:
            raise ValueError(self.status)

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "category": self.category,
        }
