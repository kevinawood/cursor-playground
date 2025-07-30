import pytest
import tempfile
import os
from app import app, db
from datetime import datetime

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    
    # Use environment DATABASE_URL if available (for CI/CD), otherwise use SQLite
    if os.getenv('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    else:
        # Create a temporary database for local testing
        db_fd, db_path = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
    
    # Clean up SQLite file if we created one
    if not os.getenv('DATABASE_URL'):
        os.close(db_fd)
        os.unlink(db_path)

@pytest.fixture
def app_context():
    """Create an application context for testing."""
    app.config['TESTING'] = True
    
    # Use environment DATABASE_URL if available (for CI/CD), otherwise use SQLite
    if os.getenv('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    else:
        # Create a temporary database for local testing
        db_fd, db_path = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app
    
    # Clean up SQLite file if we created one
    if not os.getenv('DATABASE_URL'):
        os.close(db_fd)
        os.unlink(db_path)

@pytest.fixture
def sample_feed_data():
    """Sample feed data for testing."""
    return {
        'name': 'Test Feed',
        'url': 'https://example.com/rss.xml',
        'category': 'Technology'
    }

@pytest.fixture
def sample_article_data():
    """Sample article data for testing."""
    return {
        'title': 'Test Article',
        'link': 'https://example.com/article1',
        'description': 'This is a test article',
        'published_date': datetime.utcnow(),
        'author': 'Test Author'
    } 