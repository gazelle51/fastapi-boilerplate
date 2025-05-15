"""
Custom logger setup for the API.
"""

import logging

from src.core.context import trace_id_var


class ColourFormatter(logging.Formatter):
    """Custom logging formatter that applies colour to the log level in the log output
    using ANSI escape sequences.
    """

    RESET = "\x1b[0m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    GREY = "\x1b[38m"
    BOLD_RED = "\x1b[31;1m"

    LEVEL_COLOURS = {
        logging.DEBUG: GREY,
        logging.INFO: BLUE,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD_RED,
    }

    FORMAT_STR = (
        "%(levelname)s: \t  %(asctime)s %(name)s:%(lineno)d [%(trace_id)s] %(message)s"
    )

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with colour applied to the log level.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with the coloured log level.
        """
        log_level = record.levelno
        log_format = self.FORMAT_STR
        level_colour = self.LEVEL_COLOURS.get(log_level, self.RESET)

        # Format colour sections
        record.levelname = f"{level_colour}{record.levelname}{self.RESET}"
        record.trace_id = (
            f"{self.CYAN}{record.trace_id}{self.RESET}"  #  type: ignore[attr-defined]
        )

        # Apply the default formatter with the updated levelname
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


class TraceIDFilter(logging.Filter):
    """Logging filter that injects a trace ID into log records."""

    # pylint: disable=too-few-public-methods
    def filter(self, record: logging.LogRecord) -> bool:
        """Adds a 'trace_id' attribute to the given log record.

        The trace ID is retrieved from a context variable (trace_id_var),
        allowing it to be tied to the current request or execution context.

        Args:
            record (logging.LogRecord): The log record to modify.

        Returns:
            bool: Always returns True to indicate the record should be logged.
        """
        record.trace_id = trace_id_var.get() or "-"
        return True


def setup_logger(name: str = __name__) -> logging.Logger:
    """Configure and return a logger with standard output and formatting.

    This function sets up a logger with the given name. It ensures that
    multiple handlers are not added to the same logger to avoid duplicate
    log messages. The logger outputs to the console and includes timestamps,
    log level, module name, and the log message in its format.

    Args:
        name (str): The name of the logger, typically `__name__` from the calling
                    module.

    Returns:
        logging.Logger: A configured logger instance.
    """

    handler = logging.StreamHandler()
    handler.setFormatter(ColourFormatter())
    handler.addFilter(TraceIDFilter())

    # Custom module logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(handler)

    # Explicitly configure Uvicorn loggers
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.setLevel(logging.INFO)
        uvicorn_logger.handlers = [handler]  # Replace default handler
        uvicorn_logger.propagate = False  # Avoid duplicate logs

    return logger
