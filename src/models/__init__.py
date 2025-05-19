"""
Initialise the models package.

This module provides access to all data models used across the application.
It serves as a central point for importing and exposing individual Pydantic models
to ensure consistency and simplify dependency management.

Example:
    from src.models import Document
"""

from .api_response import ErrorRouteResponse, MessageResponse
from .auth import Token, TokenData, User, UserBase, UserIn
