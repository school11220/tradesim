#!/usr/bin/env python
"""
Emergency script to create MarketNews table on production
Run this if migrations fail
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
django.setup()

from django.db import connection

def create_marketnews_table():
    """Create the MarketNews table manually if it doesn't exist"""
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'app1_marketnews'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("✅ Table app1_marketnews already exists")
            return True
        
        print("📊 Creating app1_marketnews table...")
        
        # Create the table
        cursor.execute("""
            CREATE TABLE app1_marketnews (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                impact_direction VARCHAR(10) NOT NULL DEFAULT 'neutral',
                severity VARCHAR(10) NOT NULL DEFAULT 'medium',
                affected_sectors JSONB DEFAULT '[]',
                affected_stocks JSONB DEFAULT '[]',
                trading_hint TEXT NOT NULL DEFAULT '',
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                published_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                expires_at TIMESTAMP WITH TIME ZONE NULL
            );
        """)
        
        # Create index
        cursor.execute("""
            CREATE INDEX idx_marketnews_published 
            ON app1_marketnews(published_at DESC);
        """)
        
        cursor.execute("""
            CREATE INDEX idx_marketnews_active 
            ON app1_marketnews(is_active);
        """)
        
        print("✅ Table created successfully!")
        return True

if __name__ == '__main__':
    try:
        create_marketnews_table()
        print("✅ MarketNews table is ready!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
