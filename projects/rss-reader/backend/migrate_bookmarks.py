#!/usr/bin/env python3
"""
Migration script to add is_bookmarked column to Article table
Run this script to update existing databases with the new bookmark functionality
"""

import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv

# Add the current directory to the path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

load_dotenv()

def migrate_bookmarks():
    """Add is_bookmarked column to Article table if it doesn't exist"""
    with app.app_context():
        try:
            # Check if the column already exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'article' 
                AND column_name = 'is_bookmarked'
            """))
            
            if result.fetchone():
                print("✅ is_bookmarked column already exists")
                return
            
            # Add the column
            db.session.execute(text("""
                ALTER TABLE article 
                ADD COLUMN is_bookmarked BOOLEAN DEFAULT FALSE
            """))
            
            db.session.commit()
            print("✅ Successfully added is_bookmarked column to Article table")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    print("🔄 Starting bookmark migration...")
    migrate_bookmarks()
    print("✅ Migration completed successfully!") 