"""
Application configuration module.

This module defines the application's runtime settings using Pydantic's BaseSettings.
"""

import tomllib

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_version() -> str:
    """Retrieve the application version from the pyproject.toml file.

    Returns:
        str: The version string defined under [tool.poetry.version].
    """
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        return str(data["tool"]["poetry"]["version"])


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """Configuration settings for the application.

    This class defines the configuration settings for the application using
    Pydantic's BaseSettings. It includes default values for various settings
    and loads environment variables to override these defaults.
    """

    # App config
    app_name: str = "FastAPI Boilerplate"
    app_version: str = get_version()
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    rate_limit: str = "100/minute"

    # CORS
    allowed_origins: str = "http://localhost:3000"

    # Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Location of the .env file, can override default settings
    model_config = SettingsConfigDict(env_file=".env")


# This object will be used throughout the application to access configuration settings
settings = Settings()  # pyright: ignore  # type: ignore[call-arg]
