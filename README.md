# FastAPI Boilerplate

This repository can be used as a boilerplate for creating APIs in Python. It uses FastAPI for the web framework and Poetry for dependency management and development workflow.

## Table of Contents

- [FastAPI Boilerplate](#fastapi-boilerplate)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Install Python](#install-python)
    - [Install Poetry](#install-poetry)
    - [Enable Virtual Environment Inside Project](#enable-virtual-environment-inside-project)
    - [Install Dependencies](#install-dependencies)
    - [Set Up Pre-commit Hooks](#set-up-pre-commit-hooks)
      - [Windows Users](#windows-users)
  - [Running the App](#running-the-app)
    - [Environment Variables](#environment-variables)
    - [Development Mode](#development-mode)
    - [Production Mode](#production-mode)
  - [Authentication](#authentication)
    - [Obtain a Token](#obtain-a-token)
    - [Use the Token](#use-the-token)
  - [API Documentation](#api-documentation)
  - [Developing the App](#developing-the-app)
    - [Add Dependencies](#add-dependencies)
    - [Add Development Dependencies](#add-development-dependencies)
    - [Run Unit Tests](#run-unit-tests)
    - [Manually Run Pre-commit Hooks](#manually-run-pre-commit-hooks)
  - [Features](#features)

## Project Structure

```
.
├── scripts/                  # Custom scripts used by Poetry scripts
├── src/
│   ├── auth/                 # Authentication logic (JWT, hashing, dependencies)
│   ├── core/                 # App configuration (settings, logger, constants)
│   ├── exceptions/           # Custom exception handlers and error responses
│   ├── middlewares/          # Custom FastAPI middlewares
│   ├── models/               # Pydantic models
│   ├── routes/               # API endpoints
│   ├── services/             # Logic and external integrations
│   ├── utils/                # Helper functions and utilities
│   └── main.py               # FastAPI app entry point
├── tests/                    # Unit tests
├── .env_template             # Template for environment variables
├── .gitignore                # Git ignored files
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── .python-version           # Python version specification
├── Dockerfile                # Docker configuration for the app
├── poetry.lock               # Locked versions of dependencies
├── pyproject.toml            # Project metadata and dependencies for Poetry
└── README.md                 # Project overview and setup instructions
```

## Getting Started

### Install Python

Ensure you have the correct version of Python installed, as specified in the `.python-version` file.

### Install Poetry

Poetry is used to manage dependencies and virtual environments. To install Poetry, run:

```bash
pip install poetry
```

### Enable Virtual Environment Inside Project

To keep the virtual environment inside the project directory, configure Poetry by running:

```bash
poetry config virtualenvs.in-project true
```

### Install Dependencies

Install the project dependencies using Poetry:

```bash
poetry install
```

This will set up the virtual environment and install all required dependencies.

### Set Up Pre-commit Hooks

To install pre-commit hooks for code quality checks (linting, formatting, etc.), run:

```bash
poetry run pre-commit install
```

These hooks include:

- `black` for code formatting
- `isort` for import sorting
- `pylint` for linting
- `mypy` for static type checking

#### Windows Users

Adjust `.pre-commit-config.yaml` to ensure the correct path for `pylint`:

- Change `entry: .venv/bin/pylint` to `entry: .venv/Scripts/pylint`.

## Running the App

### Environment Variables

Create a `.env` file in the project root by copying the provided `.env_template`.

```bash
cp .env_template .env
```

Update the values as needed. **Do not commit the `.env` file** to version control, as it may contain sensitive information such as API keys or secrets.

To generate a secure random secret key for the `SECRET_KEY` variable:

```bash
openssl rand -hex 32
```

### Development Mode

To run the app in development mode with hot-reloading:

```bash
poetry run start-dev
```

### Production Mode

To run the app in production mode:

```bash
poetry run start
```

## Authentication

The API uses JWT-based authentication. By default, the issued Bearer token will expire after 60 minutes.

### Obtain a Token

Send a `POST` request to `/api/v1/token` with valid credentials provided as form-data:

```json
{
  "username": "your_user",
  "password": "your_password",
  "grant_type": "password"
}
```

### Use the Token

Include the access token in the `Authorization` header for protected routes:

```
Authorization: Bearer <your_token>
```

## API Documentation

After starting the app, access the automatically generated API docs: http://localhost:8000/docs.

## Developing the App

### Add Dependencies

To add a new dependency to the project:

```bash
poetry add <package-name>
```

### Add Development Dependencies

To add dependencies that are only needed for development (like linters, testing tools), use the `-D` flag:

```bash
poetry add -D <package-name>
```

### Run Unit Tests

To run the unit tests and generate code coverage reports:

```bash
poetry run pytest
```

### Manually Run Pre-commit Hooks

To run hooks manually:

```bash
poetry run pre-commit run --all-files
```

## Features

This application contains the following features:

- FastAPI framework
- Poetry dependency management
- Pre-commit checks
  - `black` for code formatting
  - `isort` for import sorting
  - `pylint` for linting
  - `mypy` for static type checking
- Settings and environment variables
- Unit testing with `pytest`
- Models and validation with `pydantic`
- Logging
- Request tracing
- Custom error handlers
- Custom response models
- CORS
- Rate limiting
- JWT authentication
- A sample Dockerfile
- Auto-generated Swagger documentation
