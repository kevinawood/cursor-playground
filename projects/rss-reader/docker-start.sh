#!/bin/bash

# RSS Reader Docker Startup Script
# This script starts the RSS reader using Docker Compose

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Detect OS and set up environment accordingly
OS_TYPE="$(uname -s)"
if [ "$OS_TYPE" = "Linux" ]; then
    echo "🐧 Detected Linux - setting up UID/GID for volume permissions..."
    export DOCKER_UID=$(id -u)
    export DOCKER_GID=$(id -g)
    # Fix frontend directory permissions on Linux
    if [ -d "./frontend" ]; then
        sudo chown -R $DOCKER_UID:$DOCKER_GID ./frontend 2>/dev/null || true
    fi
else
    echo "🍎 Detected macOS/other - Docker Desktop handles permissions automatically"
    # Set empty values so docker-compose doesn't fail
    export DOCKER_UID=""
    export DOCKER_GID=""
fi

echo "🐳 Starting RSS Reader with Docker Compose..."
echo "📍 Backend: http://localhost:5001"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Database: localhost:5432"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose down

# Build and start the services
echo "🔨 Building and starting services..."
if [ "$OS_TYPE" = "Linux" ]; then
    # Use Linux override file for proper UID/GID mapping
    docker-compose -f docker-compose.yml -f docker-compose.linux.yml up --build -d
else
    docker-compose up --build -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ RSS Reader is starting up!"
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "🔧 Backend API will be available at: http://localhost:5001"
echo ""
echo "📝 Useful commands:"
echo "  docker-compose logs -f    # View logs"
echo "  docker-compose down       # Stop services"
echo "  docker-compose restart    # Restart services"
echo ""
echo "Press Ctrl+C to stop the services"
echo ""

# Follow logs
docker-compose logs -f 