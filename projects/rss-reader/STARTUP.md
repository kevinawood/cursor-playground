# RSS Reader - Quick Startup Guide

This guide shows you how to quickly start the RSS Reader application using the provided startup scripts.

## 🚀 Quick Start

### Option 1: Setup Aliases (Recommended)
Run this once to set up convenient aliases:
```bash
./setup-aliases.sh
source ~/.zshrc  # or ~/.bashrc
```

Then use these simple commands:
```bash
rss-start    # Start both backend and frontend
rss-backend  # Start only backend
rss-frontend # Start only frontend
```

### Option 2: Direct Script Execution
```bash
./start-app.sh        # Start both servers
./start-backend.sh    # Start only backend
./start-frontend.sh   # Start only frontend
```

### Option 3: Manual Commands
```bash
# Backend
cd backend && source ../venv/bin/activate && python app.py

# Frontend
cd frontend && npm run dev
```

## 📋 Available Commands

| Command | Description | Port |
|---------|-------------|------|
| `rss-start` | Start both backend and frontend | 5001, 3000 |
| `rss-backend` | Start only backend server | 5001 |
| `rss-frontend` | Start only frontend server | 3000 |
| `rss-both` | Start both servers (same as rss-start) | 5001, 3000 |
| `rss-b` | Short for backend only | 5001 |
| `rss-f` | Short for frontend only | 3000 |

## 🔧 Features

The startup scripts include:
- ✅ Automatic virtual environment activation
- ✅ Port conflict detection and resolution
- ✅ Dependency installation (frontend)
- ✅ Clear status messages
- ✅ Easy-to-remember aliases

## 🌐 Access Points

Once started, access the application at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001/api/

## 🛠️ Troubleshooting

### Port Already in Use
The scripts automatically detect and kill processes using the required ports.

### Virtual Environment Issues
If you get virtual environment errors:
```bash
cd backend
python -m venv ../venv
source ../venv/bin/activate
pip install -r requirements.txt
```

### Frontend Dependencies
If frontend doesn't start:
```bash
cd frontend
npm install
```

## 📝 Notes

- The backend requires PostgreSQL to be running
- The backend auto-refreshes feeds every 5 minutes
- Both servers run in development mode with hot reloading 