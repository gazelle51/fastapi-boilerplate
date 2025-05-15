# pylint: disable=missing-module-docstring

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from src.core.context import trace_id_var
from src.middlewares.trace_id import TraceIdMiddleware

app = FastAPI()
app.add_middleware(TraceIdMiddleware)


@app.get("/trace-id")
def get_trace_id(request: Request):
    """
    Endpoint for testing if the trace ID is properly set in the request state
    and context variable, and if it's returned correctly in the response.
    """
    # Retrieve the trace ID from request state and context var
    trace_id_from_state = request.state.trace_id
    trace_id_from_context = trace_id_var.get()

    return {
        "trace_id_state": trace_id_from_state,
        "trace_id_context": trace_id_from_context,
    }


client = TestClient(app)


def test_trace_id_in_response_header_and_body():
    """
    Test that the trace ID is properly generated, attached to the response header,
    and that it matches the trace ID in both the request state and the context variable.
    `"""
    response = client.get("/trace-id")
    body = response.json()

    # Check trace ID is in response header
    trace_id_header = response.headers.get("X-Trace-ID")
    assert trace_id_header is not None

    # Check trace ID is set in request.state and context var (and they match)
    assert body["trace_id_state"] == trace_id_header
    assert body["trace_id_context"] == trace_id_header
