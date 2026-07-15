"""Smoke test for Package-019B-05 application logging."""

from __future__ import annotations

import logging
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.app_logger import (
    configure_logging,
    get_logger,
    shutdown_logging,
)


def main() -> None:
    try:
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_file = configure_logging(
                log_dir=temporary_directory,
                console_level=logging.CRITICAL,
                file_level=logging.DEBUG,
                force=True,
            )

            logger = get_logger("LoggerSmokeTest")
            logger.debug("debug message")
            logger.info("info message")

            for handler in logging.getLogger("OpportunityLab").handlers:
                handler.flush()

            contents = log_file.read_text(encoding="utf-8")
            assert "debug message" in contents
            assert "info message" in contents
            assert "OpportunityLab.LoggerSmokeTest" in contents

            # Windows locks log files while handlers remain open.
            shutdown_logging()

    finally:
        # Safe even if configuration or an assertion failed.
        shutdown_logging()

    print("Package-019B-05 Logger smoke test passed.")


if __name__ == "__main__":
    main()
