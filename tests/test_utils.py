from __future__ import annotations

import logging
from unittest.mock import patch

from utils.cli import log_server_banner, log_shutdown_message, log_startup_message
from utils.logger import configure_logging, get_logger


class TestGetLogger:
    def test_returns_child_logger(self) -> None:
        logger = get_logger("test_module")
        assert logger.name == "AiDemo.test_module"

    def test_default_level_from_env(self) -> None:
        with patch.dict("os.environ", {"LOG_LEVEL": "WARNING"}):
            import importlib  # noqa: I001

            import utils.logger

            importlib.reload(utils.logger)
            logger = utils.logger.get_logger("warn_test")
            assert logger.level == logging.WARNING
            importlib.reload(utils.logger)

    def test_explicit_level_override(self) -> None:
        logger = get_logger("debug_test", level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_logger_has_handlers(self) -> None:
        get_logger("handler_test")
        parent = logging.getLogger("AiDemo")
        assert len(parent.handlers) > 0


class TestConfigureLogging:
    def test_configures_root_logger(self) -> None:
        root = logging.getLogger("AiDemo")
        configure_logging(root)
        assert root.level == logging.DEBUG
        assert not root.propagate
        assert len(root.handlers) == 1

    def test_removes_existing_handlers(self) -> None:
        root = logging.getLogger("AiDemo")
        root.addHandler(logging.StreamHandler())
        root.addHandler(logging.StreamHandler())
        configure_logging(root)
        assert len(root.handlers) == 1

    def test_plain_logging_when_rich_disabled(self) -> None:
        with patch("utils.logger._USE_RICH", False):
            root = logging.getLogger("AiDemo.plain")
            configure_logging(root)
            handler = root.handlers[0]
            assert isinstance(handler, logging.StreamHandler)


class TestLogServerBanner:
    def test_banner_renders_without_error(self) -> None:
        with patch("utils.cli.console") as mock_console:
            log_server_banner("TestServer", "http", host="127.0.0.1", port=9999)
            mock_console.print.assert_called_once()

    def test_banner_stdio_transport(self) -> None:
        with patch("utils.cli.console") as mock_console:
            log_server_banner("StdioServer", "stdio")
            mock_console.print.assert_called_once()


class TestStartupShutdownMessages:
    def test_startup_message(self) -> None:
        with patch("utils.cli.console") as mock_console:
            log_startup_message()
            assert mock_console.print.call_count == 2

    def test_shutdown_message(self) -> None:
        with patch("utils.cli.console") as mock_console:
            log_shutdown_message()
            mock_console.print.assert_called_once()
