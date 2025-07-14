# RSS Reader Setup Instructions

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL

## Backend Setup

1. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE rss_reader;
   ```

2. **Set up Python environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

4. **Run the backend:**
   ```bash
   python app.py
   ```

## Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Run the development server:**
   ```bash
   npm run dev
   ```

## Usage

1. Open http://localhost:3000 in your browser
2. Go to the "Feeds" tab to add RSS feeds
3. View articles on the "Articles" tab
4. Feeds automatically refresh every 5 minutes

## Example RSS Feeds

- TechCrunch: https://techcrunch.com/feed/
- Hacker News: https://news.ycombinator.com/rss
- Reddit Programming: https://www.reddit.com/r/programming/.rss
- Ars Technica: https://feeds.arstechnica.com/arstechnica/index

## Features

- ✅ RSS feed management
- ✅ Auto-refresh every 5 minutes
- ✅ Article categorization
- ✅ Read/unread status
- ✅ Clean, responsive UI
- ✅ Pagination
- ✅ Statistics dashboard

## Roadmap

- [ ] Reddit timeline integration
- [ ] Spotify new releases
- [ ] Rotten Tomatoes integration
- [ ] Article search
- [ ] Export/import feeds
- [ ] Mobile app 