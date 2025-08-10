import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/rss_reader')
    
    # Feed refresh settings (30 minutes default for egress optimization)
    FEED_REFRESH_INTERVAL_MINUTES = int(os.getenv('FEED_REFRESH_INTERVAL_MINUTES', '30'))
    
    # Memory optimization settings
    BATCH_SIZE_FOR_FEED_PROCESSING = int(os.getenv('BATCH_SIZE_FOR_FEED_PROCESSING', '10'))
    COMMIT_EVERY_N_ARTICLES = int(os.getenv('COMMIT_EVERY_N_ARTICLES', '10'))
    
    # API settings
    FEEDSEARCH_TIMEOUT = int(os.getenv('FEEDSEARCH_TIMEOUT', '15'))
    
    # Flask settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true' 