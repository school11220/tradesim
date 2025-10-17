"""
Management command to update stock prices using realistic simulation
"""
from django.core.management.base import BaseCommand
from app1.models import Stock
from datetime import datetime
from decimal import Decimal
import sys
import random


class Command(BaseCommand):
    help = 'Update stock prices using realistic market simulation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Run continuously with interval',
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Interval in seconds between updates (default: 60)',
        )
        parser.add_argument(
            '--symbols',
            nargs='+',
            help='Specific stock symbols to update (default: all active)',
        )

    def handle(self, *args, **options):
        continuous = options['continuous']
        interval = options['interval']
        specific_symbols = options.get('symbols')
        
        if continuous:
            import time
            self.stdout.write(self.style.SUCCESS(f'🔄 Starting continuous simulation updates (every {interval}s)'))
            self.stdout.write(self.style.WARNING('Press Ctrl+C to stop\n'))
            update_count = 0
            
            try:
                while True:
                    update_count += 1
                    self.stdout.write(self.style.WARNING(f'\n📊 Update #{update_count} at {datetime.now().strftime("%H:%M:%S")}'))
                    self.update_prices(specific_symbols)
                    self.stdout.write(self.style.SUCCESS(f'⏱️  Next update in {interval} seconds...\n'))
                    time.sleep(interval)
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS('\n\n✅ Stopped continuous updates'))
                sys.exit(0)
        else:
            self.update_prices(specific_symbols)

    def update_prices(self, specific_symbols=None):
        """Update stock prices using realistic simulation"""
        
        # Get stocks to update
        if specific_symbols:
            stocks = Stock.objects.filter(symbol__in=specific_symbols, is_active=True)
        else:
            stocks = Stock.objects.filter(is_active=True)
        
        if not stocks.exists():
            self.stdout.write(self.style.WARNING('⚠️  No active stocks found'))
            return
        
        # Determine market sentiment for this update cycle
        market_sentiments = ['neutral', 'bullish', 'bearish']
        sentiment_weights = [0.60, 0.20, 0.20]  # 60% neutral, 20% bullish, 20% bearish
        market_sentiment = random.choices(market_sentiments, weights=sentiment_weights)[0]
        
        # Market drift based on sentiment
        if market_sentiment == 'bullish':
            market_drift = random.uniform(0.1, 0.5)  # 0.1-0.5% upward bias
        elif market_sentiment == 'bearish':
            market_drift = random.uniform(-0.5, -0.1)  # 0.1-0.5% downward bias
        else:
            market_drift = random.uniform(-0.1, 0.1)  # Neutral
        
        # Group stocks by sector for correlation
        sectors = {}
        for stock in stocks:
            sector = stock.sector or 'Other'
            if sector not in sectors:
                sectors[sector] = {
                    'trend': random.uniform(-1.0, 1.0),  # Sector-specific trend
                    'stocks': []
                }
            sectors[sector]['stocks'].append(stock)
        
        sentiment_icons = {
            'bullish': '🐂',
            'bearish': '🐻',
            'neutral': '➡️'
        }
        
        self.stdout.write(f'📈 Simulating realistic prices for {len(stocks)} stocks...')
        self.stdout.write(f'   Market Sentiment: {sentiment_icons[market_sentiment]} {market_sentiment.upper()} (drift: {market_drift:+.2f}%)')
        
        updated = 0
        
        # Process all stocks
        for stock in stocks:
            try:
                old_price = float(stock.current_price)
                
                # Get sector trend
                sector = stock.sector or 'Other'
                sector_trend = sectors[sector]['trend']
                
                # Base volatility: 0.5% to 2% per update
                base_volatility = random.uniform(0.5, 2.0)
                
                # Combine market drift, sector trend, and random volatility
                total_change = market_drift + (sector_trend * 0.3) + random.gauss(0, base_volatility)
                
                # Calculate new price
                new_price = old_price * (1 + total_change / 100)
                
                # Apply safety limits
                # 1. Price bounds: $1 minimum, $50,000 maximum
                new_price = max(1.0, min(50000.0, new_price))
                
                # 2. Max single update change: ±15%
                max_change = old_price * 0.15
                if new_price > old_price + max_change:
                    new_price = old_price + max_change
                elif new_price < old_price - max_change:
                    new_price = old_price - max_change
                
                # Round to 2 decimal places
                new_price = round(new_price, 2)
                
                # Update stock
                stock.previous_close = Decimal(str(old_price))
                stock.current_price = Decimal(str(new_price))
                stock.last_updated = datetime.now()
                stock.save()
                
                change = new_price - old_price
                change_pct = (change / old_price) * 100 if old_price > 0 else 0
                
                icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                color = self.style.SUCCESS if change > 0 else self.style.ERROR if change < 0 else self.style.WARNING
                
                self.stdout.write(
                    color(f'   {icon} {stock.symbol:6s} ${old_price:8.2f} → ${new_price:8.2f}  {change:+7.2f} ({change_pct:+.2f}%)')
                )
                updated += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ {stock.symbol}: {str(e)}'))
        
        # Summary
        self.stdout.write('')
        if updated > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Successfully updated: {updated}/{len(stocks)} stocks'))
            self.stdout.write(self.style.SUCCESS(f'🎲 Mode: Realistic Simulation (Market: {market_sentiment})'))
