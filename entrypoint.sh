#!/bin/bash

# Start the application
echo "Starting application with Gemini API..."
# Navigate to the correct directory if needed, or run from root
# We are in /app
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
