"""Background monitor for due OpportunityLab search schedules."""

from __future__ import annotations

import logging
import threading
from datetime import datetime
from typing import Any, Callable

from src.scheduling.scheduled_search_runner import ScheduledSearchRunner


class ScheduledSearchMonitor:
    def __init__(
        self,
        runner: ScheduledSearchRunner,
        check_interval_seconds: float = 60.0,
        on_results: Callable[[list[Any]], None] | None = None,
    ) -> None:
        if check_interval_seconds <= 0:
            raise ValueError("Check interval must be greater than zero.")

        self.runner = runner
        self.check_interval_seconds = float(check_interval_seconds)
        self.on_results = on_results
        self.logger = logging.getLogger("OpportunityLab.ScheduledSearchMonitor")
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def check_now(self, now: datetime | None = None):
        results = self.runner.run_due(now)

        if results and self.on_results is not None:
            self.on_results(list(results))

        return results

    def start(self) -> None:
        if self.running:
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._monitor_loop,
            name="OpportunityLab-ScheduledSearchMonitor",
            daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join(timeout=timeout)

        self._thread = None

    def _monitor_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                self.check_now()
            except Exception:
                self.logger.exception("Scheduled search check failed")

            self._stop_event.wait(self.check_interval_seconds)
