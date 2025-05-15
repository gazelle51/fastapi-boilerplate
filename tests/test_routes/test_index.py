# pylint: disable=missing-module-docstring

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routes.index import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_get_index():
    """
    Test that the root route ("/") returns the correct response with the success
    message.
    """
    response = client.get("/")

    # Assert that the response body contains the expected success message
    assert response.json() == {"message": "Successfully connected to the API"}
