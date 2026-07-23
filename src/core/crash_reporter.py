"""Create local diagnostic reports for unexpected UI callback failures."""

from __future__ import annotations

import platform
import traceback
from datetime import datetime, timezone
from pathlib import Path
from types import TracebackType

from src.version import VERSION_INFO


class CrashReporter:
    def __init__(self, log_directory: str | Path = "logs") -> None:
        self.log_directory = Path(log_directory)

    def capture(
        self,
        exception_type: type[BaseException],
        exception: BaseException,
        traceback_value: TracebackType | None,
    ) -> Path:
        self.log_directory.mkdir(parents=True, exist_ok=True)
        created = datetime.now(timezone.utc)
        destination = self.log_directory / (
            f"crash-{created.strftime('%Y%m%d-%H%M%S-%f')}.log"
        )
        details = [
            "OpportunityLab Crash Report",
            f"Generated: {created.isoformat()}",
            f"Version: {VERSION_INFO.full_label}",
            f"Python: {platform.python_version()}",
            f"Platform: {platform.platform()}",
            "",
            "Exception:",
            "".join(
                traceback.format_exception(
                    exception_type,
                    exception,
                    traceback_value,
                )
            ).rstrip(),
            "",
        ]
        destination.write_text("\n".join(details), encoding="utf-8")
        return destination
