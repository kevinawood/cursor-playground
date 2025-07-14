#!/bin/bash

# RSS Reader Frontend Startup Script
# This script starts the Vue.js frontend development server

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the frontend directory
cd "$SCRIPT_DIR/frontend"

# Check if node_modules exists, if not install dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Check if port 3000 is already in use
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 3000 is already in use. Stopping existing process..."
    lsof -ti:3000 | xargs kill -9
    sleep 2
fi

# Start the Vue.js development server
echo "🚀 Starting RSS Reader Frontend Server..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev 