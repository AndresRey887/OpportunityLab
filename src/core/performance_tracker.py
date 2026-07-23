"""Small monotonic performance tracker for production diagnostics."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceCheckpoint:
    name: str
    elapsed_seconds: float


class PerformanceTracker:
    def __init__(
        self,
        name: str,
        clock: Callable[[], float] = time.perf_counter,
    ) -> None:
        self.name = name
        self._clock = clock
        self._started = clock()
        self._checkpoints: list[PerformanceCheckpoint] = []

    def checkpoint(self, name: str) -> PerformanceCheckpoint:
        checkpoint = PerformanceCheckpoint(
            name=name,
            elapsed_seconds=self._clock() - self._started,
        )
        self._checkpoints.append(checkpoint)
        return checkpoint

    @property
    def elapsed_seconds(self) -> float:
        return self._clock() - self._started

    @property
    def checkpoints(self) -> tuple[PerformanceCheckpoint, ...]:
        return tuple(self._checkpoints)

    def summary(self) -> str:
        points = ", ".join(
            f"{checkpoint.name}={checkpoint.elapsed_seconds:.3f}s"
            for checkpoint in self._checkpoints
        )
        total = f"total={self.elapsed_seconds:.3f}s"
        return f"{self.name}: {points}, {total}" if points else (
            f"{self.name}: {total}"
        )
