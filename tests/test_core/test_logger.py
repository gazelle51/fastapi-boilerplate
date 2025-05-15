# pylint: disable=missing-module-docstring

from src.core.logger import setup_logger


def test_log_something(caplog):
    """Test that a log message is emitted at the INFO level and captured correctly."""
    # Set up the logger
    logger = setup_logger()

    # Capture logs during this block
    with caplog.at_level("INFO", logger="my_app"):
        logger.info("Something happened")

    # Assert that the log message is captured correctly
    assert "INFO" in caplog.text
    assert "src.core.logger" in caplog.text
    assert "Something happened" in caplog.text


def test_no_duplicate_handlers():
    """
    Test that calling setup_logger() multiple times does not add duplicate handlers.
    """
    logger = setup_logger()
    initial_handler_count = len(logger.handlers)

    logger = setup_logger()

    assert len(logger.handlers) == initial_handler_count
