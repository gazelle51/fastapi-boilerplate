"""
Custom exception handler for generic errors.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.core.logger import setup_logger

logger = setup_logger(__name__)


def internal_server_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """Handles uncaught exceptions and returns a generic 500 error response.

    Args:
        _ (Request): The incoming request that triggered the exception.
        exc (Exception): The unhandled exception that was raised.

    Returns:
        JSONResponse: A JSON response with a 500 status code and generic error message.
    """
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": "internal_server_error",
            "detail": "Internal server error",
        },
    )
