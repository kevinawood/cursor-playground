import pytest
import json
from unittest.mock import patch, MagicMock
from app import db, Feed, Article

class TestFeedAPI:
    """Test cases for feed-related API endpoints."""
    
    def test_get_feeds_empty(self, client):
        """Test getting feeds when none exist."""
        response = client.get('/api/feeds')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_get_feeds_with_data(self, client, app_context):
        """Test getting feeds when they exist."""
        # Create a test feed
        feed = Feed(name='Test Feed', url='https://example.com/rss.xml', category='Technology')
        db.session.add(feed)
        db.session.commit()
        
        response = client.get('/api/feeds')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['name'] == 'Test Feed'
        assert data[0]['url'] == 'https://example.com/rss.xml'
    
    @patch('app.feedparser.parse')
    def test_add_feed_success(self, mock_parse, client):
        """Test successfully adding a new feed."""
        # Mock feedparser to return valid RSS data
        mock_feed = MagicMock()
        mock_feed.entries = [MagicMock()]
        mock_parse.return_value = mock_feed
        
        feed_data = {
            'name': 'Test Feed',
            'url': 'https://example.com/rss.xml',
            'category': 'Technology'
        }
        
        response = client.post('/api/feeds', 
                             data=json.dumps(feed_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test Feed'
        assert data['url'] == 'https://example.com/rss.xml'
    
    def test_add_feed_missing_data(self, client):
        """Test adding a feed with missing required data."""
        feed_data = {'name': 'Test Feed'}  # Missing URL
        
        response = client.post('/api/feeds',
                             data=json.dumps(feed_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_feed_duplicate_url(self, client, app_context):
        """Test adding a feed with a URL that already exists."""
        # Create existing feed
        existing_feed = Feed(name='Existing Feed', url='https://example.com/rss.xml')
        db.session.add(existing_feed)
        db.session.commit()
        
        # Try to add feed with same URL
        feed_data = {
            'name': 'New Feed',
            'url': 'https://example.com/rss.xml',
            'category': 'Technology'
        }
        
        response = client.post('/api/feeds',
                             data=json.dumps(feed_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data['error']
    
    def test_delete_feed(self, client, app_context):
        """Test deleting a feed."""
        # Create a test feed
        feed = Feed(name='Test Feed', url='https://example.com/rss.xml')
        db.session.add(feed)
        db.session.commit()
        
        response = client.delete(f'/api/feeds/{feed.id}')
        assert response.status_code == 200
        
        # Check that feed is marked as inactive
        db.session.refresh(feed)
        assert feed.is_active is False

class TestArticleAPI:
    """Test cases for article-related API endpoints."""
    
    def test_get_articles_empty(self, client):
        """Test getting articles when none exist."""
        response = client.get('/api/articles')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['articles'] == []
        assert data['total'] == 0
    
    def test_get_articles_with_data(self, client, app_context):
        """Test getting articles when they exist."""
        # Create a feed and article
        feed = Feed(name='Test Feed', url='https://example.com/rss.xml')
        db.session.add(feed)
        db.session.commit()
        
        article = Article(
            feed_id=feed.id,
            title='Test Article',
            link='https://example.com/article1'
        )
        db.session.add(article)
        db.session.commit()
        
        response = client.get('/api/articles')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['articles']) == 1
        assert data['articles'][0]['title'] == 'Test Article'
        assert data['total'] == 1
    
    def test_mark_article_as_read(self, client, app_context):
        """Test marking an article as read."""
        # Create a feed and article
        feed = Feed(name='Test Feed', url='https://example.com/rss.xml')
        db.session.add(feed)
        db.session.commit()
        
        article = Article(
            feed_id=feed.id,
            title='Test Article',
            link='https://example.com/article1'
        )
        db.session.add(article)
        db.session.commit()
        
        response = client.put(f'/api/articles/{article.id}/read')
        assert response.status_code == 200
        
        # Check that article is marked as read
        db.session.refresh(article)
        assert article.is_read is True
    
    def test_mark_article_as_unread(self, client, app_context):
        """Test marking an article as unread."""
        # Create a feed and article (already read)
        feed = Feed(name='Test Feed', url='https://example.com/rss.xml')
        db.session.add(feed)
        db.session.commit()
        
        article = Article(
            feed_id=feed.id,
            title='Test Article',
            link='https://example.com/article1',
            is_read=True
        )
        db.session.add(article)
        db.session.commit()
        
        response = client.put(f'/api/articles/{article.id}/unread')
        assert response.status_code == 200
        
        # Check that article is marked as unread
        db.session.refresh(article)
        assert article.is_read is False

class TestStatsAPI:
    """Test cases for stats API endpoint."""
    
    def test_get_stats_empty(self, client):
        """Test getting stats when no data exists."""
        response = client.get('/api/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_feeds'] == 0
        assert data['total_articles'] == 0
        assert data['unread_articles'] == 0
        assert data['read_articles'] == 0
    
    def test_get_stats_with_data(self, client, app_context):
        """Test getting stats when data exists."""
        # Create feeds and articles
        feed1 = Feed(name='Feed 1', url='https://example1.com/rss.xml')
        feed2 = Feed(name='Feed 2', url='https://example2.com/rss.xml')
        db.session.add_all([feed1, feed2])
        db.session.commit()
        
        # Create articles (2 read, 1 unread)
        article1 = Article(feed_id=feed1.id, title='Article 1', link='link1', is_read=True)
        article2 = Article(feed_id=feed1.id, title='Article 2', link='link2', is_read=True)
        article3 = Article(feed_id=feed2.id, title='Article 3', link='link3', is_read=False)
        db.session.add_all([article1, article2, article3])
        db.session.commit()
        
        response = client.get('/api/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_feeds'] == 2
        assert data['total_articles'] == 3
        assert data['unread_articles'] == 1
        assert data['read_articles'] == 2 