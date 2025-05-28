# pylint: disable=missing-module-docstring

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from jwt import PyJWTError

from src.middlewares.auth import AuthMiddleware
from src.models import UserBase

app = FastAPI()
app.add_middleware(AuthMiddleware, exclude_paths=["/open"])


@app.get("/open")
def open_route():
    """Open route that doesn't requires a valid JWT token to access."""
    return {"status": "success"}


@app.get("/protected")
def protected_route(request: Request):
    """Protected route that requires a valid JWT token to access."""
    return getattr(request.state, "user", None)


client = TestClient(app)


def test_open_route_no_auth():
    """Test that auth is not required for excluded paths."""
    response = client.get("/open")

    assert response.status_code == 200
    assert response.json() == {"status": "success"}


@patch("src.middlewares.auth.oauth2_scheme", new_callable=AsyncMock)
@patch("src.middlewares.auth.decode_token")
@patch("src.middlewares.auth.get_user_base")
def test_protected_route_with_valid_token(
    mock_get_user_base: MagicMock,
    mock_decode_token: MagicMock,
    mock_oauth2_scheme: AsyncMock,
):
    """
    Test that auth properly executed on a protected route and user details are attached
    to the request state.
    """
    mock_oauth2_scheme.return_value = "validtoken"
    mock_decode_token.return_value = MagicMock(
        sub="testuser", exp=datetime.now(timezone.utc) + timedelta(minutes=60)
    )
    mock_get_user_base.return_value = UserBase(
        username="testuser",
        first_name="Test",
        last_name="User",
        email="testuser@email.com",
    )

    response = client.get("/protected", headers={"Authorization": "Bearer validtoken"})
    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@email.com",
    }


@patch("src.middlewares.auth.oauth2_scheme", new_callable=AsyncMock)
@patch("src.middlewares.auth.decode_token")
def test_protected_route_with_invalid_token(
    mock_decode_token: MagicMock,
    mock_oauth2_scheme: AsyncMock,
):
    """Test the auth middleware when the token is invalid."""
    mock_oauth2_scheme.return_value = "invalidtoken"
    mock_decode_token.return_value = MagicMock(sub=None)

    response = client.get(
        "/protected", headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


@patch("src.middlewares.auth.oauth2_scheme", new_callable=AsyncMock)
@patch("src.middlewares.auth.decode_token")
@patch("src.middlewares.auth.get_user_base")
def test_protected_route_with_missing_user(
    mock_get_user_base: MagicMock,
    mock_decode_token: MagicMock,
    mock_oauth2_scheme: AsyncMock,
):
    """Test the auth middleware when the user is invalid."""
    mock_oauth2_scheme.return_value = "token"
    mock_decode_token.return_value = MagicMock(
        sub="testuser", exp=datetime.now(timezone.utc) + timedelta(minutes=60)
    )
    mock_get_user_base.return_value = None

    response = client.get("/protected", headers={"Authorization": "Bearer token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


@patch("src.middlewares.auth.decode_token")
@patch("src.middlewares.auth.oauth2_scheme", new_callable=AsyncMock)
def test_protected_route_with_invalid_credentials(
    mock_oauth2_scheme: AsyncMock,
    mock_decode_token: MagicMock,
):
    """Test the auth middleware when the credentials are invalid."""
    mock_oauth2_scheme.return_value = "token"
    mock_decode_token.side_effect = PyJWTError("Invalid credentials")

    response = client.get("/protected", headers={"Authorization": "Bearer token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
