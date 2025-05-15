# pylint: disable=missing-module-docstring

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.exceptions.internal_server_error import internal_server_error_handler

app = FastAPI()
app.add_exception_handler(Exception, internal_server_error_handler)


@app.get("/raise-error")
def raise_error():
    """Raises an Exception."""
    # pylint: disable=broad-exception-raised
    raise Exception("There is a bug on line 25")


client = TestClient(app, raise_server_exceptions=False)


def test_internal_server_error_handler():
    """
    Test that the custom HTTPException handler correctly processes a generic HTTP
    exception.
    """
    response = client.get("/raise-error")

    # Assert the response properties
    assert response.status_code == 500
    assert response.json() == {
        "status": "error",
        "error": "internal_server_error",
        "detail": "Internal server error",
    }
