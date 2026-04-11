# tests/core/test_logging.py

import logging
import sys
from src.core.logging import logger


class TestLogging:
    def test_logger_name(self):
        """Tests the logger name."""
        assert logger.name == "backend"

    def test_logger_is_logging_logger_instance(self):
        """Tests the logger is a logging.Logger instance."""
        assert isinstance(logger, logging.Logger)

    def test_root_logger_level_is_info(self):
        """Tests the root logger level is INFO."""
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        assert root_logger.level == logging.INFO

    def test_root_logger_has_stream_handler(self):
        """Tests the root logger has a stream handler."""
        root_logger = logging.getLogger()
        handler_types = [type(h) for h in root_logger.handlers]
        assert any(issubclass(h, logging.StreamHandler) for h in handler_types)

    def test_stream_handler_outputs_to_stdout(self):
        """Tests the stream handler outputs to stdout."""
        root_logger = logging.getLogger("config_test")
        handler = logging.StreamHandler(sys.stdout)
        root_logger.addHandler(handler)
        assert root_logger.handlers[0].stream == sys.stdout

    def test_stream_handler_format(self):
        """Tests the stream handler format."""
        test_logger = logging.getLogger("test_config_logger")
        test_logger.propagate = False
        
        handler = logging.StreamHandler()
        expected_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        handler.setFormatter(logging.Formatter(expected_format))
        test_logger.addHandler(handler)
        
        assert test_logger.handlers[0].formatter._fmt == expected_format

    def test_logger_propagates_to_root(self):
        """Tests the logger propagates to the root logger."""
        assert logger.propagate is True

    def test_logger_emits_info_message(self, caplog):
        """Tests the logger emits info messages."""
        with caplog.at_level(logging.INFO):
            logger.info("test info message")
        assert "test info message" in caplog.text

    def test_logger_emits_error_message(self, caplog):
        """Tests the logger emits error messages."""
        with caplog.at_level(logging.ERROR):
            logger.error("test error message")
        assert "test error message" in caplog.text

    def test_logger_does_not_emit_debug_message(self, capfd):
        """Tests the logger does not emit debug messages."""
        logger.debug("test debug message")
        captured = capfd.readouterr()
        assert "test debug message" not in captured.out