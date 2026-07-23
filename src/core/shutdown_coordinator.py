"""Run every shutdown action even when an earlier action fails."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class ShutdownAction:
    name: str
    callback: Callable[[], None]


@dataclass(frozen=True)
class ShutdownResult:
    name: str
    succeeded: bool
    error: str = ""


class ShutdownCoordinator:
    def run(
        self,
        actions: Iterable[ShutdownAction],
    ) -> tuple[ShutdownResult, ...]:
        results = []
        for action in actions:
            try:
                action.callback()
            except Exception as exc:
                results.append(
                    ShutdownResult(
                        name=action.name,
                        succeeded=False,
                        error=f"{type(exc).__name__}: {exc}",
                    )
                )
            else:
                results.append(
                    ShutdownResult(name=action.name, succeeded=True)
                )
        return tuple(results)
