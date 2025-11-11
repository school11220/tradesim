#!/usr/bin/env python3
"""Test the news page with team authentication"""
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_news_page():
    """Test news page with team login"""
    session = requests.Session()
    
    # First, check if we have any teams
    print("🔍 Checking for test teams...")
    try:
        import os
        import django
        
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
        django.setup()
        
        from app1.models import Team
        teams = Team.objects.all()
        
        if not teams.exists():
            print("❌ No teams found! Creating test team...")
            from create_test_team import create_test_team
            create_test_team()
            teams = Team.objects.all()
        
        team = teams.first()
        print(f"✅ Using team: {team.team_name} (Code: {team.team_code})")
        
        # Try to login
        print(f"\n🔐 Logging in as team: {team.team_code}...")
        login_response = session.post(
            f"{BASE_URL}/team/login/",
            data={
                'team_code': team.team_code,
                'password': 'test123'  # Default password from create_test_team
            },
            allow_redirects=False
        )
        
        print(f"Login Status: {login_response.status_code}")
        if login_response.status_code == 302:
            print(f"Redirected to: {login_response.headers.get('Location', 'Unknown')}")
        
        # Now try accessing news page
        print(f"\n📰 Accessing news page...")
        news_response = session.get(f"{BASE_URL}/team/news/", allow_redirects=False)
        print(f"News Page Status: {news_response.status_code}")
        
        if news_response.status_code == 200:
            print("✅ News page loaded successfully!")
            if 'Market News' in news_response.text:
                print("✅ Page contains expected content")
            if 'No News Available' in news_response.text:
                print("ℹ️  No news items found (this is normal if none created)")
            return True
        elif news_response.status_code == 302:
            print(f"❌ Still redirecting to: {news_response.headers.get('Location', 'Unknown')}")
            print("\n🔍 Checking server logs for errors...")
            return False
        else:
            print(f"❌ Unexpected status code: {news_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_news_page()
    sys.exit(0 if success else 1)
