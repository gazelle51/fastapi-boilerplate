"""
Application entrypoint.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.logger import setup_logger
from src.core.settings import settings
from src.exceptions import (
    http_exception_handler,
    internal_server_error_handler,
    rate_limit_handler,
    validation_exception_handler,
)
from src.middlewares import AuthMiddleware, TraceIdMiddleware
from src.routes import router


def create_app() -> FastAPI:
    """
    Initialize and configure the FastAPI application.

    This function sets up the FastAPI application with the specified title,
    version, and debug mode. It adds CORS middleware to allow cross-origin
    requests from specified origins. It includes the API router.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """

    # Set up logging
    logger = setup_logger(__name__)
    logger.info("FastAPI application started")

    # Initialize the FastAPI application with settings from the configuration
    app = FastAPI(
        title=settings.app_name, version=settings.app_version, debug=settings.debug
    )

    # Rate limiter, use IP address as key
    limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
    app.state.limiter = limiter

    # Add middlewares
    app.add_middleware(TraceIdMiddleware)
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins.split(","),
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
        ],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "X-Requested-With",
            "User-Agent",
            "Cache-Control",
            "Cookie",
        ],
    )
    app.add_middleware(
        AuthMiddleware, exclude_paths=[settings.api_v1_prefix + "/token"]
    )

    # Register routers
    app.include_router(router, prefix=settings.api_v1_prefix)

    # Register exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
    app.add_exception_handler(Exception, internal_server_error_handler)

    return app


# Create the FastAPI application instance
api = create_app()
