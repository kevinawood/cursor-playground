# RSS Reader Configuration

This document explains the configurable settings for the RSS Reader application.

## Environment Variables

You can configure the application by setting these environment variables in your `.env` file:

### Feed Refresh Settings

- `FEED_REFRESH_INTERVAL_MINUTES` (default: 15)
  - How often the application automatically fetches new articles from RSS feeds
  - Set to 15 minutes by default to reduce server load and memory usage

### Memory Optimization Settings

- `BATCH_SIZE_FOR_FEED_PROCESSING` (default: 10)
  - Number of feeds to process in each batch during refresh
  - Lower values use less memory but may be slower

- `COMMIT_EVERY_N_ARTICLES` (default: 10)
  - How often to commit new articles to the database during processing
  - Lower values use less memory but may be slower

### API Settings

- `FEEDSEARCH_TIMEOUT` (default: 15)
  - Timeout in seconds for feed search API calls
  - Increase if you experience timeout errors

### Database Configuration

- `DATABASE_URL` (required)
  - PostgreSQL connection string
  - Example: `postgresql://username:password@localhost/rss_reader`

### Flask Settings

- `FLASK_DEBUG` (default: False)
  - Enable Flask debug mode
  - Set to `true` for development

## Example .env File

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/rss_reader

# Feed Refresh Settings
FEED_REFRESH_INTERVAL_MINUTES=15

# Memory Optimization Settings
BATCH_SIZE_FOR_FEED_PROCESSING=10
COMMIT_EVERY_N_ARTICLES=10

# API Settings
FEEDSEARCH_TIMEOUT=15

# Flask Settings
FLASK_DEBUG=False

# OpenAI API (for article summarization)
OPENAI_API_KEY=your_openai_api_key_here
```

## Railway Deployment Considerations

For Railway deployment, consider these settings to prevent OOM errors:

```bash
# More conservative settings for Railway
FEED_REFRESH_INTERVAL_MINUTES=30
BATCH_SIZE_FOR_FEED_PROCESSING=5
COMMIT_EVERY_N_ARTICLES=5
FEEDSEARCH_TIMEOUT=10
```

## Changing Settings

1. Update your `.env` file with the desired values
2. Restart the application:
   ```bash
   # For Docker
   docker-compose down && docker-compose up -d
   
   # For local development
   # Restart your Flask application
   ```

## Memory Optimization Features

The application now includes several memory optimization features:

1. **Batch Processing**: Feeds are processed in small batches
2. **Regular Commits**: Database commits happen frequently to prevent memory buildup
3. **Session Cleanup**: Database sessions are cleared after each feed
4. **Garbage Collection**: Forced garbage collection after refresh cycles
5. **Error Handling**: Individual feed errors don't stop the entire refresh process 