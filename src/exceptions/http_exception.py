"""
Custom exception handler for Pydantic validation errors.
"""

from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.logger import setup_logger
from src.utils.string_utils import to_snake_case

logger = setup_logger(__name__)


def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handles FastAPI HTTPexceptions and returns a structured response.

    Args:
        _ (Request): The incoming request that triggered the exception.
        exc (Exception): The validation exception that was raised.

    Returns:
        JSONResponse: A JSON response with the correct status code and the error
                      message.
    """
    # Pass 500 error on to internal server error handler
    if exc.status_code == 500:
        raise exc

    status_text = HTTPStatus(exc.status_code).phrase
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": to_snake_case(status_text),
            "detail": exc.detail,
        },
    )
