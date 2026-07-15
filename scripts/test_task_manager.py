"""No-network smoke test for Package-019B-04."""

from __future__ import annotations

import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.task import TaskStatus
from src.core.task_manager import BackgroundTaskManager


def main() -> None:
    manager = BackgroundTaskManager(root=None, max_workers=2, autostart=False)
    events: list[tuple[str, object]] = []

    successful = manager.submit(
        name="Successful task",
        target=lambda left, right: left + right,
        args=(20, 22),
        on_success=lambda result: events.append(("success", result)),
    )

    failed = manager.submit(
        name="Failed task",
        target=lambda: (_ for _ in ()).throw(RuntimeError("expected failure")),
        on_error=lambda error: events.append(("error", str(error))),
    )

    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline:
        manager.process_pending()
        if len(events) == 2:
            break
        time.sleep(0.01)

    manager.shutdown(wait=True)

    assert ("success", 42) in events, events
    assert ("error", "expected failure") in events, events
    assert successful.status is TaskStatus.SUCCEEDED
    assert failed.status is TaskStatus.FAILED

    print("Package-019B-04 BackgroundTaskManager smoke test passed.")


if __name__ == "__main__":
    main()
