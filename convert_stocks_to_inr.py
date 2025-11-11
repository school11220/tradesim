"""
Standalone script to convert US stock prices from USD to INR
Can be run directly: python convert_stocks_to_inr.py
Or in Django shell: exec(open('convert_stocks_to_inr.py').read())
"""

try:
    from app1.models import Stock
    import random
    
    # Approximate USD to INR exchange rate
    USD_TO_INR = 83.0
    
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
    
    print('Converting US stock prices from USD to INR...')
    print(f'Exchange rate: 1 USD = ₹{USD_TO_INR}')
    print('')
    
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
            print(f'⏭️  Skipped (already converted): {stock.symbol} @ ₹{old_current}')
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
        
        print(f'✅ {stock.symbol}: ${old_current:.2f} → ₹{new_current:.2f} ({"+" if change >= 0 else ""}{change_pct:.2f}%)')
    
    print('')
    print(f'✅ Conversion complete!')
    print(f'Converted: {converted} stocks')
    print(f'Skipped: {skipped} stocks')

except Exception as e:
    print(f'❌ Error: {e}')
    print('Make sure you run this from Django shell or manage.py context')
