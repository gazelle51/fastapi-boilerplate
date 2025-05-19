# pylint: disable=missing-module-docstring

from datetime import datetime
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.models import User
from src.routes.auth import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


@patch("src.routes.auth.user_exists")
@patch("src.routes.auth.create_user")
@patch("src.routes.auth.create_access_token")
def test_register_success(
    mock_create_access_token: MagicMock,
    mock_create_user: MagicMock,
    mock_user_exists: MagicMock,
):
    """Test the registration route when user doesn't exist."""
    mock_user_exists.return_value = False
    mock_create_user.return_value = User(
        username="new_user",
        hashed_password="hashed",
        first_name="New",
        last_name="User",
        email="newuser@email.com",
    )
    mock_create_access_token.return_value = "mocked_access_token"

    user_in = {
        "username": "new_user",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "email": "newuser@email.com",
    }
    response = client.post("/register", json=user_in)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["access_token"] == "mocked_access_token"
    assert response_json["token_type"] == "bearer"
    assert datetime.fromisoformat(
        response_json["expires_at"].replace("Z", "+00:00")
    )  # Assert ISO format


@patch("src.routes.auth.user_exists")
def test_register_user_exists(mock_user_exists: MagicMock):
    """Test the registration route when the user already exists."""
    mock_user_exists.return_value = True

    user_in = {
        "username": "existing_user",
        "password": "password123",
        "first_name": "Existing",
        "last_name": "User",
        "email": "existinguser@email.com",
    }
    response = client.post("/register", json=user_in)

    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


@patch("src.routes.auth.authenticate_user")
@patch("src.routes.auth.create_access_token")
def test_login_success(
    mock_create_access_token: MagicMock, mock_authenticate_user: MagicMock
):
    """Test the login route when credentials are correct."""
    mock_authenticate_user.return_value = User(
        username="new_user",
        hashed_password="hashed",
        first_name="New",
        last_name="User",
        email="newuser@email.com",
    )
    mock_create_access_token.return_value = "mocked_access_token"

    response = client.post(
        "/token",
        data={
            "username": "user",
            "password": "password123",
            "grant_type": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["access_token"] == "mocked_access_token"
    assert response_json["token_type"] == "bearer"
    assert datetime.fromisoformat(
        response_json["expires_at"].replace("Z", "+00:00")
    )  # Assert ISO format


@patch("src.routes.auth.authenticate_user")
def test_login_invalid_credentials(mock_authenticate_user: MagicMock):
    """Test the login route when credentials are incorrect."""
    mock_authenticate_user.return_value = None

    response = client.post(
        "/token",
        data={
            "username": "user",
            "password": "wrongpassword",
            "grant_type": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
