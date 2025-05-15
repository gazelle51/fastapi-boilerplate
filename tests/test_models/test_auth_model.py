# pylint: disable=missing-module-docstring

from datetime import datetime, timezone

from src.models import Token, TokenData, User, UserIn


def test_user_model():
    """Test User model loads fields correctly."""
    user_data = {"username": "testuser", "hashed_password": "hashedpassword123"}
    user = User(**user_data)
    assert user.username == "testuser"
    assert user.hashed_password == "hashedpassword123"


def test_user_in_model():
    """Test UserIn model loads fields correctly."""
    user_in_data = {"username": "testuser", "password": "password123"}
    user_in = UserIn(**user_in_data)
    assert user_in.username == "testuser"
    assert user_in.password == "password123"


def test_token_model():
    """Test Token model loads fields correctly."""
    token_data = {"access_token": "some_access_token", "token_type": "bearer"}
    token = Token(**token_data)
    assert token.access_token == "some_access_token"
    assert token.token_type == "bearer"


def test_token_data_model():
    """Test TokenData model loads fields correctly."""
    token_data = {
        "sub": "testuser",
        "exp": datetime.now(timezone.utc),
    }
    token_data_instance = TokenData(**token_data)
    assert token_data_instance.sub == "testuser"
    assert isinstance(token_data_instance.exp, datetime)


def test_token_data_model_no_exp():
    """Test TokenData model loads fields correctly when `exp` is missing."""
    token_data = {"sub": "testuser"}
    token_data_instance = TokenData(**token_data)
    assert token_data_instance.sub == "testuser"
    assert token_data_instance.exp is None
