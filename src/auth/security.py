"""
Provides utility functions for password hashing and JWT token generation
using PyJWT and Passlib.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.core.settings import settings
from src.models import TokenData

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def get_password_hash(password: str) -> bytes:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password.

    Returns:
        str: The hashed password.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password  # type: ignore


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.

    Args:
        plain_password (str): The plain password provided by the user.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    password_byte_enc = plain_password.encode("utf-8")
    hashed_password_byte_enc = hashed_password.encode("utf-8")
    return bcrypt.checkpw(  # type: ignore
        password=password_byte_enc, hashed_password=hashed_password_byte_enc
    )


def create_access_token(data: TokenData) -> str:
    """
    Creates a signed JWT access token with an expiration time.

    Args:
        data (TokenData): The payload to encode into the token.

    Returns:
        str: The encoded JWT token, including an expiration time based on the
             configured access token expiration (in minutes).
    """
    to_encode = data.model_dump()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore


def decode_token(token: str) -> TokenData:
    """
    Decodes and validates a JWT token, returning a TokenData instance.

    Args:
        token (str): The JWT token string.

    Returns:
        TokenData: The decoded token payload.

    Raises:
        jwt.PyJWTError: If the token is invalid or expired.
    """
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return TokenData(**decoded_data)
