"""
Custom exception handler for Pydantic validation errors.
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.logger import setup_logger

logger = setup_logger(__name__)


def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handles Pydantic validation errors and returns a structured 422 response.

    Args:
        _ (Request): The incoming request that triggered the exception.
        exc (Exception): The validation exception that was raised.

    Returns:
        JSONResponse: A JSON response with a 422 status code and the error message.
    """
    logger.error("Validation error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error": "validation_error",
            "detail": exc.errors(),
        },
    )
