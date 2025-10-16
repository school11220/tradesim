"""
Django management command to initialize the database with stocks and event.
Usage: python manage.py init_trading_platform
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from app1.models import Stock, SimulatorSettings, Event
from decimal import Decimal


class Command(BaseCommand):
    help = 'Initialize the trading platform with stocks, settings, and an active event'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing stocks and recreate them',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('🚀 INITIALIZING TRADING PLATFORM'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        if options['reset']:
            self.stdout.write(self.style.WARNING('\n⚠️  Resetting existing data...'))
            Stock.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Cleared existing stocks'))
        
        # Create simulator settings
        self.create_settings()
        
        # Create stocks
        self.create_stocks()
        
        # Create event
        self.create_event()
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ INITIALIZATION COMPLETE!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.display_summary()

    def create_settings(self):
        """Create simulator settings"""
        self.stdout.write('\n📋 Creating simulator settings...')
        
        # Create default user balance setting
        balance_setting, created = SimulatorSettings.objects.update_or_create(
            setting_key='default_user_balance',
            defaults={
                'setting_value': '100000.00',
                'description': 'Default starting balance for new user accounts'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Created default balance setting'))
        else:
            self.stdout.write(self.style.WARNING('  ℹ Default balance setting already exists'))

    def create_stocks(self):
        """Create all 63 stocks"""
        self.stdout.write('\n📈 Creating stocks...')
        
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
        updated_count = 0
        
        for stock_data in stocks_data:
            stock, created = Stock.objects.update_or_create(
                symbol=stock_data["symbol"],
                defaults={
                    'name': stock_data["name"],
                    'sector': stock_data["sector"],
                    'current_price': stock_data["price"],
                    'previous_close': stock_data["price"],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created {stock.symbol} - {stock.name}')
            else:
                updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n  ✓ Created {created_count} new stocks'))
        if updated_count > 0:
            self.stdout.write(self.style.WARNING(f'  ℹ Updated {updated_count} existing stocks'))

    def create_event(self):
        """Create a default active event"""
        self.stdout.write('\n🏆 Creating event...')
        
        # Check if any active events exist
        if Event.objects.filter(is_active=True).exists():
            self.stdout.write(self.style.WARNING('  ℹ Active event already exists'))
            return
        
        event, created = Event.objects.get_or_create(
            name="Stock Trading Competition 2025",
            defaults={
                'description': 'Welcome to the stock trading competition! Buy and sell stocks to maximize your portfolio value.',
                'start_time': timezone.now(),
                'end_time': timezone.now() + timedelta(days=30),
                'initial_capital': 100000.00,
                'is_active': True,
                'registration_open': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created event: {event.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'  ℹ Event "{event.name}" already exists'))

    def display_summary(self):
        """Display a summary of the initialized data"""
        self.stdout.write('\n📊 Summary:')
        self.stdout.write(f'  • Total Stocks: {Stock.objects.count()}')
        self.stdout.write(f'  • Active Stocks: {Stock.objects.filter(is_active=True).count()}')
        self.stdout.write(f'  • Total Events: {Event.objects.count()}')
        self.stdout.write(f'  • Active Events: {Event.objects.filter(is_active=True).count()}')
        
        self.stdout.write('\n🎯 Next Steps:')
        self.stdout.write('  1. Go to /admin and verify the data')
        self.stdout.write('  2. Teams can register at /team/signup')
        self.stdout.write('  3. Teams can trade stocks at /team/stocks')
        self.stdout.write('\n')
