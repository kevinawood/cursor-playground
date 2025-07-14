import pytest
from datetime import datetime
from app import db, Feed, Article

class TestFeedModel:
    """Test cases for the Feed model."""
    
    def test_create_feed(self, app_context):
        """Test creating a new feed."""
        feed = Feed(
            name='Test Feed',
            url='https://example.com/rss.xml',
            category='Technology'
        )
        db.session.add(feed)
        db.session.commit()
        
        assert feed.id is not None
        assert feed.name == 'Test Feed'
        assert feed.url == 'https://example.com/rss.xml'
        assert feed.category == 'Technology'
        assert feed.is_active is True
        assert feed.created_at is not None
    
    def test_feed_name_truncation(self, app_context):
        """Test that long feed names are truncated."""
        long_name = 'A' * 150  # 150 characters
        feed = Feed(
            name=long_name,
            url='https://example.com/rss.xml',
            category='Technology'
        )
        db.session.add(feed)
        db.session.commit()
        
        # Should be truncated to 100 characters
        assert len(feed.name) <= 100
    
    def test_feed_url_uniqueness(self, app_context):
        """Test that feed URLs must be unique."""
        url = 'https://example.com/rss.xml'
        
        # Create first feed
        feed1 = Feed(name='Feed 1', url=url, category='Technology')
        db.session.add(feed1)
        db.session.commit()
        
        # Try to create second feed with same URL
        feed2 = Feed(name='Feed 2', url=url, category='Technology')
        db.session.add(feed2)
        
        with pytest.raises(Exception):  # Should raise integrity error
            db.session.commit()

class TestArticleModel:
    """Test cases for the Article model."""
    
    def test_create_article(self, app_context):
        """Test creating a new article."""
        # Create a feed first
        feed = Feed(name='Test Feed', url='https://example.com/rss.xml')
        db.session.add(feed)
        db.session.commit()
        
        article = Article(
            feed_id=feed.id,
            title='Test Article',
            link='https://example.com/article1',
            description='This is a test article',
            author='Test Author'
        )
        db.session.add(article)
        db.session.commit()
        
        assert article.id is not None
        assert article.title == 'Test Article'
        assert article.link == 'https://example.com/article1'
        assert article.feed_id == feed.id
        assert article.is_read is False
        assert article.created_at is not None
    
    def test_article_title_truncation(self, app_context):
        """Test that long article titles are truncated."""
        # Create a feed first
        feed = Feed(name='Test Feed', url='https://example.com/rss.xml')
        db.session.add(feed)
        db.session.commit()
        
        long_title = 'A' * 600  # 600 characters
        article = Article(
            feed_id=feed.id,
            title=long_title,
            link='https://example.com/article1'
        )
        db.session.add(article)
        db.session.commit()
        
        # Should be truncated to 500 characters
        assert len(article.title) <= 500
    
    def test_article_feed_relationship(self, app_context):
        """Test the relationship between articles and feeds."""
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
        
        # Test relationship
        assert article.feed == feed
        assert article in feed.articles 