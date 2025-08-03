# RSS Reader - Technical Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Backend Implementation](#backend-implementation)
3. [Frontend Implementation](#frontend-implementation)
4. [Database Design](#database-design)
5. [API Design](#api-design)
6. [Caching Strategy](#caching-strategy)
7. [Deployment Architecture](#deployment-architecture)
8. [Development Workflow](#development-workflow)
9. [Key Technical Decisions](#key-technical-decisions)
10. [Performance Considerations](#performance-considerations)

---

## System Architecture

### Overview
The RSS Reader is a full-stack web application built with a modern microservices architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Vue.js)      │◄──►│   (Flask)       │◄──►│  (PostgreSQL)   │
│   Port: 3000    │    │   Port: 5001    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Railway       │    │   Supabase      │
│   (Hosting)     │    │   (Hosting)     │    │   (Cloud DB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Frontend**: Vue.js 3 + Vite + Tailwind CSS
- **Backend**: Python Flask + SQLAlchemy + APScheduler
- **Database**: PostgreSQL (local) / Supabase (production)
- **Containerization**: Docker + Docker Compose
- **Deployment**: Railway (backend) + Vercel (frontend)
- **External APIs**: OpenAI GPT-3.5, RSS feeds, Hacker News API

---

## Backend Implementation

### Core Components

#### 1. Flask Application Structure
```python
# app.py - Main application entry point
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import openai
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
db = SQLAlchemy(app)
scheduler = BackgroundScheduler()
```

#### 2. Database Models
```python
class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    last_fetched = db.Column(db.DateTime, default=datetime.utcnow)
    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.Text)
    published_date = db.Column(db.DateTime)
    is_read = db.Column(db.Boolean, default=False)
    is_bookmarked = db.Column(db.Boolean, default=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    feed_name = db.Column(db.String(100))
```

#### 3. RSS Feed Processing
```python
def fetch_rss_feeds():
    """Background job to fetch and parse RSS feeds"""
    feeds = Feed.query.all()
    for feed in feeds:
        try:
            response = requests.get(feed.url, timeout=10)
            response.raise_for_status()
            
            # Parse XML with feedparser
            parsed_feed = feedparser.parse(response.content)
            
            # Extract and store articles
            for entry in parsed_feed.entries:
                article = Article(
                    title=entry.title,
                    link=entry.link,
                    description=entry.description,
                    published_date=parse_date(entry.published),
                    feed_id=feed.id,
                    feed_name=feed.name
                )
                db.session.add(article)
            
            feed.last_fetched = datetime.utcnow()
            db.session.commit()
            
        except Exception as e:
            print(f"Error fetching {feed.name}: {e}")
```

#### 4. AI Integration (OpenAI)
```python
def summarize_article(article_id):
    """Generate AI summary using OpenAI GPT-3.5"""
    article = Article.query.get_or_404(article_id)
    
    try:
        # Web scraping to get full content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(article.link, timeout=10, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract main content
        content = extract_main_content(soup)
        
        # Generate summary with OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes articles."},
                {"role": "user", "content": f"Summarize this article in 2-3 sentences: {content[:2000]}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Failed to generate summary: {str(e)}"
```

#### 5. Reading Time Calculation
```python
def get_article_reading_time(article_id):
    """Calculate accurate reading time by scraping article content"""
    article = Article.query.get_or_404(article_id)
    
    try:
        # Web scraping with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(article.link, timeout=10, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove irrelevant elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()
        
        # Extract main content using multiple selectors
        content_selectors = [
            'article', '[class*="article"]', '[class*="content"]', 
            '[class*="post"]', 'main', '.entry-content'
        ]
        
        content_text = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                largest_element = max(elements, key=lambda x: len(x.get_text()))
                content_text = largest_element.get_text()
                break
        
        if not content_text:
            content_text = soup.get_text()
        
        # Calculate reading time (200 words per minute)
        word_count = len(content_text.split())
        minutes = max(1, round(word_count / 200))
        
        return {
            'reading_time': f"{minutes} min read",
            'word_count': word_count,
            'minutes': minutes
        }
        
    except Exception as e:
        # Fallback to description-based estimation
        fallback_words = len((article.description or article.title or "").split())
        fallback_minutes = max(1, round(fallback_words * 2 / 200))
        
        return {
            'reading_time': f"{fallback_minutes} min read (estimated)",
            'word_count': fallback_words,
            'minutes': fallback_minutes,
            'note': 'Using fallback estimation'
        }
```

---

## Frontend Implementation

### Core Components

#### 1. Vue.js Application Structure
```javascript
// main.js - Application entry point
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Feeds from './views/Feeds.vue'
import Bookmarks from './views/Bookmarks.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/feeds', component: Feeds },
  { path: '/bookmarks', component: Bookmarks }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
```

#### 2. API Configuration
```javascript
// config/axios.js - Centralized API configuration
import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

const api = axios.create({
  baseURL: baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request/Response interceptors for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('❌ Response Error:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      message: error.message
    })
    return Promise.reject(error)
  }
)

export default api
```

#### 3. Component Architecture
```vue
<!-- Home.vue - Main articles display component -->
<template>
  <div class="flex h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Sidebar -->
    <div class="w-56 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
      <div class="p-4">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Subscribed Feeds</h2>
        <div class="mt-4 space-y-2">
          <div v-for="feed in feeds" :key="feed.id" 
               class="text-sm text-gray-600 dark:text-gray-300">
            {{ feed.name }} ({{ feed.article_count }})
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="flex-1 overflow-auto">
      <div class="p-6">
        <div class="grid gap-6">
          <article v-for="article in articles" :key="article.id"
                   class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <!-- Article content -->
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/config/axios'

export default {
  name: 'Home',
  data() {
    return {
      articles: [],
      feeds: [],
      readingTimeCache: new Map(),
      summaryCache: new Map(),
      loading: false
    }
  },
  methods: {
    async fetchArticles() {
      try {
        this.loading = true
        const response = await api.get('/api/articles')
        this.articles = response.data
      } catch (error) {
        console.error('Error fetching articles:', error)
      } finally {
        this.loading = false
      }
    },
    
    async toggleBookmark(article) {
      try {
        const response = await api.post(`/api/articles/${article.id}/bookmark`)
        article.is_bookmarked = response.data.is_bookmarked
      } catch (error) {
        console.error('Error toggling bookmark:', error)
      }
    },
    
    async summarizeArticle(article) {
      // Check cache first
      if (this.summaryCache.has(article.id)) {
        return this.summaryCache.get(article.id)
      }
      
      try {
        const response = await api.get(`/api/articles/${article.id}/summarize`)
        const summary = response.data.summary
        
        // Cache the result
        this.summaryCache.set(article.id, summary)
        
        return summary
      } catch (error) {
        console.error('Error summarizing article:', error)
        return 'Failed to generate summary'
      }
    },
    
    calculateReadingTime(article) {
      // Check cache first
      if (this.readingTimeCache.has(article.id)) {
        return this.readingTimeCache.get(article.id)
      }
      
      // Fetch accurate reading time
      this.fetchAccurateReadingTime(article)
      return 'Calculating...'
    },
    
    async fetchAccurateReadingTime(article) {
      try {
        const response = await api.get(`/api/articles/${article.id}/reading-time`)
        const result = response.data
        
        // Cache the result
        this.readingTimeCache.set(article.id, result.reading_time)
        
        // Force re-render
        this.$forceUpdate()
      } catch (error) {
        console.error('Error fetching reading time:', error)
        const fallbackTime = this.calculateFallbackReadingTime(article)
        this.readingTimeCache.set(article.id, fallbackTime)
        this.$forceUpdate()
      }
    }
  },
  
  mounted() {
    this.fetchArticles()
    this.fetchFeeds()
  }
}
</script>
```

#### 4. Dark Mode Implementation
```javascript
// App.vue - Dark mode toggle and application state
export default {
  name: 'App',
  data() {
    return {
      darkMode: localStorage.getItem('darkMode') === 'true'
    }
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
      this.applyDarkMode()
    },
    
    applyDarkMode() {
      if (this.darkMode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
  },
  
  mounted() {
    this.applyDarkMode()
  }
}
```

#### 5. Hacker News Integration
```javascript
// utils/hnUtils.js - Hacker News utility functions
export function isHackerNewsArticle(article) {
  return article.feed_name && article.feed_name.includes('Hacker News')
}

export function getHNDiscussionUrl(article) {
  try {
    const url = new URL(article.link)
    const pathParts = url.pathname.split('/')
    const itemId = pathParts[pathParts.length - 1]
    return `https://news.ycombinator.com/item?id=${itemId}`
  } catch (e) {
    return null
  }
}

export function getHNDiscussionUrlBySearch(articleTitle, articleLink) {
  let searchQuery = articleTitle
  try {
    const url = new URL(articleLink)
    const domain = url.hostname.replace('www.', '')
    searchQuery = `${articleTitle} ${domain}`
  } catch (e) {
    searchQuery = articleTitle
  }
  const encodedQuery = encodeURIComponent(searchQuery)
  return `https://hn.algolia.com/?q=${encodedQuery}&sort=byPopularity&prefix=false&page=0&dateRange=all&type=story`
}

export function getHNModalContent(article) {
  const discussionUrl = getHNDiscussionUrl(article)
  const searchUrl = getHNDiscussionUrlBySearch(article.title, article.link)
  
  return {
    title: article.title,
    originalLink: article.link,
    discussionUrl: discussionUrl || searchUrl,
    searchUrl: searchUrl
  }
}
```

---

## Database Design

### Schema Overview
```sql
-- Feeds table
CREATE TABLE feed (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(500) NOT NULL UNIQUE,
    last_fetched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Articles table
CREATE TABLE article (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    link VARCHAR(1000) NOT NULL UNIQUE,
    description TEXT,
    published_date TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    is_bookmarked BOOLEAN DEFAULT FALSE,
    feed_id INTEGER REFERENCES feed(id),
    feed_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Key Design Decisions
1. **Unique Constraints**: Article links are unique to prevent duplicates
2. **Denormalization**: `feed_name` is stored in articles for performance
3. **Indexing**: Indexes on `feed_id`, `is_read`, `is_bookmarked`, `published_date`
4. **Timestamps**: Automatic creation timestamps for tracking

---

## API Design

### RESTful Endpoints

#### Articles
```
GET    /api/articles              # Get all articles with filters
GET    /api/articles/{id}         # Get specific article
POST   /api/articles/{id}/read    # Mark article as read
POST   /api/articles/{id}/bookmark # Toggle bookmark
GET    /api/articles/{id}/summarize # Get AI summary
GET    /api/articles/{id}/reading-time # Get reading time
```

#### Feeds
```
GET    /api/feeds                 # Get all feeds
POST   /api/feeds                 # Add new feed
DELETE /api/feeds/{id}            # Remove feed
```

#### Statistics
```
GET    /api/stats                 # Get application statistics
```

### Response Format
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation completed successfully"
}
```

### Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'message': str(error)
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': str(error)
    }), 500
```

---

## Caching Strategy

### Frontend Caching
```javascript
// In-memory caching for API responses
class CacheManager {
  constructor() {
    this.cache = new Map()
    this.ttl = new Map() // Time-to-live
  }
  
  set(key, value, ttlMs = 300000) { // 5 minutes default
    this.cache.set(key, value)
    this.ttl.set(key, Date.now() + ttlMs)
  }
  
  get(key) {
    if (!this.cache.has(key)) return null
    
    const expiry = this.ttl.get(key)
    if (Date.now() > expiry) {
      this.cache.delete(key)
      this.ttl.delete(key)
      return null
    }
    
    return this.cache.get(key)
  }
  
  clear() {
    this.cache.clear()
    this.ttl.clear()
  }
}

// Usage in components
const cache = new CacheManager()

async function getCachedData(key, fetchFunction) {
  const cached = cache.get(key)
  if (cached) return cached
  
  const data = await fetchFunction()
  cache.set(key, data)
  return data
}
```

### Backend Caching
```python
# Simple in-memory cache for expensive operations
import time
from functools import wraps

cache = {}
cache_ttl = {}

def cached(ttl_seconds=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Check if cached and not expired
            if cache_key in cache:
                if time.time() < cache_ttl.get(cache_key, 0):
                    return cache[cache_key]
                else:
                    del cache[cache_key]
                    del cache_ttl[cache_key]
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[cache_key] = result
            cache_ttl[cache_key] = time.time() + ttl_seconds
            
            return result
        return wrapper
    return decorator

# Usage
@cached(ttl_seconds=600)  # Cache for 10 minutes
def get_article_reading_time(article_id):
    # Expensive web scraping operation
    pass
```

---

## Deployment Architecture

### Production Setup
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Railway       │    │   Supabase      │
│   Frontend      │◄──►│   Backend       │◄──►│   Database      │
│   (CDN)         │    │   (Container)   │    │   (Cloud)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Environment Configuration
```bash
# Frontend (.env)
VITE_API_URL=https://your-backend.railway.app

# Backend (.env)
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=sk-...
FLASK_ENV=production
PORT=5001
```

### Docker Configuration
```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app"]

# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

---

## Development Workflow

### Local Development
```bash
# Start all services
./docker-start.sh

# Or start individually
docker-compose up -d backend
docker-compose up -d frontend
docker-compose up -d db

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature-name

# Make changes and commit
git add .
git commit -m "Add feature description"

# Push and create PR
git push origin feature-name
# Create Pull Request on GitHub

# Merge via PR (not direct push to main)
```

### Testing Strategy
```python
# Backend tests (pytest)
def test_get_articles():
    response = client.get('/api/articles')
    assert response.status_code == 200
    assert 'articles' in response.json

def test_toggle_bookmark():
    response = client.post('/api/articles/1/bookmark')
    assert response.status_code == 200
    assert 'is_bookmarked' in response.json
```

```javascript
// Frontend tests (Vitest)
import { mount } from '@vue/test-utils'
import Home from '@/views/Home.vue'

describe('Home.vue', () => {
  it('displays articles', () => {
    const wrapper = mount(Home)
    expect(wrapper.find('.article-card').exists()).toBe(true)
  })
})
```

---

## Key Technical Decisions

### 1. Technology Choices
- **Vue.js**: Chosen for simplicity and reactivity
- **Flask**: Lightweight Python framework for API
- **PostgreSQL**: Robust relational database
- **Docker**: Consistent development environment
- **Tailwind CSS**: Utility-first CSS for rapid development

### 2. Architecture Decisions
- **Microservices**: Separate frontend/backend for scalability
- **RESTful APIs**: Standard HTTP interface
- **Background Jobs**: APScheduler for RSS fetching
- **Caching**: In-memory caching for performance
- **Error Handling**: Graceful fallbacks throughout

### 3. Performance Optimizations
- **Lazy Loading**: Articles loaded on demand
- **Caching**: API responses and expensive operations
- **Database Indexing**: Optimized queries
- **CDN**: Vercel for frontend delivery
- **Connection Pooling**: Database connection management

### 4. Security Considerations
- **CORS**: Configured for production domains
- **Input Validation**: Sanitized user inputs
- **Rate Limiting**: API request throttling
- **Environment Variables**: Sensitive data protection
- **HTTPS**: SSL/TLS encryption

---

## Performance Considerations

### Frontend Performance
1. **Code Splitting**: Route-based lazy loading
2. **Image Optimization**: WebP format, lazy loading
3. **Bundle Optimization**: Tree shaking, minification
4. **Caching**: Browser cache, service workers
5. **Virtual Scrolling**: For large article lists

### Backend Performance
1. **Database Optimization**: Indexes, query optimization
2. **Connection Pooling**: Efficient database connections
3. **Background Processing**: Async RSS fetching
4. **Caching**: Redis for session data
5. **Load Balancing**: Multiple backend instances

### Monitoring and Analytics
```python
# Performance monitoring
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper
```

---

## Conclusion

This RSS Reader application demonstrates modern full-stack development practices with:

- **Scalable Architecture**: Microservices with clear separation of concerns
- **Modern Technologies**: Vue.js, Flask, PostgreSQL, Docker
- **Performance Optimization**: Caching, lazy loading, background processing
- **User Experience**: Dark mode, responsive design, real-time updates
- **Production Ready**: Cloud deployment, monitoring, error handling

The application serves as an excellent example of how to build a complete web application from concept to production deployment. 