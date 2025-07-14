# Docker Setup for RSS Reader

This document explains how to run the RSS Reader using Docker for consistent deployment across different systems.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

## Quick Start

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd rss-reader
   ```

2. **Start all services**:
   ```bash
   ./docker-start.sh
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001
   - Database: localhost:5432

## Manual Docker Commands

### Start Services
```bash
# Build and start all services in background
docker-compose up --build -d

# Start services and follow logs
docker-compose up --build
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This will delete all data)
docker-compose down -v
```

### View Logs
```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Service Management
```bash
# Restart a specific service
docker-compose restart backend

# Rebuild a specific service
docker-compose up --build backend

# Check service status
docker-compose ps
```

## Services Overview

### Database (PostgreSQL)
- **Container**: `rss-reader-db`
- **Port**: 5432
- **Database**: `rss_reader`
- **User**: `rss_user`
- **Password**: `rss_password`
- **Data Persistence**: PostgreSQL data is stored in a Docker volume

### Backend (Flask)
- **Container**: `rss-reader-backend`
- **Port**: 5001
- **Environment**: Development mode with auto-reload
- **Dependencies**: Waits for database to be healthy before starting

### Frontend (Vue.js)
- **Container**: `rss-reader-frontend`
- **Port**: 3000
- **Environment**: Development mode with hot reload
- **Dependencies**: Waits for backend to start

## Development Workflow

### Code Changes
- **Backend**: Changes are automatically detected and the Flask server will reload
- **Frontend**: Changes are automatically detected and Vite will hot-reload
- **Database**: Schema changes require container restart

### Adding Dependencies
- **Backend**: Add to `backend/requirements.txt`, then rebuild:
  ```bash
  docker-compose up --build backend
  ```
- **Frontend**: Add to `frontend/package.json`, then rebuild:
  ```bash
  docker-compose up --build frontend
  ```

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Check what's using the port
   lsof -i :5001
   lsof -i :3000
   lsof -i :5432
   
   # Stop conflicting services
   docker-compose down
   ```

2. **Database connection issues**:
   ```bash
   # Check database logs
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

3. **Build failures**:
   ```bash
   # Clean build
   docker-compose build --no-cache
   docker-compose up --build
   ```

4. **Permission issues**:
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Reset Everything
```bash
# Stop all services and remove everything
docker-compose down -v
docker system prune -f
./docker-start.sh
```

## Production Considerations

This Docker setup is optimized for development. For production:

1. **Use production images** (not development servers)
2. **Add reverse proxy** (Nginx)
3. **Use environment variables** for secrets
4. **Configure proper logging**
5. **Set up monitoring and health checks**
6. **Use Docker secrets** for sensitive data

## Environment Variables

Key environment variables can be customized in `docker-compose.yml`:

- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `DATABASE_URL`: Backend database connection string
- `VITE_API_URL`: Frontend API endpoint

## Data Persistence

- **Database**: PostgreSQL data is persisted in a Docker volume named `postgres_data`
- **Application Data**: Feed and article data is stored in the database
- **Logs**: Container logs are available via `docker-compose logs`

## Performance

- **Development**: Optimized for fast rebuilds and hot reloading
- **Memory**: ~500MB total (PostgreSQL: ~200MB, Backend: ~150MB, Frontend: ~150MB)
- **Startup Time**: ~30-60 seconds for initial build, ~10-15 seconds for subsequent starts 