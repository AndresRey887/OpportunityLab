"""Background task data structures for OpportunityLab.

Package-019B-04
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from uuid import uuid4


class TaskStatus(str, Enum):
    """Lifecycle state for a background task."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class BackgroundTask:
    """Description and runtime state for one submitted task."""

    name: str
    target: Callable[..., Any]
    args: tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)
    on_success: Callable[[Any], None] | None = None
    on_error: Callable[[Exception], None] | None = None
    on_complete: Callable[[], None] | None = None
    task_id: str = field(default_factory=lambda: uuid4().hex)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Exception | None = None
