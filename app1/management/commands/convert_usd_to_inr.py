"""
Convert all US stock prices from USD to INR
Run with: python manage.py convert_usd_to_inr
"""
from django.core.management.base import BaseCommand
from app1.models import Stock
import random


class Command(BaseCommand):
    help = 'Convert US stock prices from USD to INR (1 USD = ₹83 approx)'

    def handle(self, *args, **options):
        # Approximate USD to INR exchange rate
        USD_TO_INR = 89.0
        
        # Indian stock symbols (don't convert these)
        indian_symbols = {
            'TCS', 'INFY', 'WIPRO', 'HCLTECH', 'TECHM',
            'HDFCBANK', 'ICICIBANK', 'SBIN', 'AXISBANK', 'KOTAKBANK',
            'TATAMOTORS', 'MARUTI', 'M&M', 'BAJAJ-AUTO', 'HEROMOTOCO',
            'HINDUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'DABUR',
            'RELIANCE', 'ONGC', 'BPCL', 'IOC', 'COALINDIA',
            'SUNPHARMA', 'DRREDDY', 'CIPLA', 'AUROPHARMA', 'DIVISLAB',
            'TATASTEEL', 'HINDALCO', 'VEDL', 'JSWSTEEL', 'NMDC',
            'BHARTIARTL', 'IDEA', 'LT', 'ADANIPORTS', 'ULTRACEMCO',
            'DMART', 'TRENT'
        }
        
        self.stdout.write(self.style.WARNING('Converting US stock prices from USD to INR...'))
        self.stdout.write(self.style.WARNING(f'Exchange rate: 1 USD = ₹{USD_TO_INR}'))
        
        converted = 0
        skipped = 0
        
        # Get all stocks
        all_stocks = Stock.objects.all()
        
        for stock in all_stocks:
            # Skip Indian stocks
            if stock.symbol in indian_symbols:
                skipped += 1
                continue
            
            # Convert USD prices to INR
            old_current = float(stock.current_price)
            old_previous = float(stock.previous_close)
            
            # Check if already converted (prices > 1000 likely already in INR)
            if old_current > 1000:
                self.stdout.write(self.style.WARNING(f'⏭️  Skipped (already converted): {stock.symbol} @ ₹{old_current}'))
                skipped += 1
                continue
            
            # Convert to INR
            new_current = old_current * USD_TO_INR
            new_previous = old_previous * USD_TO_INR
            
            # Add small random variation to previous_close (±0.5% to ±2%)
            variation = random.uniform(0.995, 1.02)
            new_previous = new_previous * variation
            
            # Update stock
            stock.current_price = round(new_current, 2)
            stock.previous_close = round(new_previous, 2)
            stock.save()
            
            converted += 1
            
            # Calculate change
            change = new_current - new_previous
            change_pct = (change / new_previous * 100) if new_previous > 0 else 0
            
            self.stdout.write(self.style.SUCCESS(
                f'✅ Converted: {stock.symbol} | '
                f'USD ${old_current:.2f} → INR ₹{new_current:.2f} | '
                f'Change: {"+" if change >= 0 else ""}{change:.2f} ({change_pct:+.2f}%)'
            ))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Conversion complete!'))
        self.stdout.write(self.style.SUCCESS(f'Converted: {converted} stocks'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped} stocks (Indian or already converted)'))
