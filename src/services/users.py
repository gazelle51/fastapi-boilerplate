"""
Fake user database. To be replaced.
"""

from src.core.security import get_password_hash, verify_password
from src.models import User, UserBase

# Simulated user DB
fake_users_db = {
    "user": User(
        username="user",
        hashed_password=get_password_hash("password"),
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@testuser.com",
    )
}


def user_exists(username: str) -> bool:
    """
    Checks if a user already exists in the fake user database.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return username in fake_users_db


def get_user(username: str) -> User | None:
    """
    Retrieves a user from the fake user database by username.

    Args:
        username (str): The username to search for in the database.

    Returns:
        Optional[User]: The user if found, otherwise None.
    """
    return fake_users_db.get(username)


def get_user_base(username: str) -> UserBase | None:
    """
    Retrieves a user from the fake user database by username but does not return
    password.

    Args:
        username (str): The username to search for in the database.

    Returns:
        Optional[UserBase]: The user if found, otherwise None.
    """
    user_data = fake_users_db.get(username)
    if user_data:
        return UserBase(**user_data.model_dump(exclude={"hashed_password"}))
    return None


def create_user(
    username: str, password: str, first_name: str, last_name: str, email: str
) -> User:
    """
    Creates a new user, hashes the password, and stores the user in the fake user
    database.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.

    Returns:
        User: The newly created user.
    """
    hashed_password = get_password_hash(password)
    user = User(
        username=username,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    fake_users_db[username] = user
    return user


def authenticate_user(username: str, password: str) -> User | None:
    """
    Authenticates a user by checking the password.

    Args:
        username (str): The username to authenticate.
        password (str): The password to authenticate.

    Returns:
        Optional[User]: The user if authentication is successful, otherwise None.
    """
    user = get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
