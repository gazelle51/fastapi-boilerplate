# pylint: disable=missing-module-docstring

from fastapi import FastAPI
from fastapi.testclient import TestClient
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.exceptions import rate_limit_handler

app = FastAPI()
limiter = Limiter(key_func=get_remote_address, default_limits=["0/minute"])
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)


@app.get("/test-rate-limit")
def test_rate_limit():
    """A dummy request."""
    return


client = TestClient(app, raise_server_exceptions=False)


def test_rate_limit_handler():
    """
    Test that the rate limit handler correctly processes rate limit exceeded.
    """
    response = client.get("/test-rate-limit")

    # Assert the response properties
    assert response.status_code == 429
    assert response.json() == {
        "status": "error",
        "error": "rate_limit_exceeded",
        "detail": "Rate limit exceeded: 0 per 1 minute",
    }
