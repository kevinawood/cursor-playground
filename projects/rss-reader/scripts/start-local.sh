#!/bin/bash

# RSS Reader Local Startup Script
# This script starts the application using local services

set -e

echo "🚀 Starting RSS Reader in LOCAL mode"
echo "===================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Docker is running and stop it
if docker ps | grep -q "rss-reader"; then
    print_warning "Docker containers are running. Stopping them first..."
    docker-compose down
    sleep 3
fi

# Start local PostgreSQL
echo ""
echo "🗄️  Starting local PostgreSQL..."
if ! brew services list | grep -q "postgresql.*started"; then
    brew services start postgresql@14
    sleep 5
    print_status "PostgreSQL started"
else
    print_status "PostgreSQL already running"
fi

# Create database if it doesn't exist
echo ""
echo "📊 Setting up database..."
createdb rss_reader 2>/dev/null || print_status "Database already exists"

# Start backend
echo ""
echo "🔧 Starting Flask backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -f "venv/bin/activate" ]; then
    print_warning "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Start backend in background
python app.py &
BACKEND_PID=$!
echo $BACKEND_PID > ../backend.pid
print_status "Backend started (PID: $BACKEND_PID)"

cd ..

# Wait for backend to start
echo ""
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is responding
if curl -s http://localhost:5001/api/stats > /dev/null; then
    print_status "Backend is responding"
else
    print_error "Backend failed to start"
    exit 1
fi

# Start frontend
echo ""
echo "🎨 Starting Vue frontend..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    print_warning "Installing frontend dependencies..."
    npm install
fi

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../frontend.pid
print_status "Frontend started (PID: $FRONTEND_PID)"

cd ..

# Wait for frontend to start
echo ""
echo "⏳ Waiting for frontend to start..."
sleep 10

# Check if frontend is responding
if curl -s http://localhost:3000 > /dev/null; then
    print_status "Frontend is responding"
else
    print_error "Frontend failed to start"
    exit 1
fi

echo ""
echo "🎉 RSS Reader started in LOCAL mode!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5001"
echo ""
echo "📊 Database:"
echo "   Host: localhost"
echo "   Port: 5432"
echo "   Database: rss_reader"
echo "   User: kevinanaro-wood"
echo ""
echo "🛑 To stop: ./scripts/stop-local.sh"
echo "🔍 To check status: ./scripts/check-env.sh" 