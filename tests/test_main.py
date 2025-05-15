# pylint: disable=missing-module-docstring

from fastapi.testclient import TestClient

from src.main import api

client = TestClient(api)


def test_read_root():
    """Test API call fails without auth."""
    response = client.get("/api/v1")
    assert response.status_code == 401
