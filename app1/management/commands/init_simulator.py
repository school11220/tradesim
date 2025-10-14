from django.core.management.base import BaseCommand
from app1.models import Stock, SimulatorSettings


class Command(BaseCommand):
    help = 'Initialize stock market simulator with default stocks and settings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing stock market simulator...')
        
        # Create default stocks
        default_stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'current_price': 178.50, 'previous_close': 175.20},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'current_price': 380.75, 'previous_close': 378.90},
            {'symbol': 'GOOG', 'name': 'Alphabet Inc.', 'current_price': 139.25, 'previous_close': 138.00},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'current_price': 325.40, 'previous_close': 322.10},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'current_price': 143.90, 'previous_close': 142.50},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'current_price': 242.30, 'previous_close': 238.75},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'current_price': 495.20, 'previous_close': 485.30},
            {'symbol': 'NFLX', 'name': 'Netflix Inc.', 'current_price': 445.60, 'previous_close': 442.00},
            {'symbol': 'SONY', 'name': 'Sony Group Corporation', 'current_price': 92.15, 'previous_close': 91.80},
            {'symbol': 'DIS', 'name': 'The Walt Disney Company', 'current_price': 91.25, 'previous_close': 90.50},
        ]
        
        created_count = 0
        updated_count = 0
        
        for stock_data in default_stocks:
            stock, created = Stock.objects.update_or_create(
                symbol=stock_data['symbol'],
                defaults={
                    'name': stock_data['name'],
                    'current_price': stock_data['current_price'],
                    'previous_close': stock_data['previous_close'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created stock: {stock.symbol} - {stock.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'  ↻ Updated stock: {stock.symbol} - {stock.name}'))
        
        # Create default simulator settings
        default_balance = SimulatorSettings.set_default_balance(10000.0)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Set default user balance: ${default_balance.setting_value}'))
        
        # Trading fee setting
        trading_fee, created = SimulatorSettings.objects.update_or_create(
            setting_key='trading_fee_percent',
            defaults={
                'setting_value': '0.0',
                'description': 'Trading fee percentage (0.0 = no fee)'
            }
        )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Set trading fee: {trading_fee.setting_value}%'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Successfully initialized simulator!'))
        self.stdout.write(self.style.SUCCESS(f'  - Created {created_count} new stocks'))
        self.stdout.write(self.style.SUCCESS(f'  - Updated {updated_count} existing stocks'))
        self.stdout.write('')
        self.stdout.write(self.style.NOTICE('Next steps:'))
        self.stdout.write('  1. Create a superuser: python manage.py createsuperuser')
        self.stdout.write('  2. Go to /admin to control stock prices and user balances')
        self.stdout.write('  3. Users can start trading with the default balance')
