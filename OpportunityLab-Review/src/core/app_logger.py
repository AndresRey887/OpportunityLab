"""Central logging configuration for OpportunityLab.

Package-019B-05
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from threading import Lock


APP_LOGGER_NAME = "OpportunityLab"
DEFAULT_LOG_FILENAME = "OpportunityLab.log"
DEFAULT_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_config_lock = Lock()
_configured = False
_log_file: Path | None = None


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def configure_logging(
    *,
    log_dir: str | Path | None = None,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    max_bytes: int = 1_000_000,
    backup_count: int = 3,
    force: bool = False,
) -> Path:
    """Configure console and rotating-file logging once.

    Returns the full path of the active log file.
    """
    global _configured, _log_file

    with _config_lock:
        if _configured and not force and _log_file is not None:
            return _log_file

        target_dir = (
            Path(log_dir)
            if log_dir is not None
            else _project_root() / "logs"
        )
        target_dir.mkdir(parents=True, exist_ok=True)
        log_file = target_dir / DEFAULT_LOG_FILENAME

        root_logger = logging.getLogger(APP_LOGGER_NAME)
        root_logger.setLevel(logging.DEBUG)
        root_logger.propagate = False

        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)
            try:
                handler.close()
            except Exception:
                pass

        formatter = logging.Formatter(
            DEFAULT_FORMAT,
            datefmt=DEFAULT_DATE_FORMAT,
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max(1, int(max_bytes)),
            backupCount=max(0, int(backup_count)),
            encoding="utf-8",
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        _configured = True
        _log_file = log_file
        return log_file


def shutdown_logging() -> None:
    """Flush and close all OpportunityLab logging handlers.

    This is primarily useful for tests, application shutdown, and Windows
    environments where an open file handler prevents the log file from being
    moved or deleted.
    """
    global _configured, _log_file

    with _config_lock:
        root_logger = logging.getLogger(APP_LOGGER_NAME)

        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)
            try:
                handler.flush()
            finally:
                handler.close()

        _configured = False
        _log_file = None



def get_logger(component: str | None = None) -> logging.Logger:
    """Return an OpportunityLab child logger with shared configuration."""
    if not _configured:
        configure_logging()

    if component:
        return logging.getLogger(f"{APP_LOGGER_NAME}.{component}")

    return logging.getLogger(APP_LOGGER_NAME)


def get_log_file() -> Path:
    """Return the active log-file path, configuring logging if needed."""
    if not _configured or _log_file is None:
        return configure_logging()
    return _log_file
