# pylint: disable=missing-module-docstring

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient

from src.exceptions.validation_exception import validation_exception_handler

app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/raise-error")
def raise_error():
    """Raises a RequestValidationError."""
    raise RequestValidationError(
        errors=[
            {
                "type": "missing",
                "loc": ["body", "price"],
                "msg": "Field required",
                "input": {"name": "Apple"},
            }
        ]
    )


client = TestClient(app, raise_server_exceptions=False)


def test_validation_exception_handler():
    """
    Test that the custom validation exception handler correctly processes an exception.
    """
    response = client.get("/raise-error")

    # Assert the response properties
    assert response.status_code == 422
    assert response.json() == {
        "status": "error",
        "error": "validation_error",
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "price"],
                "msg": "Field required",
                "input": {"name": "Apple"},
            }
        ],
    }
