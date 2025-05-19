"""
Data models for auth.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base user model containing common fields shared across different user-related
    models.
    """

    username: str = Field(..., min_length=3)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr


class User(UserBase):
    """User model with hashed password stored in the system."""

    hashed_password: str


class UserIn(UserBase):
    """User model representing input data for user registration or login."""

    password: str


class Token(BaseModel):
    """Data model representing an authentication token."""

    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class TokenData(BaseModel):
    """Data model for the JWT token payload."""

    sub: str  # The subject (e.g., user ID or username)
    exp: datetime  # The expiration time of the token
