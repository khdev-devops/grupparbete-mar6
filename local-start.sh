#!/bin/bash

# Default to port 5000 if no argument is provided
APP_PORT=${1:-5000}

echo "Starting the application on port $APP_PORT..."

# Run docker-compose with the specified or default port
APP_PORT=$APP_PORT docker compose up --build

# Check if docker-compose failed
if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Docker Compose failed to start. Maybe port $APP_PORT was already in use?"
    echo
    echo "Usage: ./local-start.sh [PORT]"
    echo "Example: ./local-start.sh 5001 (to run on port 5001)"
    exit 1
fi