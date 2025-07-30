#!/bin/bash

# Build script for production deployment
echo "Building frontend for production..."

# Set the production API URL
export VITE_API_URL=https://your-railway-app-name.railway.app

# Build the application
npm run build

echo "Build complete! Deploy the 'dist' folder to Vercel or Netlify." 