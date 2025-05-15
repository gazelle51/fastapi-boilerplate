# pylint: disable=missing-module-docstring

import asyncio

from src.core.context import trace_id_var


def test_set_and_get_trace_id():
    """Test that trace_id_var can be set and retrieved in the current context."""
    token = trace_id_var.set("abc123")
    assert trace_id_var.get() == "abc123"
    trace_id_var.reset(token)  # Clean up after test


def test_default_trace_id():
    """Test that trace_id_var returns None by default when not explicitly set."""
    assert trace_id_var.get() is None


async def set_and_get_in_task(value):
    """
    Helper coroutine that sets and retrieves a value in trace_id_var after an async
    delay.
    """
    trace_id_var.set(value)
    await asyncio.sleep(0.1)  # simulate async work
    return trace_id_var.get()


def test_context_isolation_across_async_tasks():
    """Test that trace_id_var values are isolated across concurrent async tasks."""

    async def run_tasks():
        return await asyncio.gather(
            set_and_get_in_task("A"),
            set_and_get_in_task("B"),
        )

    results = asyncio.run(run_tasks())
    assert results == ["A", "B"]
