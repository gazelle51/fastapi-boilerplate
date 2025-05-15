"""
Fake user database. To be replaced.
"""

from src.auth.security import get_password_hash, verify_password
from src.models import User

# Simulated user DB
fake_users_db = {
    "user": User(username="user", hashed_password=get_password_hash("password"))
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


def create_user(username: str, password: str) -> User:
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
    user = User(username=username, hashed_password=hashed_password)
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
