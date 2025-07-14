#!/bin/bash

# RSS Reader Backend Startup Script
# This script starts the Flask backend server with proper virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the backend directory
cd "$SCRIPT_DIR/backend"

# Activate virtual environment
source ../venv/bin/activate

# Check if port 5001 is already in use
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5001 is already in use. Stopping existing process..."
    lsof -ti:5001 | xargs kill -9
    sleep 2
fi

# Start the Flask application
echo "🚀 Starting RSS Reader Backend Server..."
echo "📍 Server will be available at: http://localhost:5001"
echo "📊 API endpoints: http://localhost:5001/api/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py 