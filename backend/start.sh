#!/bin/bash
set -e

# 1. Ensure all required runtime directories exist
echo "Ensuring runtime directories exist..."
mkdir -p data generated_images uploads exports

# 2. Execute alembic upgrade head to apply all database migrations
echo "Running database migrations..."
alembic upgrade head

# 3. Execute database seed script to populate benchmark prompts
echo "Seeding benchmark prompts..."
python -m backend.app.database.seed

# 4. Start the FastAPI application
echo "Starting the application..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
