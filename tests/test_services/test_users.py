# pylint: disable=missing-module-docstring

from src.services.users import (
    authenticate_user,
    create_user,
    get_user,
    get_user_base,
    user_exists,
)


def test_user_exists_true():
    """Test that user_exists returns True for an existing user."""
    assert user_exists("user") is True


def test_user_exists_false():
    """Test that user_exists returns False for a non-existing user."""
    assert user_exists("nonexistent_user") is False


def test_get_user_existing():
    """Test that get_user returns a user when the user exists."""
    user = get_user("user")
    assert user is not None
    assert user.username == "user"


def test_get_user_non_existing():
    """Test that get_user returns None for a non-existing user."""
    user = get_user("nonexistent_user")
    assert user is None


def test_get_user_base_existing():
    """Test that get_user returns a user base when the user exists."""
    user = get_user_base("user")
    assert user is not None
    assert user.username == "user"
    assert not hasattr(user, "hashed_password")


def test_get_user_base_non_existing():
    """Test that get_user returns None for a non-existing user."""
    user = get_user_base("nonexistent_user")
    assert user is None


def test_create_user_success():
    """Test that create_user successfully creates a new user."""
    new_user = create_user(
        "new_user", "newpassword", "New", "User", "newuser@email.com"
    )
    assert new_user.username == "new_user"
    assert new_user.hashed_password != "newpassword"  # Password should be hashed
    assert new_user.first_name == "New"
    assert new_user.last_name == "User"
    assert new_user.email == "newuser@email.com"


def test_create_user_duplicate():
    """Test that create_user does not overwrite an existing user."""
    create_user(
        "existing_user", "password123", "Existing", "User", "existinguser@email.com"
    )
    new_user = create_user(
        "existing_user", "newpassword", "Existing", "User", "existinguser@email.com"
    )
    assert new_user.username == "existing_user"
    assert new_user.hashed_password != "newpassword"


def test_authenticate_user_success():
    """Test that authenticate_user returns the user when credentials are correct."""
    user = authenticate_user("user", "password")
    assert user is not None
    assert user.username == "user"


def test_authenticate_user_wrong_password():
    """Test that authenticate_user returns None when the password is incorrect."""
    user = authenticate_user("user", "wrongpassword")
    assert user is None


def test_authenticate_user_non_existing_user():
    """Test that authenticate_user returns None when the user does not exist."""
    user = authenticate_user("nonexistent_user", "password")
    assert user is None
