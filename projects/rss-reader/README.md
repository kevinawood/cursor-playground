# RSS Reader

A lightweight RSS feed aggregator built with Vue.js frontend and Flask backend.

## Features

- RSS feed management (add/remove feeds)
- Auto-refresh every 5 minutes
- Bookmarks for saving articles
- Reading progress tracking
- AI-powered article summaries (OpenAI)
- Hacker News discussion integration
- Clean, responsive dark mode interface
- Statistics dashboard

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vue.js 3, Vite, Tailwind CSS |
| **Backend** | Python Flask, SQLAlchemy |
| **Database** | PostgreSQL |
| **Deployment** | Railway (backend), Vercel (frontend), Supabase (database) |

---

## Quick Start

### Docker (Recommended)

```bash
# Prerequisites: Docker and Docker Compose installed
./docker-start.sh
```

Access the app:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001
- **Database**: localhost:5432

### Local Development

```bash
# Start both backend and frontend
./start-app.sh

# Or start individually
./start-app.sh backend
./start-app.sh frontend
```

---

## Project Structure

```
rss-reader/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── wsgi.py             # WSGI entry point
│   ├── cleanup-database.py # Database maintenance utility
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── views/          # Vue page components
│   │   ├── components/     # Reusable components
│   │   ├── config/         # API configuration
│   │   └── utils/          # Utility functions
│   ├── cypress/            # E2E tests
│   ├── tests/              # Unit tests
│   ├── Dockerfile
│   └── package.json
├── scripts/
│   ├── check-env.sh        # Environment diagnostics
│   └── test.sh             # Test runner
├── docker-compose.yml
├── docker-compose.linux.yml
├── docker-start.sh
├── start-app.sh
└── railway.json
```

---

## API Endpoints

### Feeds
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feeds` | List all feeds |
| POST | `/api/feeds` | Add new feed |
| DELETE | `/api/feeds/<id>` | Delete feed |

### Articles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/articles` | List articles (paginated) |
| PUT | `/api/articles/<id>/read` | Mark as read |
| PUT | `/api/articles/<id>/unread` | Mark as unread |
| POST | `/api/articles/<id>/bookmark` | Toggle bookmark |
| GET | `/api/articles/<id>/summarize` | AI summary |

### Other
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | List categories |
| GET | `/api/stats` | App statistics |
| GET | `/health` | Health check |

---

## Configuration

### Environment Variables

Create a `.env` file in `backend/`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Feed Settings
FEED_REFRESH_INTERVAL_MINUTES=30

# Memory Optimization
BATCH_SIZE_FOR_FEED_PROCESSING=10
COMMIT_EVERY_N_ARTICLES=10

# API Settings
FEEDSEARCH_TIMEOUT=15

# Flask
FLASK_ENV=development
FLASK_DEBUG=1

# Optional: AI Summaries
OPENAI_API_KEY=sk-...
```

---

## Docker Commands

```bash
# Start all services
docker-compose up --build -d

# View logs
docker-compose logs -f
docker-compose logs -f backend

# Stop services
docker-compose down

# Reset everything (WARNING: deletes data)
docker-compose down -v
```

---

## Testing

```bash
# Run all tests
./scripts/test.sh

# Backend tests
cd backend && pytest tests/ -v

# Frontend unit tests
cd frontend && npm run test

# E2E tests (requires app running)
cd frontend && npm run test:e2e
```

---

## Database Maintenance

Clean old articles to reduce storage:

```bash
cd backend
python cleanup-database.py
```

---

## Troubleshooting

### Check Environment Status
```bash
./scripts/check-env.sh
```

### Common Issues

**Port already in use:**
```bash
lsof -i :5001  # Check what's using port
docker-compose down  # Stop Docker services
```

**Database connection issues:**
```bash
docker-compose logs db
docker-compose restart db
```

**Permission issues (Linux):**
```bash
sudo chown -R $USER:$USER .
```

**Clean rebuild:**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up --build
```

---

## Deployment

### Production Stack
- **Frontend**: Vercel (auto-deploys from `main`)
- **Backend**: Railway (Docker deployment)
- **Database**: Supabase (PostgreSQL)

### Environment Variables

**Railway:**
- `DATABASE_URL` - Supabase connection string
- `FLASK_ENV=production`
- `FEED_REFRESH_INTERVAL_MINUTES=30`

**Vercel:**
- `VITE_API_URL` - Railway backend URL

---

## Contributing

1. Create a feature branch: `git checkout -b feature-name`
2. Make changes and commit
3. Push and create a Pull Request
4. Merge to `main` after review

---

## Roadmap

- [x] Docker containerization
- [x] Feed management
- [x] Bookmarks
- [x] AI summaries
- [x] Hacker News integration
- [ ] Article search
- [ ] Export/import feeds
- [ ] Dark mode toggle
- [ ] Mobile app
