# pylint: disable=missing-module-docstring

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routes.error import router

app = FastAPI()
app.include_router(router)

client = TestClient(app, raise_server_exceptions=False)


def test_force():
    """Test that the /force route returns a 500 status code."""
    response = client.get("/force")

    assert response.status_code == 500
