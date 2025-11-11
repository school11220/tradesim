# Add Indian Stocks to TradeWars - Production Guide

## Quick Setup Script

Run this in your production Django shell or as a management command:

```python
from app1.models import Stock

# Indian stocks with INR prices
indian_stocks = [
    # Technology & IT Services
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
    
    # Infrastructure & Real Estate
    {"symbol": "LT", "name": "Larsen & Toubro", "sector": "Industrials", "price": 3450.00},
    {"symbol": "ADANIPORTS", "name": "Adani Ports", "sector": "Industrials", "price": 1180.00},
    {"symbol": "ULTRACEMCO", "name": "UltraTech Cement", "sector": "Materials", "price": 9800.00},
    
    # Retail
    {"symbol": "DMART", "name": "Avenue Supermarts (DMart)", "sector": "Consumer Discretionary", "price": 3750.00},
    {"symbol": "TRENT", "name": "Trent Limited", "sector": "Consumer Discretionary", "price": 5200.00},
]

# Add stocks to database
for stock_data in indian_stocks:
    stock, created = Stock.objects.update_or_create(
        symbol=stock_data["symbol"],
        defaults={
            "name": stock_data["name"],
            "sector": stock_data["sector"],
            "current_price": stock_data["price"],
            "previous_close": stock_data["price"],
            "is_active": True
        }
    )
    print(f"{'✅ Added' if created else '🔄 Updated'}: {stock.symbol} - {stock.name} @ ₹{stock.current_price}")

print(f"\n✅ Indian stocks setup complete!")
```

## Alternative: Using Django Admin

1. Go to `/admin/app1/stock/`
2. Click "Add Stock" for each company
3. Use the data from the table below

## Indian Stocks Reference Table

### Technology (5 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| TCS | Tata Consultancy Services | Technology | 3,650 |
| INFY | Infosys | Technology | 1,450 |
| WIPRO | Wipro | Technology | 445 |
| HCLTECH | HCL Technologies | Technology | 1,280 |
| TECHM | Tech Mahindra | Technology | 1,150 |

### Banking & Finance (5 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| HDFCBANK | HDFC Bank | Financials | 1,650 |
| ICICIBANK | ICICI Bank | Financials | 1,050 |
| SBIN | State Bank of India | Financials | 625 |
| AXISBANK | Axis Bank | Financials | 1,080 |
| KOTAKBANK | Kotak Mahindra Bank | Financials | 1,750 |

### Automotive (5 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| TATAMOTORS | Tata Motors | Automotive | 780 |
| MARUTI | Maruti Suzuki | Automotive | 10,500 |
| M&M | Mahindra & Mahindra | Automotive | 1,850 |
| BAJAJ-AUTO | Bajaj Auto | Automotive | 9,200 |
| HEROMOTOCO | Hero MotoCorp | Automotive | 4,650 |

### FMCG & Consumer (5 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| HINDUNILVR | Hindustan Unilever | Consumer Staples | 2,380 |
| ITC | ITC Limited | Consumer Staples | 435 |
| NESTLEIND | Nestle India | Consumer Staples | 24,500 |
| BRITANNIA | Britannia Industries | Consumer Staples | 4,850 |
| DABUR | Dabur India | Consumer Staples | 505 |

### Energy & Oil (5 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| RELIANCE | Reliance Industries | Energy | 2,850 |
| ONGC | Oil & Natural Gas Corp | Energy | 245 |
| BPCL | Bharat Petroleum | Energy | 315 |
| IOC | Indian Oil Corporation | Energy | 135 |
| COALINDIA | Coal India | Energy | 410 |

### Pharmaceuticals (5 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| SUNPHARMA | Sun Pharmaceutical | Healthcare | 1,550 |
| DRREDDY | Dr. Reddy's Laboratories | Healthcare | 5,800 |
| CIPLA | Cipla | Healthcare | 1,380 |
| AUROPHARMA | Aurobindo Pharma | Healthcare | 1,210 |
| DIVISLAB | Divi's Laboratories | Healthcare | 3,650 |

### Metals & Mining (5 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| TATASTEEL | Tata Steel | Materials | 140 |
| HINDALCO | Hindalco Industries | Materials | 645 |
| VEDL | Vedanta Limited | Materials | 425 |
| JSWSTEEL | JSW Steel | Materials | 920 |
| NMDC | NMDC Limited | Materials | 220 |

### Telecom (2 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| BHARTIARTL | Bharti Airtel | Communication Services | 1,480 |
| IDEA | Vodafone Idea | Communication Services | 12.50 |

### Infrastructure (3 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| LT | Larsen & Toubro | Industrials | 3,450 |
| ADANIPORTS | Adani Ports | Industrials | 1,180 |
| ULTRACEMCO | UltraTech Cement | Materials | 9,800 |

### Retail (2 stocks)
| Symbol | Company Name | Sector | Price (₹) |
|--------|-------------|--------|-----------|
| DMART | Avenue Supermarts (DMart) | Consumer Discretionary | 3,750 |
| TRENT | Trent Limited | Consumer Discretionary | 5,200 |

## Total: 42 Indian Companies

These stocks represent major companies from the Indian stock market (NSE/BSE) across diverse sectors.

## Currency Changes Applied

All currency symbols have been changed from $ (USD) to ₹ (INR) in:
- ✅ Admin interface
- ✅ Team dashboard
- ✅ Team portfolio
- ✅ Team stocks/browse page
- ✅ All team templates
- ✅ Documentation files

## Initial Capital Recommendation

For Indian market context, consider updating the default starting balance:
- **Current:** ₹500,000 (5 Lakhs) - Good for retail investor simulation
- **Alternative:** ₹1,000,000 (10 Lakhs) - For larger portfolio management
- **Update in:** Django Admin → Simulator Settings → default_user_balance

## Notes

1. Prices are approximate and should be updated periodically
2. All prices are in Indian Rupees (₹)
3. Stocks can be activated/deactivated via admin panel
4. Price simulation will work the same way for Indian stocks
5. Mix Indian and international stocks for a global trading experience!
