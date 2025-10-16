"""
Management command to update stock prices with random fluctuations
Run this periodically to simulate real-world stock market behavior

Usage:
    python manage.py update_stock_prices              # Update all stocks once
    python manage.py update_stock_prices --continuous  # Keep updating every 30 seconds
    python manage.py update_stock_prices --interval 10 # Update every 10 seconds
"""

from django.core.management.base import BaseCommand
from app1.models import Stock
import time
from datetime import datetime


class Command(BaseCommand):
    help = 'Update stock prices with random fluctuations to simulate market movement'

    def add_arguments(self, parser):
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Keep updating prices continuously',
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=30,
            help='Seconds between updates (default: 30)',
        )
        parser.add_argument(
            '--volatility',
            type=float,
            default=0.02,
            help='Price volatility as decimal (default: 0.02 = ±2%%)',
        )

    def handle(self, *args, **options):
        continuous = options['continuous']
        interval = options['interval']
        volatility = options['volatility']

        self.stdout.write(self.style.SUCCESS(f'🎯 Stock Price Updater Started'))
        self.stdout.write(f'   Volatility: ±{volatility*100}%')
        self.stdout.write(f'   Mode: {"Continuous" if continuous else "Single update"}')
        if continuous:
            self.stdout.write(f'   Interval: {interval} seconds')
        self.stdout.write('')

        try:
            if continuous:
                update_count = 0
                while True:
                    update_count += 1
                    self.update_prices(volatility, update_count)
                    time.sleep(interval)
            else:
                self.update_prices(volatility, 1)
                
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n\n⏹️  Stopped by user'))

    def update_prices(self, volatility, update_num):
        """Update all active stock prices"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.stdout.write(self.style.SUCCESS(f'\n📊 Update #{update_num} at {timestamp}'))
        
        stocks = Stock.objects.filter(is_active=True)
        
        if not stocks.exists():
            self.stdout.write(self.style.ERROR('   ❌ No active stocks found!'))
            return
        
        self.stdout.write(f'   Updating {stocks.count()} stocks...\n')
        
        # Track changes
        gainers = []
        losers = []
        
        for stock in stocks:
            old_price = stock.current_price
            new_price = stock.update_price_random(volatility)
            change = new_price - old_price
            change_pct = (change / old_price) * 100
            
            # Format change with color
            if change > 0:
                change_str = self.style.SUCCESS(f'+${change:.2f} (+{change_pct:.2f}%)')
                gainers.append((stock.symbol, change_pct))
            elif change < 0:
                change_str = self.style.ERROR(f'-${abs(change):.2f} ({change_pct:.2f}%)')
                losers.append((stock.symbol, change_pct))
            else:
                change_str = '±$0.00 (0.00%)'
            
            self.stdout.write(f'   {stock.symbol:6s} ${old_price:8.2f} → ${new_price:8.2f}  {change_str}')
        
        # Summary
        self.stdout.write('')
        self.stdout.write(f'   📈 Gainers: {len(gainers)}')
        if gainers:
            top_gainer = max(gainers, key=lambda x: x[1])
            self.stdout.write(self.style.SUCCESS(f'      Top: {top_gainer[0]} +{top_gainer[1]:.2f}%'))
        
        self.stdout.write(f'   📉 Losers: {len(losers)}')
        if losers:
            top_loser = min(losers, key=lambda x: x[1])
            self.stdout.write(self.style.ERROR(f'      Top: {top_loser[0]} {top_loser[1]:.2f}%'))
        
        self.stdout.write(f'   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
