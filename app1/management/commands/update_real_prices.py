"""
Management command to update stock prices from real market data using Yahoo Finance
"""
from django.core.management.base import BaseCommand
from app1.models import Stock
from datetime import datetime
import sys


class Command(BaseCommand):
    help = 'Update stock prices from real market data using Yahoo Finance API'

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
            self.stdout.write(self.style.SUCCESS(f'🔄 Starting continuous real-time updates (every {interval}s)'))
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
        """Fetch and update real stock prices from Yahoo Finance"""
        try:
            import yfinance as yf
        except ImportError:
            self.stdout.write(self.style.ERROR('❌ yfinance not installed. Run: pip install yfinance'))
            return
        
        # Get stocks to update
        if specific_symbols:
            stocks = Stock.objects.filter(symbol__in=specific_symbols, is_active=True)
        else:
            stocks = Stock.objects.filter(is_active=True)
        
        if not stocks.exists():
            self.stdout.write(self.style.WARNING('⚠️  No active stocks found'))
            return
        
        symbols = [stock.symbol for stock in stocks]
        self.stdout.write(f'📈 Fetching real-time prices for {len(symbols)} stocks...')
        self.stdout.write(f'   Symbols: {", ".join(symbols[:10])}{"..." if len(symbols) > 10 else ""}')
        
        updated = 0
        failed = []
        
        # Fetch data for each symbol
        for stock in stocks:
            try:
                ticker = yf.Ticker(stock.symbol)
                
                # Method 1: Try fast_info first (fastest and most reliable)
                current_price = None
                try:
                    fast_info = ticker.fast_info
                    current_price = float(fast_info.last_price)
                except Exception:
                    # Method 2: Fallback to history (very reliable)
                    try:
                        hist = ticker.history(period="1d")
                        if not hist.empty:
                            current_price = float(hist['Close'].iloc[-1])
                    except Exception:
                        # Method 3: Last resort - try info
                        try:
                            info = ticker.info
                            for field in ['currentPrice', 'regularMarketPrice', 'previousClose']:
                                if field in info and info[field]:
                                    current_price = float(info[field])
                                    break
                        except Exception:
                            pass
                
                if current_price and current_price > 0:
                    old_price = float(stock.current_price)
                    stock.previous_close = old_price
                    stock.current_price = round(current_price, 2)
                    stock.last_updated = datetime.now()
                    stock.save()
                    
                    change = current_price - old_price
                    change_pct = (change / old_price) * 100 if old_price > 0 else 0
                    
                    icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    color = self.style.SUCCESS if change > 0 else self.style.ERROR if change < 0 else self.style.WARNING
                    
                    self.stdout.write(
                        color(f'   {icon} {stock.symbol:6s} ${old_price:8.2f} → ${current_price:8.2f}  {change:+7.2f} ({change_pct:+.2f}%)')
                    )
                    updated += 1
                else:
                    failed.append(stock.symbol)
                    self.stdout.write(self.style.WARNING(f'   ⚠️  {stock.symbol}: No price data available'))
                    
            except Exception as e:
                failed.append(stock.symbol)
                self.stdout.write(self.style.ERROR(f'   ❌ {stock.symbol}: {str(e)}'))
        
        # Summary
        self.stdout.write('')
        if updated > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Successfully updated: {updated}/{len(stocks)} stocks'))
        if failed:
            self.stdout.write(self.style.ERROR(f'❌ Failed to update: {len(failed)} stocks ({", ".join(failed[:5])}{"..." if len(failed) > 5 else ""})'))
