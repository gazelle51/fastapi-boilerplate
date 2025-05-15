# Use the official Python 3.11.4 image from Docker Hub
FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files to install dependencies
COPY pyproject.toml poetry.lock /app/

# Install poetry and dependencies
RUN pip install --no-cache-dir poetry \
  && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application with Uvicorn for production with multiple workers
CMD poetry run start

