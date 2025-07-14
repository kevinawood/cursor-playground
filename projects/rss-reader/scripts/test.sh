#!/bin/bash

# RSS Reader Test Suite
# This script runs all tests for the RSS reader application

set -e

echo "🧪 Running RSS Reader Test Suite"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Start Docker services for testing
echo "🐳 Starting Docker services..."
docker-compose up -d db
sleep 5

# Backend Tests
echo ""
echo "🔧 Running Backend Tests..."
cd backend

# Install test dependencies if not already installed
if [ ! -f "venv/bin/activate" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt

# Run backend tests
print_status "Running pytest..."
pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Check test results
if [ $? -eq 0 ]; then
    print_status "Backend tests passed!"
else
    print_error "Backend tests failed!"
    exit 1
fi

cd ..

# Frontend Tests
echo ""
echo "🎨 Running Frontend Tests..."
cd frontend

# Install dependencies
npm install

# Run unit tests
print_status "Running Vitest..."
npm run test:coverage

# Check test results
if [ $? -eq 0 ]; then
    print_status "Frontend unit tests passed!"
else
    print_error "Frontend unit tests failed!"
    exit 1
fi

cd ..

# E2E Tests (optional)
echo ""
echo "🌐 Running E2E Tests..."
echo "Note: E2E tests require the application to be running"
echo "Start the app with: ./scripts/start.sh"
echo "Then run: cd frontend && npm run test:e2e"

# Summary
echo ""
echo "=================================="
print_status "Test suite completed!"
echo ""
echo "📊 Coverage reports:"
echo "  Backend: backend/htmlcov/index.html"
echo "  Frontend: frontend/coverage/index.html"
echo ""
echo "🎯 To run specific tests:"
echo "  Backend: cd backend && pytest tests/test_api.py -v"
echo "  Frontend: cd frontend && npm run test"
echo "  E2E: cd frontend && npm run test:e2e" 