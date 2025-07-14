#!/bin/bash

# RSS Reader Local Stop Script
# This script stops the application running in local mode

echo "🛑 Stopping RSS Reader in LOCAL mode"
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

# Stop backend
echo ""
echo "🔧 Stopping Flask backend..."
if [ -f "backend.pid" ]; then
    BACKEND_PID=$(cat backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        print_status "Backend stopped (PID: $BACKEND_PID)"
    else
        print_warning "Backend process not found"
    fi
    rm -f backend.pid
else
    # Try to find and kill any running Flask processes
    if pgrep -f "python.*app.py" > /dev/null; then
        pkill -f "python.*app.py"
        print_status "Backend processes stopped"
    else
        print_warning "No backend processes found"
    fi
fi

# Stop frontend
echo ""
echo "🎨 Stopping Vue frontend..."
if [ -f "frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        print_status "Frontend stopped (PID: $FRONTEND_PID)"
    else
        print_warning "Frontend process not found"
    fi
    rm -f frontend.pid
else
    # Try to find and kill any running Vite processes
    if pgrep -f "vite" > /dev/null; then
        pkill -f "vite"
        print_status "Frontend processes stopped"
    else
        print_warning "No frontend processes found"
    fi
fi

# Stop PostgreSQL (optional - ask user)
echo ""
echo "🗄️  PostgreSQL is still running"
echo "   This is normal as other applications might be using it"
echo "   To stop PostgreSQL: brew services stop postgresql@14"

echo ""
print_status "Local RSS Reader stopped!"
echo ""
echo "🔍 To check status: ./scripts/check-env.sh"
echo "🚀 To start Docker: ./docker-start.sh"
echo "💻 To start local again: ./scripts/start-local.sh" 