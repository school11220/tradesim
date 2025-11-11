"""
Test price update system for all stocks
Run with: python manage.py test_price_updates
"""
from django.core.management.base import BaseCommand
from app1.models import Stock


class Command(BaseCommand):
    help = 'Test price updates for all active stocks'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Testing price update system...'))
        self.stdout.write('')
        
        # Get all active stocks
        stocks = Stock.objects.filter(is_active=True).order_by('symbol')
        
        if not stocks.exists():
            self.stdout.write(self.style.ERROR('❌ No active stocks found!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {stocks.count()} active stocks'))
        self.stdout.write('')
        
        updated_count = 0
        error_count = 0
        
        for stock in stocks:
            try:
                old_price = float(stock.current_price)
                old_previous = float(stock.previous_close)
                
                # Calculate current change
                old_change = old_price - old_previous
                old_change_pct = (old_change / old_previous * 100) if old_previous > 0 else 0
                
                # Update price using the model method
                new_price = stock.update_price_random(volatility=0.02)
                
                # Calculate new change
                new_change = float(new_price) - old_price
                new_change_pct = (new_change / old_price * 100) if old_price > 0 else 0
                
                updated_count += 1
                
                # Show before and after
                self.stdout.write(self.style.SUCCESS(
                    f'✅ {stock.symbol:12s} | '
                    f'Old: ₹{old_price:8.2f} ({"+" if old_change >= 0 else ""}{old_change_pct:+6.2f}%) | '
                    f'New: ₹{float(new_price):8.2f} ({"+" if new_change >= 0 else ""}{new_change_pct:+6.2f}%)'
                ))
                
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'❌ {stock.symbol}: {str(e)}'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Test complete!'))
        self.stdout.write(self.style.SUCCESS(f'Successfully updated: {updated_count} stocks'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Errors: {error_count} stocks'))
