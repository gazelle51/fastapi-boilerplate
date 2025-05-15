"""
Data models for API route responses.
"""

from pydantic import BaseModel


class ErrorRouteResponse(BaseModel):
    """
    Represents the response returned when an error occurs.

    Attributes:
        detail (str): A descriptive message explaining the error.
    """

    detail: str


class MessageResponse(BaseModel):
    """
    Represents a generic response containing a message.

    Attributes:
        message (str): A descriptive message about the result of the operation.
    """

    message: str
