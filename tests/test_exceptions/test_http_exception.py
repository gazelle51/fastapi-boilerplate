# pylint: disable=missing-module-docstring

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from src.exceptions.http_exception import http_exception_handler

app = FastAPI()
app.add_exception_handler(HTTPException, http_exception_handler)


@app.get("/raise-error")
def raise_error():
    """Raises an HTTPException with a 404 status code and a 'Not found' message."""
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/raise-error-500")
def raise_error_500():
    """Raises an HTTPException with a 500 status code."""
    raise HTTPException(status_code=500, detail="Some error")


client = TestClient(app, raise_server_exceptions=False)


def test_http_exception_handler():
    """
    Test that the custom HTTP exception handler correctly processes a HTTP exception.
    """
    response = client.get("/raise-error")

    # Assert the response properties
    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "error": "not_found",
        "detail": "Not found",
    }


def test_http_exception_handler_500():
    """
    Test that the custom HTTP exception handler re-raises 500 errors.
    """
    response = client.get("/raise-error-500")

    # Assert the response properties
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
