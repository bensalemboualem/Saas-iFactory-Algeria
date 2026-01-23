#!/bin/bash
set -e

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head
echo "Alembic migrations complete."

# Start Uvicorn
echo "Starting Uvicorn server..."
exec uvicorn main:app --host 0.0.0.0 --port 8212