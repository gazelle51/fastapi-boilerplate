"""
Package initializer for API routes.

This module imports and exposes all FastAPI routers used to define the application's
API routes.
"""

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .auth import router as auth
from .error import router as error
from .index import router as index


class StandardResponse(JSONResponse):
    """
    Custom response class to standardise the response format for success.

    Inherits from `JSONResponse` to provide JSON response functionality.
    """

    def render(self, content: Any) -> bytes:
        """
        Renders the response content by wrapping it in a standardised success format.

        Args:
            content (Any): The original content to include in the response.

        Returns:
            bytes: The serialized JSON response with the standardised structure.
        """
        data_content = {"status": "success", "detail": content}
        return bytes(super().render(data_content))


router = APIRouter(default_response_class=StandardResponse)

# Register API routes
router.include_router(auth, prefix="")
router.include_router(index, prefix="")
router.include_router(error, prefix="/error")
