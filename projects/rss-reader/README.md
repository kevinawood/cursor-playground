# RSS Reader

A lightweight RSS feed aggregator built with Vue.js frontend and Flask backend.

## Features

- ✅ RSS feed management (add/remove feeds)
- ✅ Auto-refresh every 5 minutes
- ✅ Clean, minimal interface
- ✅ Feed categorization
- ✅ Reading progress tracking
- ✅ Statistics dashboard
- ✅ Responsive design
- ✅ Pagination

## Tech Stack

- **Frontend**: Vue.js 3 with Composition API
- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Styling**: Tailwind CSS

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Prerequisites: Docker and Docker Compose installed
./docker-start.sh
```

### Option 2: Manual Setup
See [setup.md](./setup.md) for detailed setup instructions.

## Project Structure

```
rss-reader/
├── backend/           # Flask API server
│   ├── app.py        # Main Flask application
│   ├── requirements.txt
│   ├── Dockerfile    # Backend container configuration
│   └── env.example   # Environment configuration template
├── frontend/         # Vue.js frontend
│   ├── src/
│   │   ├── views/    # Vue components
│   │   ├── App.vue   # Main app component
│   │   └── main.js   # App entry point
│   ├── package.json
│   ├── Dockerfile    # Frontend container configuration
│   └── vite.config.js
├── docker-compose.yml # Multi-container orchestration
├── docker-start.sh   # Docker startup script
└── setup.md          # Setup instructions
```

## API Endpoints

- `GET /api/feeds` - List all feeds
- `POST /api/feeds` - Add new feed
- `DELETE /api/feeds/<id>` - Delete feed
- `GET /api/articles` - List articles with pagination
- `PUT /api/articles/<id>/read` - Mark article as read
- `PUT /api/articles/<id>/unread` - Mark article as unread
- `GET /api/categories` - List all categories
- `GET /api/stats` - Get statistics

## Testing

The project includes comprehensive testing across all layers:

### Quick Test Commands
```bash
# Run all tests
./scripts/test.sh

# Backend tests only
cd backend && pytest tests/ -v

# Frontend tests only
cd frontend && npm run test

# E2E tests
cd frontend && npm run test:e2e
```

### Test Coverage
- **Backend**: Unit tests for API endpoints, database models, and business logic
- **Frontend**: Component tests with Vitest and Vue Test Utils
- **E2E**: Full application testing with Cypress
- **CI/CD**: Automated testing on GitHub Actions

See [TESTING.md](./TESTING.md) for detailed testing documentation.

## Roadmap

- [x] Docker containerization for consistent deployment
- [x] Side panel with subscribed feeds for article filtering
- [x] Comprehensive testing suite
- [ ] Reddit timeline integration
- [ ] Spotify new releases
- [ ] Rotten Tomatoes movie/show tracking
- [ ] Article search functionality
- [ ] Export/import feeds
- [ ] Mobile app
- [ ] Article bookmarks
- [ ] Reading time estimates
- [ ] Dark mode theme
- [ ] Enhanced feed search with query parameters (search by domain, keywords, etc.) 