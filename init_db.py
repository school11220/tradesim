"""
Quick database initialization script
Run this to populate the database with initial data
"""

from app1.models import Stock, SimulatorSettings, Event
from django.utils import timezone
from datetime import timedelta

def init_database():
    """Initialize database with stocks and settings"""
    
    print("🚀 Initializing database...")
    
    # 1. Initialize stocks if they don't exist
    stock_count = Stock.objects.count()
    if stock_count == 0:
        print("📊 Creating 63 stocks...")
        
        stocks_data = [
            # Technology
            ("AAPL", "Apple Inc."), ("MSFT", "Microsoft Corporation"), 
            ("GOOG", "Alphabet Inc."), ("META", "Meta Platforms Inc."),
            ("AMZN", "Amazon.com Inc."), ("TSLA", "Tesla Inc."),
            ("NVDA", "NVIDIA Corporation"), ("ORCL", "Oracle Corporation"),
            ("INTC", "Intel Corporation"), ("AMD", "Advanced Micro Devices"),
            ("CRM", "Salesforce Inc."), ("ADBE", "Adobe Inc."),
            ("CSCO", "Cisco Systems"), ("IBM", "IBM Corporation"),
            ("NFLX", "Netflix Inc."),
            
            # Finance
            ("JPM", "JPMorgan Chase"), ("BAC", "Bank of America"),
            ("WFC", "Wells Fargo"), ("GS", "Goldman Sachs"),
            ("MS", "Morgan Stanley"), ("V", "Visa Inc."),
            ("MA", "Mastercard Inc."), ("AXP", "American Express"),
            ("BLK", "BlackRock Inc."), ("SCHW", "Charles Schwab"),
            
            # Healthcare
            ("JNJ", "Johnson & Johnson"), ("PFE", "Pfizer Inc."),
            ("UNH", "UnitedHealth Group"), ("ABBV", "AbbVie Inc."),
            ("TMO", "Thermo Fisher Scientific"), ("MRK", "Merck & Co."),
            ("ABT", "Abbott Laboratories"), ("BMY", "Bristol-Myers Squibb"),
            ("LLY", "Eli Lilly and Company"), ("AMGN", "Amgen Inc."),
            
            # Energy
            ("XOM", "Exxon Mobil"), ("CVX", "Chevron Corporation"),
            ("COP", "ConocoPhillips"), ("SLB", "Schlumberger"),
            ("EOG", "EOG Resources"), ("MPC", "Marathon Petroleum"),
            ("PSX", "Phillips 66"),
            
            # Consumer Goods & Retail
            ("WMT", "Walmart Inc."), ("HD", "The Home Depot"),
            ("MCD", "McDonald's Corporation"), ("NKE", "Nike Inc."),
            ("SBUX", "Starbucks Corporation"), ("TGT", "Target Corporation"),
            ("LOW", "Lowe's Companies"), ("TJX", "TJX Companies"),
            ("DG", "Dollar General"), ("COST", "Costco Wholesale"),
            
            # Industrial
            ("BA", "Boeing Company"), ("CAT", "Caterpillar Inc."),
            ("GE", "General Electric"), ("UPS", "United Parcel Service"),
            ("HON", "Honeywell International"),
            
            # Telecommunications
            ("VZ", "Verizon Communications"), ("T", "AT&T Inc."),
            ("TMUS", "T-Mobile US"),
            
            # Entertainment & Media
            ("DIS", "The Walt Disney Company"), ("SONY", "Sony Group Corporation"),
            ("CMCSA", "Comcast Corporation"),
        ]
        
        for symbol, name in stocks_data:
            Stock.objects.create(
                symbol=symbol,
                name=name,
                current_price=100.0,
                previous_close=100.0,
                is_active=True
            )
        
        print(f"✅ Created {len(stocks_data)} stocks")
    else:
        print(f"✅ {stock_count} stocks already exist")
    
    # 2. Create default simulator settings
    setting_count = SimulatorSettings.objects.count()
    if setting_count == 0:
        print("⚙️  Creating simulator settings...")
        SimulatorSettings.objects.create(
            setting_key='default_user_balance',
            setting_value='10000.0',
            description='Default starting balance for new user accounts'
        )
        print("✅ Simulator settings created")
    else:
        print(f"✅ {setting_count} settings already exist")
    
    # 3. Create a default event for testing
    event_count = Event.objects.count()
    if event_count == 0:
        print("🎯 Creating default event...")
        Event.objects.create(
            name="Default Trading Competition",
            description="Default event for testing the trading platform",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(days=30),
            initial_capital=100000.00,
            is_active=False,
            registration_open=True,
            allow_short_selling=False,
            trading_fee_percentage=0.0
        )
        print("✅ Default event created")
    else:
        print(f"✅ {event_count} events already exist")
    
    print("\n✅ Database initialization complete!")
    print(f"   - {Stock.objects.count()} stocks")
    print(f"   - {Event.objects.count()} events")
    print(f"   - {SimulatorSettings.objects.count()} settings")
    print("\n🎉 Your app is ready to use!")

if __name__ == '__main__':
    init_database()
