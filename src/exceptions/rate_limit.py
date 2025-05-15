"""
Custom exception handler for rate limit exceeded.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from src.core.logger import setup_logger

logger = setup_logger(__name__)


def rate_limit_handler(_: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Handles rate limit exceeded errors and returns a structured 429 response.

    Args:
        _ (Request): The incoming request that triggered the exception.
        exc (RateLimitExceeded): The exception indicating the rate limit was exceeded.

    Returns:
        JSONResponse: A JSON response with a 429 status code and an error message.
    """
    logger.error("Rate limit exceeded error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "status": "error",
            "error": "rate_limit_exceeded",
            "detail": "Rate limit exceeded: " + exc.detail,
        },
    )
