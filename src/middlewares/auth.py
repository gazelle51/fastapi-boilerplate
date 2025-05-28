"""
Middleware to authenticate and attach user details to each incoming request.

The user data is stored in the request state, allowing it to be accessed throughout the
request lifecycle.
"""

from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.logger import setup_logger
from src.core.security import decode_token
from src.services.users import get_user_base

logger = setup_logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that authenticates the user from a JWT token and attaches the user data
    to each request.

    The user data is stored in:
    - request.state.user
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, app: FastAPI, exclude_paths: list[str]):
        """
        Initialise the middleware with the paths to exclude from authentication.

        Args:
            app: The ASGI application instance.
            exclude_paths (list[str]): List of URL paths to skip authentication for.
        """
        super().__init__(app)
        self.exclude_paths = exclude_paths

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Authenticates user.

        Args:
            request (Request): The incoming FastAPI request.
            call_next (Callable): The next middleware or route handler.

        Returns:
            Response: The HTTP response.
        """
        # Skip routes that don't require auth
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Perform auth
        try:
            token = await oauth2_scheme(request)
            payload = decode_token(token)
            username = payload.sub

            if username is None:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token"},
                )
            # Get user data
            user = get_user_base(username)
            if user is None:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token"},
                )

            logger.info("Username of logged in user: %s", username)

            # Attach user to request
            request.state.user = user

        except PyJWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid credentials"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        return await call_next(request)
