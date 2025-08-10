from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import feedparser
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv
import openai
from bs4 import BeautifulSoup

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
    is_bookmarked = db.Column(db.Boolean, default=False)  # New bookmark field
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
                
                # Truncate article title if it's too long (database limit is 500 characters)
                title = entry.get('title', 'No Title')
                if len(title) > 500:
                    title = title[:497] + "..."
                
                # Create new article
                article = Article(
                    feed_id=feed.id,
                    title=title,
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
    with app.app_context():
        print(f"🔄 Starting scheduled feed refresh at {datetime.utcnow()}")
        feeds = Feed.query.filter_by(is_active=True).all()
        print(f"📰 Found {len(feeds)} active feeds to refresh")
        for feed in feeds:
            print(f"🔄 Refreshing feed: {feed.name}")
            fetch_feed_articles(feed.id)
        print(f"✅ Feed refresh completed at {datetime.utcnow()}")

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
    
    # Truncate feed name if it's too long (database limit is 100 characters)
    if len(name) > 100:
        name = name[:97] + "..."
        print(f"📝 Truncated feed name to: {name}")
    
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
    feed_id = request.args.get('feed_id', type=int)
    
    query = Article.query.join(Feed).filter(Feed.is_active == True)
    
    if category:
        query = query.filter(Feed.category == category)
    
    if unread_only:
        query = query.filter(Article.is_read == False)
    
    if feed_id:
        query = query.filter(Article.feed_id == feed_id)
    
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
            'is_bookmarked': article.is_bookmarked,
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

@app.route('/api/articles/<int:article_id>/bookmark', methods=['PUT'])
def toggle_bookmark(article_id):
    article = Article.query.get_or_404(article_id)
    article.is_bookmarked = not article.is_bookmarked
    db.session.commit()
    return jsonify({
        'message': 'Article bookmarked' if article.is_bookmarked else 'Article unbookmarked',
        'is_bookmarked': article.is_bookmarked
    })

@app.route('/api/articles/bookmarked', methods=['GET'])
def get_bookmarked_articles():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Article.query.filter_by(is_bookmarked=True).order_by(Article.created_at.desc())
    
    # Add feed information
    articles = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # Get total count for pagination
    total = query.count()
    pages = (total + per_page - 1) // per_page
    
    articles_data = []
    for article in articles:
        articles_data.append({
            'id': article.id,
            'title': article.title,
            'link': article.link,
            'description': article.description,
            'published_date': article.published_date.isoformat() if article.published_date else None,
            'author': article.author,
            'is_read': article.is_read,
            'is_bookmarked': article.is_bookmarked,
            'feed_name': article.feed.name,
            'feed_logo_url': article.feed.logo_url,
            'created_at': article.created_at.isoformat()
        })
    
    return jsonify({
        'articles': articles_data,
        'pages': pages,
        'total': total,
        'current_page': page
    })

@app.route('/api/articles/<int:article_id>/summarize', methods=['POST'])
def summarize_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    # Check if OpenAI API key is configured
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        return jsonify({'error': 'OpenAI API key not configured'}), 500
    
    try:
        # Try to fetch the article content with headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        try:
            # Reduced timeout for Railway and egress optimization
            response = requests.get(article.link, timeout=3, headers=headers)  # Reduced from 5 to 3 seconds
            response.raise_for_status()
            
            # Check content size to prevent memory issues and reduce egress
            content_length = len(response.content)
            if content_length > 512 * 1024:  # Reduced from 1MB to 512KB for egress optimization
                raise Exception("Article content too large for processing")
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements to reduce memory usage
            for script in soup(["script", "style", "nav", "header", "footer", "aside", "iframe", "embed"]):
                script.decompose()
            
            # Extract text content with size limits
            text = soup.get_text()
            
            # Clean up the text efficiently
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit text length to avoid token limits and memory issues, and reduce egress
            if len(text) > 2000:  # Reduced from 3000 to 2000 for egress optimization
                text = text[:2000] + "..."
            
            # Clear memory
            del soup, response
                
        except requests.RequestException as e:
            # If we can't fetch the full article, use the description as fallback
            if article.description:
                text = article.description[:500]  # Reduced from 1000 to 500 for egress optimization
            else:
                return jsonify({
                    'error': f'Unable to fetch article content. The website may be blocking requests. You can try reading the article directly: {article.link}'
                }), 500
        except Exception as e:
            # Handle memory or other errors gracefully
            if "memory" in str(e).lower() or "out of memory" in str(e).lower():
                # Use description as fallback
                text = article.description[:500] if article.description else article.title  # Reduced from 1000 to 500
            else:
                raise e
        
        # Create the prompt for summarization
        prompt = f"""
        Please provide a brief, engaging summary of this article's introduction and main points. 
        Focus on what the article is about without giving away all the details.
        Keep it under 150 words and make it compelling enough to decide if it's worth reading.
        
        Article title: {article.title}
        Article content: {text}
        """
        
        # Get summary from OpenAI with reduced tokens for egress optimization
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates engaging, concise summaries of articles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,  # Reduced from 150 to 100 for egress optimization
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        
        # Clear memory
        del text, prompt, response
        
        return jsonify({
            'summary': summary,
            'article_title': article.title
        })
        
    except Exception as e:
        error_msg = str(e)
        
        # Check if it's a quota exceeded error
        if "quota" in error_msg.lower() or "billing" in error_msg.lower():
            # Provide a helpful message with fallback summary
            fallback_summary = f"AI summary temporarily unavailable due to API quota limits. Here's a brief overview: {article.title} - {article.description[:200] if article.description else 'Click to read the full article.'}"
            
            return jsonify({
                'summary': fallback_summary,
                'article_title': article.title,
                'note': 'This is a fallback summary due to API quota limits. Please check your OpenAI billing status.'
            })
        elif "memory" in error_msg.lower() or "out of memory" in error_msg.lower():
            # Handle memory errors gracefully
            fallback_summary = f"Summary temporarily unavailable due to system limits. Here's a brief overview: {article.title} - {article.description[:200] if article.description else 'Click to read the full article.'}"
            
            return jsonify({
                'summary': fallback_summary,
                'article_title': article.title,
                'note': 'This is a fallback summary due to system memory limits.'
            })
        else:
            return jsonify({'error': f'Failed to generate summary: {error_msg}'}), 500

@app.route('/api/articles/<int:article_id>/reading-time', methods=['GET'])
def get_article_reading_time(article_id):
    """Get accurate reading time by scraping article content with memory and egress optimization"""
    article = Article.query.get_or_404(article_id)
    
    # Check if we have a cached reading time in the database
    # (You could add a reading_time field to the Article model for permanent caching)
    
    try:
        # Use the same headers as the summarize endpoint
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Reduced timeout for Railway and egress optimization
        response = requests.get(article.link, timeout=3, headers=headers)  # Reduced from 5 to 3 seconds
        response.raise_for_status()
        
        # Check content size to prevent memory issues and reduce egress
        content_length = len(response.content)
        if content_length > 512 * 1024:  # Reduced from 1MB to 512KB for egress optimization
            raise Exception("Article content too large for processing")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements to reduce memory usage
        for script in soup(["script", "style", "nav", "header", "footer", "aside", "iframe", "embed"]):
            script.decompose()
        
        # Try to find the main article content with memory-efficient approach
        content_selectors = [
            'article',
            '[class*="article"]',
            '[class*="content"]',
            '[class*="post"]',
            '[class*="story"]',
            'main',
            '.entry-content',
            '.post-content',
            '.article-content',
            '.story-content'
        ]
        
        content_text = ""
        
        # Try each selector with size limits
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                # Get text from the largest element (likely the main content)
                largest_element = max(elements, key=lambda x: len(x.get_text()))
                content_text = largest_element.get_text()
                
                # Limit content size to prevent memory issues and reduce egress
                if len(content_text) > 25000:  # Reduced from 50KB to 25KB for egress optimization
                    content_text = content_text[:25000]
                break
        
        # If no specific content found, use body text with limits
        if not content_text:
            content_text = soup.get_text()
            if len(content_text) > 25000:  # Reduced from 50KB to 25KB for egress optimization
                content_text = content_text[:25000]
        
        # Clean the text efficiently
        lines = (line.strip() for line in content_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Count words with limit
        words = text.split()
        word_count = min(len(words), 5000)  # Reduced from 10,000 to 5,000 for egress optimization
        
        # Calculate reading time (200 words per minute)
        reading_speed = 200
        minutes = max(1, round(word_count / reading_speed))
        
        # Format the result
        if minutes < 60:
            reading_time = f"{minutes} min read"
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                reading_time = f"{hours}h read"
            else:
                reading_time = f"{hours}h {remaining_minutes}m read"
        
        # Clear memory
        del soup, response, content_text, text, words
        
        return jsonify({
            'reading_time': reading_time,
            'word_count': word_count,
            'minutes': minutes,
            'url': article.link
        })
        
    except requests.RequestException as e:
        # Fallback to description-based estimation
        fallback_words = len((article.description or article.title or "").split())
        fallback_minutes = max(1, round(fallback_words * 2 / 200))  # Assume description is ~1/2 of article
        
        return jsonify({
            'reading_time': f"{fallback_minutes} min read (estimated)",
            'word_count': fallback_words,
            'minutes': fallback_minutes,
            'url': article.link,
            'note': 'Using fallback estimation - could not fetch article content'
        })
    except Exception as e:
        # Enhanced error handling for memory issues
        error_msg = str(e)
        if "memory" in error_msg.lower() or "out of memory" in error_msg.lower():
            return jsonify({
                'reading_time': '5 min read (estimated)',
                'word_count': 1000,
                'minutes': 5,
                'url': article.link,
                'note': 'Memory limit reached - using conservative estimate'
            }), 200  # Return 200 instead of 500 to prevent frontend errors
        
        return jsonify({'error': f'Failed to calculate reading time: {error_msg}'}), 500

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
    bookmarked_articles = Article.query.filter_by(is_bookmarked=True).count()
    
    return jsonify({
        'total_feeds': total_feeds,
        'total_articles': total_articles,
        'unread_articles': unread_articles,
        'read_articles': total_articles - unread_articles,
        'bookmarked_articles': bookmarked_articles
    })

@app.route('/api/feed-search')
def feed_search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing query'}), 400

    feeds = []
    
    # Use feedsearch.dev API - the most reliable RSS discovery service
    try:
        # Prepare the URL for feedsearch.dev
        # If query doesn't have http, assume it's a domain
        if not query.startswith('http'):
            search_url = f"https://feedsearch.dev/api/v1/search?url={query}"
        else:
            search_url = f"https://feedsearch.dev/api/v1/search?url={query}"
        
        resp = requests.get(search_url, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            
            # Process feedsearch.dev results
            for feed in data:
                if feed.get('url'):  # Only include feeds with valid URLs
                    feeds.append({
                        'title': feed.get('title', 'Unknown Feed'),
                        'url': feed['url'],
                        'website': feed.get('site_url', ''),
                        'description': feed.get('description', ''),
                        'favicon': feed.get('favicon', '')
                    })
        
        elif resp.status_code == 400:
            # Bad request - try with https:// prefix
            if not query.startswith('http'):
                search_url = f"https://feedsearch.dev/api/v1/search?url=https://{query}"
                resp = requests.get(search_url, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    for feed in data:
                        if feed.get('url'):
                            feeds.append({
                                'title': feed.get('title', 'Unknown Feed'),
                                'url': feed['url'],
                                'website': feed.get('site_url', ''),
                                'description': feed.get('description', ''),
                                'favicon': feed.get('favicon', '')
                            })
                            
    except Exception as e:
        print(f"Feedsearch.dev error: {str(e)}")

    return jsonify({'feeds': feeds})

@app.route('/api/refresh-feeds', methods=['POST'])
def manual_refresh_feeds():
    refresh_all_feeds()
    return jsonify({'message': 'Feeds refreshed successfully'})

# Schedule feed refresh with configurable interval (default 30 minutes for egress optimization)
feed_refresh_interval = int(os.getenv('FEED_REFRESH_INTERVAL_MINUTES', 30))
scheduler.add_job(func=refresh_all_feeds, trigger="interval", minutes=feed_refresh_interval)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port) 