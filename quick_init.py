"""
Quick Database Initialization Script for Production
Run this once to populate your database with stocks, settings, and an event.

Usage:
1. Deploy to Vercel
2. Run: vercel env pull
3. Run: python3 quick_init.py

Or run via Django shell in production.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
django.setup()

from app1.models import Stock, SimulatorSettings, Event
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

def init_stocks():
    """Create all 63 stocks"""
    print("Creating stocks...")
    
    stocks_data = [
        # Technology (15 stocks)
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "price": 150.50},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "price": 2800.00},
        {"symbol": "MSFT", "name": "Microsoft Corp.", "sector": "Technology", "price": 380.25},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Technology", "price": 3350.00},
        {"symbol": "META", "name": "Meta Platforms Inc.", "sector": "Technology", "price": 325.75},
        {"symbol": "NVDA", "name": "NVIDIA Corp.", "sector": "Technology", "price": 485.60},
        {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Technology", "price": 725.50},
        {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Technology", "price": 445.80},
        {"symbol": "INTC", "name": "Intel Corp.", "sector": "Technology", "price": 55.30},
        {"symbol": "AMD", "name": "Advanced Micro Devices", "sector": "Technology", "price": 112.45},
        {"symbol": "ORCL", "name": "Oracle Corp.", "sector": "Technology", "price": 95.20},
        {"symbol": "CSCO", "name": "Cisco Systems", "sector": "Technology", "price": 54.15},
        {"symbol": "ADBE", "name": "Adobe Inc.", "sector": "Technology", "price": 535.80},
        {"symbol": "CRM", "name": "Salesforce Inc.", "sector": "Technology", "price": 215.65},
        {"symbol": "IBM", "name": "IBM Corp.", "sector": "Technology", "price": 145.30},
        
        # Finance (12 stocks)
        {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Finance", "price": 155.40},
        {"symbol": "BAC", "name": "Bank of America", "sector": "Finance", "price": 32.85},
        {"symbol": "WFC", "name": "Wells Fargo & Co.", "sector": "Finance", "price": 45.60},
        {"symbol": "GS", "name": "Goldman Sachs Group", "sector": "Finance", "price": 365.90},
        {"symbol": "MS", "name": "Morgan Stanley", "sector": "Finance", "price": 95.75},
        {"symbol": "C", "name": "Citigroup Inc.", "sector": "Finance", "price": 52.30},
        {"symbol": "AXP", "name": "American Express", "sector": "Finance", "price": 185.25},
        {"symbol": "BLK", "name": "BlackRock Inc.", "sector": "Finance", "price": 745.80},
        {"symbol": "SCHW", "name": "Charles Schwab Corp.", "sector": "Finance", "price": 72.45},
        {"symbol": "V", "name": "Visa Inc.", "sector": "Finance", "price": 235.60},
        {"symbol": "MA", "name": "Mastercard Inc.", "sector": "Finance", "price": 385.90},
        {"symbol": "PYPL", "name": "PayPal Holdings", "sector": "Finance", "price": 65.40},
        
        # Healthcare (10 stocks)
        {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "price": 165.30},
        {"symbol": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare", "price": 35.85},
        {"symbol": "UNH", "name": "UnitedHealth Group", "sector": "Healthcare", "price": 525.40},
        {"symbol": "ABBV", "name": "AbbVie Inc.", "sector": "Healthcare", "price": 155.70},
        {"symbol": "TMO", "name": "Thermo Fisher Scientific", "sector": "Healthcare", "price": 565.20},
        {"symbol": "ABT", "name": "Abbott Laboratories", "sector": "Healthcare", "price": 115.45},
        {"symbol": "MRK", "name": "Merck & Co.", "sector": "Healthcare", "price": 108.60},
        {"symbol": "LLY", "name": "Eli Lilly and Co.", "sector": "Healthcare", "price": 585.90},
        {"symbol": "BMY", "name": "Bristol-Myers Squibb", "sector": "Healthcare", "price": 55.25},
        {"symbol": "AMGN", "name": "Amgen Inc.", "sector": "Healthcare", "price": 275.80},
        
        # Energy (8 stocks)
        {"symbol": "XOM", "name": "Exxon Mobil Corp.", "sector": "Energy", "price": 115.40},
        {"symbol": "CVX", "name": "Chevron Corp.", "sector": "Energy", "price": 165.80},
        {"symbol": "COP", "name": "ConocoPhillips", "sector": "Energy", "price": 125.65},
        {"symbol": "SLB", "name": "Schlumberger Ltd.", "sector": "Energy", "price": 58.30},
        {"symbol": "EOG", "name": "EOG Resources", "sector": "Energy", "price": 135.50},
        {"symbol": "PXD", "name": "Pioneer Natural Resources", "sector": "Energy", "price": 245.20},
        {"symbol": "MPC", "name": "Marathon Petroleum", "sector": "Energy", "price": 165.75},
        {"symbol": "PSX", "name": "Phillips 66", "sector": "Energy", "price": 125.40},
        
        # Consumer (10 stocks)
        {"symbol": "WMT", "name": "Walmart Inc.", "sector": "Consumer", "price": 155.80},
        {"symbol": "HD", "name": "Home Depot Inc.", "sector": "Consumer", "price": 325.40},
        {"symbol": "MCD", "name": "McDonald's Corp.", "sector": "Consumer", "price": 285.65},
        {"symbol": "NKE", "name": "Nike Inc.", "sector": "Consumer", "price": 105.30},
        {"symbol": "SBUX", "name": "Starbucks Corp.", "sector": "Consumer", "price": 95.75},
        {"symbol": "TGT", "name": "Target Corp.", "sector": "Consumer", "price": 145.90},
        {"symbol": "LOW", "name": "Lowe's Companies", "sector": "Consumer", "price": 225.60},
        {"symbol": "COST", "name": "Costco Wholesale", "sector": "Consumer", "price": 565.80},
        {"symbol": "PG", "name": "Procter & Gamble", "sector": "Consumer", "price": 155.40},
        {"symbol": "KO", "name": "Coca-Cola Co.", "sector": "Consumer", "price": 62.30},
        
        # Industrial (5 stocks)
        {"symbol": "BA", "name": "Boeing Co.", "sector": "Industrial", "price": 185.40},
        {"symbol": "CAT", "name": "Caterpillar Inc.", "sector": "Industrial", "price": 285.70},
        {"symbol": "GE", "name": "General Electric", "sector": "Industrial", "price": 115.80},
        {"symbol": "MMM", "name": "3M Company", "sector": "Industrial", "price": 95.60},
        {"symbol": "HON", "name": "Honeywell International", "sector": "Industrial", "price": 205.30},
        
        # Telecom (3 stocks)
        {"symbol": "T", "name": "AT&T Inc.", "sector": "Telecom", "price": 18.45},
        {"symbol": "VZ", "name": "Verizon Communications", "sector": "Telecom", "price": 42.80},
        {"symbol": "TMUS", "name": "T-Mobile US", "sector": "Telecom", "price": 165.90},
    ]
    
    created_count = 0
    for stock_data in stocks_data:
        stock, created = Stock.objects.get_or_create(
            symbol=stock_data["symbol"],
            defaults={
                'name': stock_data["name"],
                'sector': stock_data["sector"],
                'current_price': Decimal(str(stock_data["price"])),
                'previous_close': Decimal(str(stock_data["price"])),
                'is_active': True
            }
        )
        if created:
            created_count += 1
            print(f"  ✓ Created {stock.symbol} - {stock.name}")
    
    print(f"\n✅ Created {created_count} new stocks (Total: {Stock.objects.count()})")

def init_settings():
    """Create simulator settings"""
    print("\nCreating simulator settings...")
    
    settings, created = SimulatorSettings.objects.get_or_create(
        id=1,
        defaults={
            'market_open': timezone.now().replace(hour=9, minute=30, second=0, microsecond=0),
            'market_close': timezone.now().replace(hour=16, minute=0, second=0, microsecond=0),
            'trading_fee': Decimal('0.00')
        }
    )
    
    if created:
        print("  ✓ Created simulator settings")
    else:
        print("  ℹ Simulator settings already exist")

def init_event():
    """Create a default event"""
    print("\nCreating default event...")
    
    # Check if any active events exist
    if Event.objects.filter(is_active=True).exists():
        print("  ℹ Active event already exists")
        return
    
    event, created = Event.objects.get_or_create(
        name="Stock Trading Competition 2025",
        defaults={
            'description': 'Welcome to the stock trading competition! Buy and sell stocks to maximize your portfolio value.',
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(days=30),
            'initial_capital': Decimal('100000.00'),
            'is_active': True,
            'registration_open': True,
            'status': 'in_progress'
        }
    )
    
    if created:
        print(f"  ✓ Created event: {event.name}")
        print(f"    - Initial Capital: ${event.initial_capital}")
        print(f"    - Duration: 30 days")
        print(f"    - Status: Active")
    else:
        print(f"  ℹ Event '{event.name}' already exists")

def main():
    print("=" * 60)
    print("QUICK DATABASE INITIALIZATION")
    print("=" * 60)
    
    try:
        init_settings()
        init_stocks()
        init_event()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"  - Stocks: {Stock.objects.count()}")
        print(f"  - Active Stocks: {Stock.objects.filter(is_active=True).count()}")
        print(f"  - Events: {Event.objects.count()}")
        print(f"  - Active Events: {Event.objects.filter(is_active=True).count()}")
        print("\n🎯 Next Steps:")
        print("  1. Go to /admin and login")
        print("  2. Check that stocks and event are created")
        print("  3. Teams can now register at /team/signup")
        print("  4. Teams can trade stocks at /team/stocks")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
