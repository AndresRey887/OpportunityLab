"""Execution records produced by the discovery pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SourceExecutionResult:
    """The raw outcome of running one discovery source."""

    source_name: str
    items: list[dict[str, Any]]
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None

    @property
    def result_count(self) -> int:
        return len(self.items)
