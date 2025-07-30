#!/bin/bash

echo "🔍 Validating RSS Reader setup..."

# Check project structure
echo "📁 Checking project structure..."
required_files=(
    "backend/app.py"
    "backend/requirements.txt"
    "backend/Dockerfile"
    "frontend/package.json"
    "frontend/Dockerfile"
    "docker-compose.yml"
)

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

# Check backend dependencies
echo "🐍 Checking backend requirements..."
if grep -q "Flask" backend/requirements.txt; then
    echo "✅ Flask dependency found"
else
    echo "❌ Flask dependency missing"
    exit 1
fi

# Check frontend dependencies
echo "📦 Checking frontend dependencies..."
if grep -q "vue" frontend/package.json; then
    echo "✅ Vue.js dependency found"
else
    echo "❌ Vue.js dependency missing"
    exit 1
fi

# Check Docker configuration
echo "🐳 Checking Docker configuration..."
if grep -q "python:3.11" backend/Dockerfile; then
    echo "✅ Backend Dockerfile uses Python 3.11"
else
    echo "❌ Backend Dockerfile Python version mismatch"
    exit 1
fi

if grep -q "node:18" frontend/Dockerfile; then
    echo "✅ Frontend Dockerfile uses Node 18"
else
    echo "❌ Frontend Dockerfile Node version mismatch"
    exit 1
fi

echo "🎉 All validation checks passed!"
echo "✨ RSS Reader project is properly configured for deployment"