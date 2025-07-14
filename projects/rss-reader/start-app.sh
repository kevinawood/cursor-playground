#!/bin/bash

# RSS Reader Full App Startup Script
# This script can start the backend, frontend, or both servers

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to start backend
start_backend() {
    echo "🚀 Starting Backend Server..."
    cd "$SCRIPT_DIR/backend"
    source ../venv/bin/activate
    
    # Check if port 5001 is already in use
    if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port 5001 is already in use. Stopping existing process..."
        lsof -ti:5001 | xargs kill -9
        sleep 2
    fi
    
    echo "📍 Backend will be available at: http://localhost:5001"
    python app.py
}

# Function to start frontend
start_frontend() {
    echo "🚀 Starting Frontend Server..."
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
    
    echo "📍 Frontend will be available at: http://localhost:3000"
    npm run dev
}

# Function to start both servers
start_both() {
    echo "🚀 Starting RSS Reader Full Stack..."
    echo "📍 Backend: http://localhost:5001"
    echo "📍 Frontend: http://localhost:3000"
    echo ""
    
    # Start backend in background
    start_backend &
    BACKEND_PID=$!
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend
    start_frontend &
    FRONTEND_PID=$!
    
    # Wait for both processes
    wait $BACKEND_PID $FRONTEND_PID
}

# Parse command line arguments
case "${1:-both}" in
    "backend"|"b")
        start_backend
        ;;
    "frontend"|"f")
        start_frontend
        ;;
    "both"|"all"|"")
        start_both
        ;;
    *)
        echo "Usage: $0 [backend|frontend|both]"
        echo ""
        echo "Options:"
        echo "  backend, b    - Start only the backend server"
        echo "  frontend, f   - Start only the frontend server"
        echo "  both, all     - Start both servers (default)"
        echo ""
        echo "Examples:"
        echo "  $0             # Start both servers"
        echo "  $0 backend     # Start only backend"
        echo "  $0 frontend    # Start only frontend"
        exit 1
        ;;
esac 