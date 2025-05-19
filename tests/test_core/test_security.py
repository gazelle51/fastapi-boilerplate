# pylint: disable=missing-module-docstring

from datetime import datetime, timedelta, timezone

from src.core.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from src.models import TokenData


def test_get_password_hash():
    """Test hashed password is not equal to the original."""
    password = "test_password"
    hashed_password = get_password_hash(password)
    assert hashed_password != password


def test_verify_password_correct():
    """Test a hashed password matches the correct password."""
    password = "test_password"
    hashed_password = get_password_hash(password).decode("utf-8")
    assert verify_password(password, hashed_password)


def test_verify_password_incorrect():
    """Test a hashed password does not match an incorrect password."""
    password = "test_password"
    hashed_password = get_password_hash(password).decode("utf-8")
    assert not verify_password("wrong_password", hashed_password)


def test_create_access_token():
    """Test the creation of a JWT access token."""
    data = TokenData(
        sub="test_user", exp=datetime.now(timezone.utc) + timedelta(minutes=60)
    )
    token = create_access_token(data)
    assert isinstance(token, str)


def test_decode_access_token():
    """Test the decoding of a JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    data = TokenData(sub="test_user", exp=expire)
    token = create_access_token(data)
    payload = decode_token(token)

    assert payload.sub == "test_user"
    assert payload.exp.replace(microsecond=0) == expire.replace(microsecond=0)
