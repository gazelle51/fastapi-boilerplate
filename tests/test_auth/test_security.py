# pylint: disable=missing-module-docstring

import jwt

from src.auth.security import (
    ALGORITHM,
    SECRET_KEY,
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
    data = TokenData(sub="test_user")
    token = create_access_token(data)
    assert isinstance(token, str)


def test_create_access_token_with_expiration():
    """Test that the access token contains an 'exp' field."""
    data = TokenData(sub="test_user")
    token = create_access_token(data)

    # Decode the token to check the payload
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert "exp" in decoded_payload


def test_decode_access_token():
    """Test the decoding of a JWT access token."""
    data = TokenData(sub="test_user")
    token = create_access_token(data)
    payload = decode_token(token)

    assert payload.sub == "test_user"
    assert "exp" in payload.model_dump()
