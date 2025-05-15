"""
Provides FastAPI dependency functions related to authentication.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from .security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency function to retrieve the currently authenticated user from the JWT token.

    Args:
        token (str): JWT access token from the Authorization header.

    Returns:
        dict: A dictionary containing the user's data from the token payload.

    Raises:
        HTTPException: If the token is invalid or missing.
    """
    try:
        payload = decode_token(token)
        username = payload.sub

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        return {"username": username}

    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
