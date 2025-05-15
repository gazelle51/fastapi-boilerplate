# pylint: disable=missing-module-docstring

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from jwt import PyJWTError

from src.auth.dependencies import get_current_user
from src.models import TokenData

app = FastAPI()


# Dependency inclusion
@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    """
    Protected route that requires a valid JWT token to access.

    Args:
        current_user (dict): The current authenticated user, retrieved from the JWT
                             token.
    """
    return current_user


client = TestClient(app)


@patch("src.auth.dependencies.decode_token")
def test_get_current_user_valid_token(mock_decode_token: MagicMock):
    """Test the 'get_current_user' function when the token is valid."""
    mock_decode_token.return_value = TokenData(
        sub="valid_user", exp=datetime.now(timezone.utc) + timedelta(minutes=60)
    )

    token = "valid_token"
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"username": "valid_user"}


@patch("src.auth.dependencies.decode_token")
def test_get_current_user_invalid_token(mock_decode_token: MagicMock):
    """Test the 'get_current_user' function when the token is invalid."""
    mock_decode_token.return_value = MagicMock(sub=None)

    token = "invalid_token"
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


@patch("src.auth.dependencies.decode_token")
def test_get_current_user_invalid_credentials(mock_decode_token: MagicMock):
    """Test the 'get_current_user' function when the credentials are invalid."""
    mock_decode_token.side_effect = PyJWTError("Invalid credentials")

    token = "invalid_credentials"
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_get_current_user_missing_token():
    """Test the 'get_current_user' function when the token is missing."""
    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
