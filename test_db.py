#!/usr/bin/env python
"""Quick database diagnostic script"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
django.setup()

from app1.models import Stock, Event, Team, SimulatorSettings

print("=" * 60)
print("DATABASE DIAGNOSTIC")
print("=" * 60)

print(f"\n📈 STOCKS:")
stocks = Stock.objects.all()
print(f"  Total: {stocks.count()}")
print(f"  Active: {Stock.objects.filter(is_active=True).count()}")
if stocks.exists():
    print(f"\n  First 5 stocks:")
    for stock in stocks[:5]:
        print(f"    - {stock.symbol}: ${stock.current_price} ({stock.name})")

print(f"\n🏆 EVENTS:")
events = Event.objects.all()
print(f"  Total: {events.count()}")
active_events = Event.objects.filter(is_active=True)
print(f"  Active: {active_events.count()}")
if active_events.exists():
    event = active_events.first()
    print(f"    - {event.name}")
    print(f"    - Start: {event.start_time}")
    print(f"    - End: {event.end_time}")
    print(f"    - Initial Capital: ${event.initial_capital}")
    print(f"    - Registration Open: {event.registration_open}")

print(f"\n👥 TEAMS:")
teams = Team.objects.all()
print(f"  Total: {teams.count()}")
if teams.exists():
    print(f"\n  All teams:")
    for team in teams:
        print(f"    - {team.team_name} ({team.team_code})")
        print(f"      Balance: ${team.balance}")
        print(f"      Event: {team.event.name if team.event else 'None'}")
        print(f"      Portfolio: {team.portfolio}")

print(f"\n⚙️  SETTINGS:")
settings = SimulatorSettings.objects.all()
print(f"  Total: {settings.count()}")
for setting in settings:
    print(f"    - {setting.key}: {setting.value}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
