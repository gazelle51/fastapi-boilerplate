# pylint: disable=missing-module-docstring

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.main import api

client = TestClient(api)


def test_read_root():
    """Test API call fails without auth."""
    with pytest.raises(HTTPException) as exc_info:
        client.get("/api/v1")
    assert exc_info.value.status_code == 401
