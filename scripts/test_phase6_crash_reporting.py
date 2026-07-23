"""Verify Phase 6 local crash reporting and UI integration."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.crash_reporter import CrashReporter
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        try:
            raise ValueError("safe test failure")
        except ValueError:
            exception_type, exception, traceback_value = sys.exc_info()
            reporter = CrashReporter(Path(directory) / "logs")
            report_path = reporter.capture(
                exception_type,
                exception,
                traceback_value,
            )

        assert report_path.is_file()
        report = report_path.read_text(encoding="utf-8")
        assert "OpportunityLab Crash Report" in report
        assert "ValueError: safe test failure" in report
        assert VERSION_INFO.full_label in report

    main_source = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    assert "def report_callback_exception" in main_source
    assert "CrashReporter()" in main_source
    assert "showerror" in main_source
    assert VERSION_INFO.package == "Package-100A-08"
    assert VERSION_INFO.build == 10
    print("Phase 6 crash reporting test passed.")


if __name__ == "__main__":
    main()
