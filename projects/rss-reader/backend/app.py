from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import feedparser
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/rss_reader')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False, unique=True)
    category = db.Column(db.String(50), default='General')
    logo_url = db.Column(db.String(500))  # Store the feed logo URL
    last_fetched = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.Text)
    published_date = db.Column(db.DateTime)
    author = db.Column(db.String(200))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Feed
    feed = db.relationship('Feed', backref=db.backref('articles', lazy=True))

# Scheduler for background tasks
scheduler = BackgroundScheduler()
scheduler.start()

def extract_feed_logo(parsed_feed, feed_url):
    """Extract logo URL from RSS feed"""
    logo_url = None
    
    # Try to get logo from feed metadata
    if hasattr(parsed_feed.feed, 'image'):
        logo_url = parsed_feed.feed.image.get('href')
    elif hasattr(parsed_feed.feed, 'logo'):
        logo_url = parsed_feed.feed.logo
    
    # If no logo found, try to extract from the website's favicon
    if not logo_url:
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(feed_url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            logo_url = f"{base_url}/favicon.ico"
        except:
            pass
    
    return logo_url

def fetch_feed_articles(feed_id):
    """Fetch articles from a specific feed"""
    feed = Feed.query.get(feed_id)
    if not feed or not feed.is_active:
        return
    
    try:
        parsed_feed = feedparser.parse(feed.url)
        
        for entry in parsed_feed.entries:
            # Check if article already exists
            existing = Article.query.filter_by(
                feed_id=feed.id,
                link=entry.get('link', '')
            ).first()
            
            if not existing:
                # Parse published date
                published_date = None
                if 'published_parsed' in entry:
                    published_date = datetime(*entry.published_parsed[:6])
                elif 'updated_parsed' in entry:
                    published_date = datetime(*entry.updated_parsed[:6])
                
                # Create new article
                article = Article(
                    feed_id=feed.id,
                    title=entry.get('title', 'No Title'),
                    link=entry.get('link', ''),
                    description=entry.get('summary', ''),
                    published_date=published_date,
                    author=entry.get('author', '')
                )
                db.session.add(article)
        
        # Extract and store logo if not already set
        if not feed.logo_url:
            logo_url = extract_feed_logo(parsed_feed, feed.url)
            if logo_url:
                feed.logo_url = logo_url
        
        feed.last_fetched = datetime.utcnow()
        db.session.commit()
        
    except Exception as e:
        print(f"Error fetching feed {feed.name}: {str(e)}")

def refresh_all_feeds():
    """Refresh all active feeds"""
    feeds = Feed.query.filter_by(is_active=True).all()
    for feed in feeds:
        fetch_feed_articles(feed.id)

# Routes
@app.route('/api/feeds', methods=['GET'])
def get_feeds():
    feeds = Feed.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': feed.id,
        'name': feed.name,
        'url': feed.url,
        'category': feed.category,
        'logo_url': feed.logo_url,
        'last_fetched': feed.last_fetched.isoformat() if feed.last_fetched else None,
        'article_count': Article.query.filter_by(feed_id=feed.id).count()
    } for feed in feeds])

@app.route('/api/feeds', methods=['POST'])
def add_feed():
    data = request.json
    name = data.get('name')
    url = data.get('url')
    category = data.get('category', 'General')
    
    if not name or not url:
        return jsonify({'error': 'Name and URL are required'}), 400
    
    # Check if feed already exists
    existing = Feed.query.filter_by(url=url).first()
    if existing:
        return jsonify({'error': 'Feed already exists'}), 400
    
    # Validate RSS feed
    try:
        parsed = feedparser.parse(url)
        if not parsed.entries:
            return jsonify({'error': 'Invalid RSS feed or no entries found'}), 400
    except:
        return jsonify({'error': 'Could not parse RSS feed'}), 400
    
    feed = Feed(name=name, url=url, category=category)
    db.session.add(feed)
    db.session.commit()
    
    # Fetch initial articles
    fetch_feed_articles(feed.id)
    
    return jsonify({
        'id': feed.id,
        'name': feed.name,
        'url': feed.url,
        'category': feed.category,
        'last_fetched': feed.last_fetched.isoformat() if feed.last_fetched else None
    }), 201

@app.route('/api/feeds/<int:feed_id>', methods=['DELETE'])
def delete_feed(feed_id):
    feed = Feed.query.get_or_404(feed_id)
    feed.is_active = False
    db.session.commit()
    return jsonify({'message': 'Feed deleted successfully'})

@app.route('/api/articles', methods=['GET'])
def get_articles():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    
    query = Article.query.join(Feed).filter(Feed.is_active == True)
    
    if category:
        query = query.filter(Feed.category == category)
    
    if unread_only:
        query = query.filter(Article.is_read == False)
    
    articles = query.order_by(Article.published_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'articles': [{
            'id': article.id,
            'title': article.title,
            'link': article.link,
            'description': article.description,
            'published_date': article.published_date.isoformat() if article.published_date else None,
            'author': article.author,
            'is_read': article.is_read,
            'feed_name': article.feed.name,
            'feed_category': article.feed.category,
            'feed_logo_url': article.feed.logo_url
        } for article in articles.items],
        'total': articles.total,
        'pages': articles.pages,
        'current_page': page
    })

@app.route('/api/articles/<int:article_id>/read', methods=['PUT'])
def mark_as_read(article_id):
    article = Article.query.get_or_404(article_id)
    article.is_read = True
    db.session.commit()
    return jsonify({'message': 'Article marked as read'})

@app.route('/api/articles/<int:article_id>/unread', methods=['PUT'])
def mark_as_unread(article_id):
    article = Article.query.get_or_404(article_id)
    article.is_read = False
    db.session.commit()
    return jsonify({'message': 'Article marked as unread'})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Feed.category).distinct().all()
    return jsonify([category[0] for category in categories])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_feeds = Feed.query.filter_by(is_active=True).count()
    total_articles = Article.query.join(Feed).filter(Feed.is_active == True).count()
    unread_articles = Article.query.join(Feed).filter(
        Feed.is_active == True,
        Article.is_read == False
    ).count()
    
    return jsonify({
        'total_feeds': total_feeds,
        'total_articles': total_articles,
        'unread_articles': unread_articles,
        'read_articles': total_articles - unread_articles
    })

# Schedule feed refresh every 5 minutes
scheduler.add_job(func=refresh_all_feeds, trigger="interval", minutes=5)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001) 