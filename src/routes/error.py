"""
Test API routes to ensure functionality for errors.
"""

from fastapi import APIRouter

from src.models import ErrorRouteResponse

router = APIRouter()


@router.get("/force", response_model=ErrorRouteResponse)
def force_error() -> ErrorRouteResponse:
    """Forces an error to be raised when this route is accessed.

    This route is typically used for testing error handling.
    It raises a generic Exception with a predefined message.

    Raises:
        Exception: A forced exception with the message "This is a forced error".
    """
    raise Exception("This is a forced error")  # pylint: disable=broad-exception-raised
