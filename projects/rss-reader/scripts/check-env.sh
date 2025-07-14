#!/bin/bash

# RSS Reader Environment Checker
# This script helps you understand which environment is currently running

echo "🔍 RSS Reader Environment Checker"
echo "=================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check Docker containers
echo ""
echo "🐳 Docker Environment:"
if docker ps | grep -q "rss-reader"; then
    print_status "Docker containers are running"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep rss-reader
else
    print_error "No Docker containers found"
fi

# Check local processes
echo ""
echo "💻 Local Environment:"
if pgrep -f "python.*app.py" > /dev/null; then
    print_status "Local Flask backend is running"
else
    print_error "Local Flask backend is not running"
fi

if pgrep -f "vite" > /dev/null; then
    print_status "Local Vite frontend is running"
else
    print_error "Local Vite frontend is not running"
fi

if brew services list | grep -q "postgresql.*started"; then
    print_status "Local PostgreSQL is running"
else
    print_error "Local PostgreSQL is not running"
fi

# Check port usage
echo ""
echo "🔌 Port Usage:"
for port in 3000 5001 5432; do
    if lsof -i :$port > /dev/null 2>&1; then
        process=$(lsof -i :$port | tail -1 | awk '{print $1}')
        print_status "Port $port: $process"
    else
        print_error "Port $port: Not in use"
    fi
done

# Check API connectivity
echo ""
echo "🌐 API Connectivity:"
if curl -s http://localhost:5001/api/stats > /dev/null 2>&1; then
    print_status "Backend API is responding"
    stats=$(curl -s http://localhost:5001/api/stats | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Feeds: {data[\"total_feeds\"]}, Articles: {data[\"total_articles\"]}')")
    print_info "Stats: $stats"
else
    print_error "Backend API is not responding"
fi

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    print_status "Frontend is responding"
else
    print_error "Frontend is not responding"
fi

# Environment recommendation
echo ""
echo "🎯 Environment Status:"
if docker ps | grep -q "rss-reader" && ! pgrep -f "python.*app.py" > /dev/null && ! pgrep -f "vite" > /dev/null; then
    print_status "You're running in DOCKER mode"
    echo "   - All services are containerized"
    echo "   - Data is in Docker PostgreSQL"
    echo "   - Use: docker-compose logs to see logs"
    echo "   - Use: docker-compose down to stop"
elif pgrep -f "python.*app.py" > /dev/null || pgrep -f "vite" > /dev/null; then
    print_status "You're running in LOCAL mode"
    echo "   - Services are running locally"
    echo "   - Data is in local PostgreSQL"
    echo "   - Use: pkill -f 'python.*app.py' to stop backend"
    echo "   - Use: pkill -f 'vite' to stop frontend"
else
    print_warning "No environment is currently running"
    echo "   - Start Docker: ./docker-start.sh"
    echo "   - Start Local: ./scripts/start-local.sh"
fi

# Check for conflicts
echo ""
echo "⚠️  Conflicts Check:"
conflicts=0

if docker ps | grep -q "rss-reader" && (pgrep -f "python.*app.py" > /dev/null || pgrep -f "vite" > /dev/null); then
    print_warning "Docker and local processes are running simultaneously!"
    print_warning "This may cause port conflicts and data inconsistencies."
    conflicts=1
fi

if [ $conflicts -eq 0 ]; then
    print_status "No conflicts detected"
fi

echo ""
echo "📋 Quick Commands:"
echo "  Check environment: ./scripts/check-env.sh"
echo "  Start Docker: ./docker-start.sh"
echo "  Stop Docker: docker-compose down"
echo "  Start Local: ./scripts/start-local.sh"
echo "  Stop Local: ./scripts/stop-local.sh" 