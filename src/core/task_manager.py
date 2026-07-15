"""Central background task manager for OpportunityLab.

Worker functions run in a thread pool. Their completion callbacks are placed
on a queue and executed by Tkinter's main thread during queue polling.

Package-019B-04
"""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from queue import Empty, Queue
from threading import Lock
from typing import Any, Callable

from src.core.app_logger import get_logger
from src.core.task import BackgroundTask, TaskStatus


logger = get_logger("TaskManager")


class BackgroundTaskManager:
    """Run background work and safely dispatch callbacks to the UI thread."""

    def __init__(
        self,
        root: Any | None = None,
        *,
        max_workers: int = 3,
        poll_interval_ms: int = 50,
        autostart: bool = True,
    ) -> None:
        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")

        self._root = root
        self._poll_interval_ms = max(10, int(poll_interval_ms))
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="OpportunityLabWorker",
        )
        self._callbacks: Queue[Callable[[], None]] = Queue()
        self._tasks: dict[str, BackgroundTask] = {}
        self._futures: dict[str, Future[Any]] = {}
        self._lock = Lock()
        self._running = True

        logger.info("Ready with %s worker(s)", max_workers)

        if root is not None and autostart:
            self._schedule_poll()

    def submit(
        self,
        *,
        name: str,
        target: Callable[..., Any],
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
        on_success: Callable[[Any], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_complete: Callable[[], None] | None = None,
    ) -> BackgroundTask:
        """Submit work and return its task record immediately."""
        if not self._running:
            raise RuntimeError("BackgroundTaskManager has been shut down")
        if not callable(target):
            raise TypeError("target must be callable")

        task = BackgroundTask(
            name=name,
            target=target,
            args=tuple(args or ()),
            kwargs=dict(kwargs or {}),
            on_success=on_success,
            on_error=on_error,
            on_complete=on_complete,
        )

        with self._lock:
            self._tasks[task.task_id] = task

        logger.debug("Task submitted: %s [%s]", task.name, task.task_id)
        future = self._executor.submit(self._execute, task)

        with self._lock:
            self._futures[task.task_id] = future

        return task

    def _execute(self, task: BackgroundTask) -> None:
        if task.status is TaskStatus.CANCELLED:
            return

        task.status = TaskStatus.RUNNING

        try:
            result = task.target(*task.args, **task.kwargs)
        except Exception as error:
            logger.exception("Task failed: %s [%s]", task.name, task.task_id)
            task.error = error
            task.status = TaskStatus.FAILED
            self._callbacks.put(
                lambda current=task, failure=error: self._dispatch_error(
                    current,
                    failure,
                )
            )
        else:
            logger.debug("Task succeeded: %s [%s]", task.name, task.task_id)
            task.result = result
            task.status = TaskStatus.SUCCEEDED
            self._callbacks.put(
                lambda current=task, value=result: self._dispatch_success(
                    current,
                    value,
                )
            )

    def _dispatch_success(self, task: BackgroundTask, result: Any) -> None:
        try:
            if task.on_success is not None:
                task.on_success(result)
        finally:
            self._dispatch_complete(task)

    def _dispatch_error(self, task: BackgroundTask, error: Exception) -> None:
        try:
            if task.on_error is not None:
                task.on_error(error)
        finally:
            self._dispatch_complete(task)

    def _dispatch_complete(self, task: BackgroundTask) -> None:
        try:
            if task.on_complete is not None:
                task.on_complete()
        finally:
            with self._lock:
                self._futures.pop(task.task_id, None)

    def process_pending(self, limit: int = 100) -> int:
        """Run queued callbacks on the calling thread and return the count."""
        processed = 0

        while processed < limit:
            try:
                callback = self._callbacks.get_nowait()
            except Empty:
                break

            callback()
            processed += 1

        return processed

    def _schedule_poll(self) -> None:
        if not self._running or self._root is None:
            return

        try:
            self._root.after(
                self._poll_interval_ms,
                self._poll,
            )
        except Exception:
            self._running = False

    def _poll(self) -> None:
        if not self._running:
            return

        self.process_pending()
        self._schedule_poll()

    def get_task(self, task_id: str) -> BackgroundTask | None:
        with self._lock:
            return self._tasks.get(task_id)

    def active_tasks(self) -> list[BackgroundTask]:
        with self._lock:
            return [
                task
                for task in self._tasks.values()
                if task.status in {TaskStatus.PENDING, TaskStatus.RUNNING}
            ]

    def cancel(self, task_id: str) -> bool:
        """Cancel a task that has not started running."""
        with self._lock:
            task = self._tasks.get(task_id)
            future = self._futures.get(task_id)

        if task is None or future is None:
            return False

        cancelled = future.cancel()
        if cancelled:
            task.status = TaskStatus.CANCELLED
            with self._lock:
                self._futures.pop(task_id, None)

        return cancelled

    def shutdown(self, *, wait: bool = False) -> None:
        """Stop polling and prevent new work from being submitted."""
        if not self._running:
            return

        logger.info("Shutting down background task manager")
        self._running = False
        self._executor.shutdown(wait=wait, cancel_futures=True)
