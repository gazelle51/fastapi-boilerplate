"""
Data models for auth.
"""

from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    """Data model representing a user in the system."""

    username: str
    hashed_password: str


class UserIn(BaseModel):
    """Data model representing input data for user registration or login."""

    username: str
    password: str


class Token(BaseModel):
    """Data model representing an authentication token."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data model for the JWT token payload."""

    sub: str  # The subject (e.g., user ID or username)
    exp: datetime | None = None  # The expiration time of the token
