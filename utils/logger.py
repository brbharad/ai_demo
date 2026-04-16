"""Centralized logging configuration with optional Rich formatting.

Environment variables
---------------------
LOG_LEVEL       Console log level (default: INFO).
USE_RICH_LOGGING
                Set to "FALSE" for plain-text logs (e.g. in containers).
                Any other value (or unset) enables Rich formatting.
"""

from __future__ import annotations

import logging
import os
from typing import Literal

from rich.console import Console
from rich.logging import RichHandler

LOG_LEVELS = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

_CONSOLE_LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
_USE_RICH: bool = os.getenv("USE_RICH_LOGGING", "TRUE").upper() != "FALSE"

_console = Console()

_ROOT_LOGGER_NAME = "AiDemo"


def configure_logging(
    logger: logging.Logger | None = None,
    *,
    enable_rich_tracebacks: bool = True,
) -> None:
    """Set up handlers on the root application logger.

    Calling this more than once is safe — existing handlers are removed first.

    Args:
        logger: Logger instance to configure.  Defaults to the package root
            logger (``AiDemo``).
        enable_rich_tracebacks: Show Rich tracebacks with source links when
            ``USE_RICH_LOGGING`` is enabled.
    """
    if logger is None:
        logger = logging.getLogger(_ROOT_LOGGER_NAME)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    if _USE_RICH:
        console_handler: logging.Handler = RichHandler(
            console=_console,
            rich_tracebacks=enable_rich_tracebacks,
            show_path=True,
            show_time=True,
        )
        formatter = logging.Formatter("%(message)s")
    else:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s  (%(name)s:%(funcName)s:%(lineno)d)"
        )

    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def get_logger(
    name: str,
    level: str = _CONSOLE_LOG_LEVEL,
) -> logging.Logger:
    """Return a child logger under the ``AiDemo`` namespace.

    The parent logger is lazily configured on the first call.

    Args:
        name: Logger name — typically ``__name__``.
        level: Minimum severity for this logger (default from ``LOG_LEVEL``
            env var).
    """
    parent = logging.getLogger(_ROOT_LOGGER_NAME)
    if not parent.handlers:
        configure_logging()

    child = logging.getLogger(f"{_ROOT_LOGGER_NAME}.{name}")
    child.setLevel(getattr(logging, level))
    return child


__all__ = [
    "configure_logging",
    "get_logger",
]
