#!/usr/bin/env python
"""Create a test team with known credentials"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
django.setup()

from app1.models import Team, Event
from django.utils import timezone

# Get the active event
event = Event.objects.filter(is_active=True).first()

if not event:
    print("❌ No active event found!")
    exit(1)

# Create test team
team, created = Team.objects.get_or_create(
    team_code="TEST-2024",
    defaults={
        'team_name': "Test Team",
        'leader_name': "Test Leader",
        'leader_email': "test@test.com",
        'password': "password123",  # Simple password for testing
        'event': event,
        'balance': event.initial_capital,
        'portfolio': {},
        'trade_history': [],
        'members': ['Test Leader', 'Member 2', 'Member 3']
    }
)

if created:
    print("✅ Test team created successfully!")
else:
    print("ℹ️  Test team already exists, updated password")
    team.password = "password123"
    team.save()

print("\n" + "=" * 60)
print("TEST TEAM CREDENTIALS")
print("=" * 60)
print(f"Team Code: TEST-2024")
print(f"Password: password123")
print(f"Team Name: {team.team_name}")
print(f"Balance: ${team.balance}")
print("=" * 60)
print("\n📍 Login at: http://127.0.0.1:8000/team/login")
print("📈 View stocks at: http://127.0.0.1:8000/team/stocks")
print("💼 View portfolio at: http://127.0.0.1:8000/team/portfolio")
print("=" * 60)
