"""
Add Indian stocks to the TradeWars platform
Run this script with: python manage.py shell < add_indian_stocks.py
"""

from app1.models import Stock

# Indian stocks to add with INR prices
indian_stocks = [
    # Technology & IT
    {"symbol": "TCS", "name": "Tata Consultancy Services", "sector": "Technology", "price": 3650.00},
    {"symbol": "INFY", "name": "Infosys", "sector": "Technology", "price": 1450.00},
    {"symbol": "WIPRO", "name": "Wipro", "sector": "Technology", "price": 445.00},
    {"symbol": "HCLTECH", "name": "HCL Technologies", "sector": "Technology", "price": 1280.00},
    {"symbol": "TECHM", "name": "Tech Mahindra", "sector": "Technology", "price": 1150.00},
    
    # Banking & Finance
    {"symbol": "HDFCBANK", "name": "HDFC Bank", "sector": "Financials", "price": 1650.00},
    {"symbol": "ICICIBANK", "name": "ICICI Bank", "sector": "Financials", "price": 1050.00},
    {"symbol": "SBIN", "name": "State Bank of India", "sector": "Financials", "price": 625.00},
    {"symbol": "AXISBANK", "name": "Axis Bank", "sector": "Financials", "price": 1080.00},
    {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank", "sector": "Financials", "price": 1750.00},
    
    # Automotive
    {"symbol": "TATAMOTORS", "name": "Tata Motors", "sector": "Automotive", "price": 780.00},
    {"symbol": "MARUTI", "name": "Maruti Suzuki", "sector": "Automotive", "price": 10500.00},
    {"symbol": "M&M", "name": "Mahindra & Mahindra", "sector": "Automotive", "price": 1850.00},
    {"symbol": "BAJAJ-AUTO", "name": "Bajaj Auto", "sector": "Automotive", "price": 9200.00},
    {"symbol": "HEROMOTOCO", "name": "Hero MotoCorp", "sector": "Automotive", "price": 4650.00},
    
    # FMCG & Consumer
    {"symbol": "HINDUNILVR", "name": "Hindustan Unilever", "sector": "Consumer Staples", "price": 2380.00},
    {"symbol": "ITC", "name": "ITC Limited", "sector": "Consumer Staples", "price": 435.00},
    {"symbol": "NESTLEIND", "name": "Nestle India", "sector": "Consumer Staples", "price": 24500.00},
    {"symbol": "BRITANNIA", "name": "Britannia Industries", "sector": "Consumer Staples", "price": 4850.00},
    {"symbol": "DABUR", "name": "Dabur India", "sector": "Consumer Staples", "price": 505.00},
    
    # Energy & Oil
    {"symbol": "RELIANCE", "name": "Reliance Industries", "sector": "Energy", "price": 2850.00},
    {"symbol": "ONGC", "name": "Oil & Natural Gas Corp", "sector": "Energy", "price": 245.00},
    {"symbol": "BPCL", "name": "Bharat Petroleum", "sector": "Energy", "price": 315.00},
    {"symbol": "IOC", "name": "Indian Oil Corporation", "sector": "Energy", "price": 135.00},
    {"symbol": "COALINDIA", "name": "Coal India", "sector": "Energy", "price": 410.00},
    
    # Pharmaceuticals
    {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical", "sector": "Healthcare", "price": 1550.00},
    {"symbol": "DRREDDY", "name": "Dr. Reddy's Laboratories", "sector": "Healthcare", "price": 5800.00},
    {"symbol": "CIPLA", "name": "Cipla", "sector": "Healthcare", "price": 1380.00},
    {"symbol": "AUROPHARMA", "name": "Aurobindo Pharma", "sector": "Healthcare", "price": 1210.00},
    {"symbol": "DIVISLAB", "name": "Divi's Laboratories", "sector": "Healthcare", "price": 3650.00},
    
    # Metals & Mining
    {"symbol": "TATASTEEL", "name": "Tata Steel", "sector": "Materials", "price": 140.00},
    {"symbol": "HINDALCO", "name": "Hindalco Industries", "sector": "Materials", "price": 645.00},
    {"symbol": "VEDL", "name": "Vedanta Limited", "sector": "Materials", "price": 425.00},
    {"symbol": "JSWSTEEL", "name": "JSW Steel", "sector": "Materials", "price": 920.00},
    {"symbol": "NMDC", "name": "NMDC Limited", "sector": "Materials", "price": 220.00},
    
    # Telecom
    {"symbol": "BHARTIARTL", "name": "Bharti Airtel", "sector": "Communication Services", "price": 1480.00},
    {"symbol": "IDEA", "name": "Vodafone Idea", "sector": "Communication Services", "price": 12.50},
    
    # Real Estate & Infrastructure
    {"symbol": "LT", "name": "Larsen & Toubro", "sector": "Industrials", "price": 3450.00},
    {"symbol": "ADANIPORTS", "name": "Adani Ports", "sector": "Industrials", "price": 1180.00},
    {"symbol": "ULTRACEMCO", "name": "UltraTech Cement", "sector": "Materials", "price": 9800.00},
    
    # Retail
    {"symbol": "DMART", "name": "Avenue Supermarts", "sector": "Consumer Discretionary", "price": 3750.00},
    {"symbol": "TRENT", "name": "Trent Limited", "sector": "Consumer Discretionary", "price": 5200.00},
]

print("Adding Indian stocks to the database...")
added = 0
updated = 0

for stock_data in indian_stocks:
    import random
    # Add random price variation to show changes (-2% to +2%)
    current_price = stock_data["price"]
    # Create variation in previous_close (2% to 5% difference)
    variation = random.uniform(0.97, 1.05)  # 97% to 105% of current price
    previous_close = current_price * variation
    
    stock, created = Stock.objects.update_or_create(
        symbol=stock_data["symbol"],
        defaults={
            "name": stock_data["name"],
            "sector": stock_data["sector"],
            "current_price": round(current_price, 2),
            "previous_close": round(previous_close, 2),
            "is_active": True
        }
    )
    if created:
        added += 1
        print(f"✅ Added: {stock.symbol} - {stock.name} @ ₹{stock.current_price}")
    else:
        updated += 1
        print(f"🔄 Updated: {stock.symbol} - {stock.name} @ ₹{stock.current_price}")

print(f"\n✅ Complete! Added {added} new stocks, updated {updated} existing stocks.")
print(f"Total Indian stocks in database: {len(indian_stocks)}")
