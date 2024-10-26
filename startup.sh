#!/bin/bash
set -euo pipefail

export OPENAI_API_KEY=$(cat .env | grep OPENAI_API_KEY | awk -F'=' '{print $2}')
export DATABASE_URL=$(cat .env | grep DATABASE_URL | awk -F'=' '{print $2}')

# Check if the environment variables are set
if [ -z "$OPENAI_API_KEY" ] || [ -z "$DATABASE_URL" ]; then
  echo "Error: Environment variables not set. Please ensure .env file is present and contains OPENAI_API_KEY and DATABASE_URL."
  exit 1
fi

# Check if the virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Error: Virtual environment not activated. Please activate the virtual environment before running this script."
  exit 1
fi

# Ensure the database is created and configured
# - Check if the database exists
if ! psql -lqt | grep -q "request_response_system"; then
  echo "Creating database request_response_system..."
  createdb request_response_system
fi

# - Connect to the database and create the extension for encryption
psql -U postgres -d request_response_system -c "CREATE EXTENSION IF NOT EXISTS pgcrypto"

# Start the FastAPI application using uvicorn
echo "Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Handle any errors during startup
if [ $? -ne 0 ]; then
  echo "Error: FastAPI application failed to start."
  exit 1
fi