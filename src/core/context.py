"""
Module for managing the context across the application.
"""

from contextvars import ContextVar

trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)
