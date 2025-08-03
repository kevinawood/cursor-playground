# RSS Reader - Quick Reference Guide

## 🚀 Quick Start Commands

### Development
```bash
# Start all services
./docker-start.sh

# Start individual services
docker-compose up -d backend
docker-compose up -d frontend
docker-compose up -d db

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

### Generate PDF Documentation
```bash
./generate-pdf-docs.sh
```

## 📁 Project Structure
```
rss-reader/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── tests/              # Backend tests
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── views/          # Vue components
│   │   ├── config/         # API configuration
│   │   └── utils/          # Utility functions
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Multi-container setup
├── docker-start.sh         # Development startup script
└── TECHNICAL_DOCUMENTATION.md  # Complete technical docs
```

## 🔧 Key Technologies

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls

### Backend
- **Flask**: Lightweight Python web framework
- **SQLAlchemy**: Python ORM for database
- **APScheduler**: Background job scheduling
- **OpenAI API**: AI-powered article summaries
- **BeautifulSoup**: Web scraping for reading time

### Infrastructure
- **Docker**: Containerization
- **PostgreSQL**: Relational database
- **Railway**: Backend hosting
- **Vercel**: Frontend hosting
- **Supabase**: Cloud database

## 🌐 API Endpoints

### Articles
```
GET    /api/articles                    # Get all articles
GET    /api/articles/{id}              # Get specific article
POST   /api/articles/{id}/read         # Mark as read
POST   /api/articles/{id}/bookmark     # Toggle bookmark
GET    /api/articles/{id}/summarize    # AI summary
GET    /api/articles/{id}/reading-time # Reading time
```

### Feeds
```
GET    /api/feeds                      # Get all feeds
POST   /api/feeds                      # Add new feed
DELETE /api/feeds/{id}                 # Remove feed
```

### Statistics
```
GET    /api/stats                      # App statistics
```

## 💾 Database Schema

### Feed Table
```sql
CREATE TABLE feed (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(500) NOT NULL UNIQUE,
    last_fetched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Article Table
```sql
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

## 🔄 Development Workflow

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
```

### Testing
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## 🎨 Key Features

### Frontend Features
- **Dark Mode**: Toggle between light/dark themes
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live feed refreshing
- **Caching**: In-memory caching for performance
- **Hacker News Integration**: Special modal for HN articles

### Backend Features
- **RSS Processing**: Automatic feed fetching
- **AI Summaries**: OpenAI-powered article summaries
- **Reading Time**: Web scraping for accurate estimates
- **Background Jobs**: Scheduled RSS updates
- **Error Handling**: Graceful fallbacks

## 🔐 Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=sk-...
FLASK_ENV=development
PORT=5001
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:5001
```

## 📊 Performance Tips

### Frontend
- Use Vue's `v-memo` for expensive components
- Implement virtual scrolling for large lists
- Cache API responses with Map objects
- Lazy load routes and components

### Backend
- Use database indexes on frequently queried columns
- Implement caching for expensive operations
- Use connection pooling for database
- Background processing for heavy tasks

## 🐛 Common Issues & Solutions

### Docker Permission Issues
```bash
# Fix frontend permissions
sudo chown -R $USER:$USER frontend/
chmod +x *.sh
```

### Database Connection Issues
```bash
# Check database status
docker-compose ps db
docker-compose logs db
```

### API Connection Issues
```bash
# Test backend API
curl http://localhost:5001/api/stats

# Check backend logs
docker-compose logs backend
```

## 📚 Learning Resources

### Vue.js
- [Vue.js Official Guide](https://vuejs.org/guide/)
- [Vue Router Documentation](https://router.vuejs.org/)
- [Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)

### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Multi-stage Builds](https://docs.docker.com/develop/dev-best-practices/multistage-build/)

### Deployment
- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [Supabase Documentation](https://supabase.com/docs)

## 🎯 Next Steps

### Potential Improvements
1. **Mobile App**: React Native or Flutter
2. **Advanced Filtering**: Tags, categories, search
3. **Social Features**: Sharing, recommendations
4. **Analytics**: Reading patterns, popular feeds
5. **Offline Support**: PWA capabilities
6. **Performance**: Redis caching, CDN
7. **Security**: Authentication, rate limiting
8. **Monitoring**: Logging, metrics, alerts

### Learning Path
1. **Frontend**: Master Vue.js, learn React for comparison
2. **Backend**: Explore FastAPI, Django, Node.js
3. **Database**: Learn Redis, MongoDB, database design
4. **DevOps**: Kubernetes, CI/CD, monitoring
5. **Architecture**: Microservices, event-driven design

---

**Remember**: This is a living document. Update it as you learn and improve the application! 