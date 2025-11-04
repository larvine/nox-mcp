"""Logging utility."""

import json
import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Any


class LogLevel(str, Enum):
    """Log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Logger:
    """JSON logger for structured logging."""

    def __init__(self, context: str) -> None:
        """Initialize logger with context."""
        self.context = context
        self.logger = logging.getLogger(context)

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _log(self, level: LogLevel, message: str, meta: dict[str, Any] | None = None) -> None:
        """Internal log method."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            "context": self.context,
            "message": message,
        }
        if meta:
            log_entry["meta"] = meta

        log_line = json.dumps(log_entry)

        if level == LogLevel.DEBUG:
            self.logger.debug(log_line)
        elif level == LogLevel.INFO:
            self.logger.info(log_line)
        elif level == LogLevel.WARNING:
            self.logger.warning(log_line)
        elif level == LogLevel.ERROR:
            self.logger.error(log_line)

    def debug(self, message: str, meta: dict[str, Any] | None = None) -> None:
        """Log debug message."""
        self._log(LogLevel.DEBUG, message, meta)

    def info(self, message: str, meta: dict[str, Any] | None = None) -> None:
        """Log info message."""
        self._log(LogLevel.INFO, message, meta)

    def warning(self, message: str, meta: dict[str, Any] | None = None) -> None:
        """Log warning message."""
        self._log(LogLevel.WARNING, message, meta)

    def error(self, message: str, meta: dict[str, Any] | None = None) -> None:
        """Log error message."""
        self._log(LogLevel.ERROR, message, meta)
