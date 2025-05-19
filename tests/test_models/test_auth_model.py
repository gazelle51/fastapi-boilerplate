# pylint: disable=missing-module-docstring

from datetime import datetime, timedelta, timezone

from src.models import Token, TokenData, User, UserIn


def test_user_model():
    """Test User model loads fields correctly."""
    user_data = {
        "username": "testuser",
        "hashed_password": "hashedpassword123",
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@email.com",
    }
    user = User(**user_data)
    assert user.username == "testuser"
    assert user.hashed_password == "hashedpassword123"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.email == "testuser@email.com"


def test_user_in_model():
    """Test UserIn model loads fields correctly."""
    user_in_data = {
        "username": "testuser",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@email.com",
    }
    user_in = UserIn(**user_in_data)
    assert user_in.username == "testuser"
    assert user_in.password == "password123"
    assert user_in.first_name == "Test"
    assert user_in.last_name == "User"
    assert user_in.email == "testuser@email.com"


def test_token_model():
    """Test Token model loads fields correctly."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    token_data = {
        "access_token": "some_access_token",
        "token_type": "bearer",
        "expires_at": expire,
    }
    token = Token(**token_data)
    assert token.access_token == "some_access_token"
    assert token.token_type == "bearer"
    assert token.expires_at == expire


def test_token_data_model():
    """Test TokenData model loads fields correctly."""
    token_data = {
        "sub": "testuser",
        "exp": datetime.now(timezone.utc),
    }
    token_data_instance = TokenData(**token_data)
    assert token_data_instance.sub == "testuser"
    assert isinstance(token_data_instance.exp, datetime)
