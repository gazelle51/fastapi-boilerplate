"""
Auth API routes.
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.core.security import create_access_token
from src.core.settings import settings
from src.models import Token, TokenData, UserIn
from src.services.users import authenticate_user, create_user, user_exists

router = APIRouter()


@router.post("/register", response_model=Token)
def register(user_in: UserIn) -> Token:
    """
    Registers a new user and returns a JWT access token.

    Args:
        user_in (UserIn): The user data containing the username and password for
                          registration.

    Raises:
        HTTPException: If the user already exists, raises a 400 error with a relevant
                       message.

    Returns:
        Token: The access token, its type (bearer) and the expiration datetime.
    """
    if user_exists(user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    user = create_user(
        user_in.username,
        user_in.password,
        user_in.first_name,
        user_in.last_name,
        user_in.email,
    )
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = create_access_token(data=TokenData(sub=user.username, exp=expire))

    return Token(
        access_token=access_token, token_type="bearer", expires_at=expire.isoformat()
    )


@router.post("/token", response_model=Token, response_class=JSONResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Authenticates a user and returns a JWT access token using the OAuth2 password flow.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing the user's username
                                               and password. This must include
                                               'grant_type=password' as per the OAuth2
                                               spec.

    Raises:
        HTTPException: If the username or password is incorrect, raises a 401
                       Unauthorized error.

    Returns:
        Token: The access token, its type (bearer) and the expiration datetime.
    """
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = create_access_token(data=TokenData(sub=user.username, exp=expire))

    return Token(
        access_token=access_token, token_type="bearer", expires_at=expire.isoformat()
    )
