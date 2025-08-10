#!/usr/bin/env python3
"""
Database Cleanup Script for RSS Reader
This script helps reduce Supabase storage usage by cleaning old data.
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

def get_database_connection():
    """Create database connection"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        sys.exit(1)
    
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return engine, Session()

def cleanup_old_articles(session, days_to_keep=30):
    """Remove articles older than specified days"""
    cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
    
    # Count articles before deletion
    count_before = session.execute(text("SELECT COUNT(*) FROM article")).scalar()
    
    # Delete old articles that are not bookmarked
    result = session.execute(text("""
        DELETE FROM article 
        WHERE created_at < :cutoff_date 
        AND is_bookmarked = false
    """), {'cutoff_date': cutoff_date})
    
    deleted_count = result.rowcount
    session.commit()
    
    # Count articles after deletion
    count_after = session.execute(text("SELECT COUNT(*) FROM article")).scalar()
    
    print(f"🗑️  Deleted {deleted_count} old articles (older than {days_to_keep} days)")
    print(f"📊 Articles before: {count_before}, after: {count_after}")
    
    return deleted_count

def cleanup_read_articles(session, days_to_keep=7):
    """Remove read articles older than specified days"""
    cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
    
    # Count read articles before deletion
    count_before = session.execute(text("SELECT COUNT(*) FROM article WHERE is_read = true")).scalar()
    
    # Delete old read articles that are not bookmarked
    result = session.execute(text("""
        DELETE FROM article 
        WHERE is_read = true 
        AND created_at < :cutoff_date 
        AND is_bookmarked = false
    """), {'cutoff_date': cutoff_date})
    
    deleted_count = result.rowcount
    session.commit()
    
    # Count read articles after deletion
    count_after = session.execute(text("SELECT COUNT(*) FROM article WHERE is_read = true")).scalar()
    
    print(f"🗑️  Deleted {deleted_count} old read articles (older than {days_to_keep} days)")
    print(f"📊 Read articles before: {count_before}, after: {count_after}")
    
    return deleted_count

def get_database_stats(session):
    """Get database statistics"""
    stats = {}
    
    # Total articles
    stats['total_articles'] = session.execute(text("SELECT COUNT(*) FROM article")).scalar()
    
    # Read articles
    stats['read_articles'] = session.execute(text("SELECT COUNT(*) FROM article WHERE is_read = true")).scalar()
    
    # Bookmarked articles
    stats['bookmarked_articles'] = session.execute(text("SELECT COUNT(*) FROM article WHERE is_bookmarked = true")).scalar()
    
    # Unread articles
    stats['unread_articles'] = session.execute(text("SELECT COUNT(*) FROM article WHERE is_read = false")).scalar()
    
    # Old articles (older than 30 days)
    old_date = datetime.utcnow() - timedelta(days=30)
    stats['old_articles'] = session.execute(text("SELECT COUNT(*) FROM article WHERE created_at < :old_date"), 
                                          {'old_date': old_date}).scalar()
    
    # Total feeds
    stats['total_feeds'] = session.execute(text("SELECT COUNT(*) FROM feed")).scalar()
    
    return stats

def vacuum_database(engine):
    """Vacuum the database to reclaim storage"""
    try:
        with engine.connect() as conn:
            conn.execute(text("VACUUM"))
            conn.commit()
        print("🧹 Database vacuumed successfully")
    except Exception as e:
        print(f"⚠️  Could not vacuum database: {e}")

def main():
    """Main cleanup function"""
    print("🧹 RSS Reader Database Cleanup")
    print("=" * 40)
    
    # Get database connection
    engine, session = get_database_connection()
    
    try:
        # Show initial stats
        print("\n📊 Initial Database Statistics:")
        initial_stats = get_database_stats(session)
        for key, value in initial_stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Cleanup operations
        print("\n🔄 Starting cleanup operations...")
        
        # Clean old articles (older than 30 days, not bookmarked)
        deleted_old = cleanup_old_articles(session, days_to_keep=30)
        
        # Clean old read articles (older than 7 days, not bookmarked)
        deleted_read = cleanup_read_articles(session, days_to_keep=7)
        
        # Show final stats
        print("\n📊 Final Database Statistics:")
        final_stats = get_database_stats(session)
        for key, value in final_stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Calculate savings
        total_deleted = deleted_old + deleted_read
        print(f"\n💾 Total articles deleted: {total_deleted}")
        
        # Vacuum database
        print("\n🧹 Reclaiming storage space...")
        vacuum_database(engine)
        
        print("\n✅ Database cleanup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        session.rollback()
        sys.exit(1)
    finally:
        session.close()
        engine.dispose()

if __name__ == "__main__":
    main() 