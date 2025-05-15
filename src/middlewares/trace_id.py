"""
Middleware to attach a unique trace ID to each incoming request.

The trace ID is stored in both the request state and a context variable,
allowing it to be accessed throughout the request lifecycle and included
in logs or response headers for tracing purposes.
"""

import uuid
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.context import trace_id_var


class TraceIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware that generates and attaches a trace ID to each request.

    The trace ID is stored in:
    - request.state.trace_id (available in route handlers)
    - a context variable (used in logging filters)
    - the response header 'X-Trace-ID' for external visibility
    """

    # pylint: disable=too-few-public-methods
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Handles the request lifecycle by injecting a trace ID.

        Args:
            request (Request): The incoming FastAPI request.
            call_next (Callable): The next middleware or route handler.

        Returns:
            Response: The HTTP response with the trace ID added to headers.
        """
        # Generate a unique trace ID
        trace_id = str(uuid.uuid4())

        # Add the trace ID to the request state
        request.state.trace_id = trace_id
        trace_id_var.set(trace_id)

        # Call the next middleware or the actual request handler
        response = await call_next(request)

        # Optionally add the trace ID to response headers
        response.headers["X-Trace-ID"] = trace_id

        return response
