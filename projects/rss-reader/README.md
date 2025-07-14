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

See [setup.md](./setup.md) for detailed setup instructions.

## Project Structure

```
rss-reader/
├── backend/           # Flask API server
│   ├── app.py        # Main Flask application
│   ├── requirements.txt
│   └── env.example   # Environment configuration template
├── frontend/         # Vue.js frontend
│   ├── src/
│   │   ├── views/    # Vue components
│   │   ├── App.vue   # Main app component
│   │   └── main.js   # App entry point
│   ├── package.json
│   └── vite.config.js
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

## Roadmap

- [ ] Reddit timeline integration
- [ ] Spotify new releases
- [ ] Rotten Tomatoes movie/show tracking
- [ ] Article search functionality
- [ ] Export/import feeds
- [ ] Mobile app
- [ ] Article bookmarks
- [ ] Reading time estimates 