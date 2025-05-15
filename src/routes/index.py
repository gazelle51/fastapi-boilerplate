"""
Index API routes.
"""

from fastapi import APIRouter

from src.models import MessageResponse

router = APIRouter()


@router.get("/", response_model=MessageResponse)
def get_index() -> object:
    """Handles the root route of the API.

    Returns:
        object: A JSON response with a success message and a 200 HTTP status code.
    """
    return MessageResponse(message="Successfully connected to the API")
