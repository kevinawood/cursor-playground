#!/bin/bash

# RSS Reader Docker Startup Script
# This script starts the RSS reader using Docker Compose

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Export UID and GID for Linux compatibility
export DOCKER_UID=$(id -u)
export DOCKER_GID=$(id -g)

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
docker-compose up --build -d

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