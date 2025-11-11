# Stock Price Data Source Explanation 📊

## Current Situation

### What You're Seeing Now (Local Development)
The prices you see in your admin panel are the **initial prices** from the populate_stocks.py script. These are static values until the price update system runs.

### What Happens in Deployment

## ✅ YES - Real Yahoo Finance API is Used!

Your system **DOES fetch real prices from Yahoo Finance API** in production. Here's how:

---

## How It Works

### 1. **Price Update System**

Your system has a GitHub Action (`.github/workflows/update-prices.yml`) that:
- Runs every 5 minutes during market hours (9 AM - 9 PM UTC)
- Calls the endpoint: `/api/update-prices-real`
- This endpoint uses the `yfinance` Python library
- Fetches REAL, LIVE prices from Yahoo Finance

### 2. **The API Endpoint** (`/api/update-prices-real`)

```python
def update_prices_real(request):
    """
    Fetch REAL stock prices from Yahoo Finance API using yfinance
    Updates all active stocks with current market prices
    """
    import yfinance as yf
    
    # Fetches all symbols at once
    tickers = yf.Tickers('AAPL MSFT GOOGL META ...')
    
    # For each stock:
    for stock in stocks:
        ticker = tickers.tickers[stock.symbol]
        info = ticker.info
        
        # Get REAL market data
        current_price = info.get('currentPrice')  # Live price
        previous_close = info.get('previousClose')  # Previous day close
        
        # Update database
        stock.current_price = current_price
        stock.previous_close = previous_close
        stock.save()
```

---

## Price Data Sources

### Yahoo Finance API Provides:
- ✅ **Current Market Price** - Real-time or 15-minute delayed
- ✅ **Previous Close** - Yesterday's closing price  
- ✅ **Price Changes** - Calculated from current vs previous
- ✅ **Market State** - OPEN, CLOSED, PRE, POST
- ✅ **Volume** - Trading volume
- ✅ **52-Week High/Low** - Annual range

### What Your System Displays:
- **Current Price**: From Yahoo Finance `currentPrice` or `regularMarketPrice`
- **Previous Close**: From Yahoo Finance `previousClose`
- **Price Change**: Calculated as (current_price - previous_close)
- **Change Percent**: Calculated as (change / previous_close) × 100

---

## Verification

### How to Verify Real Data is Being Used:

1. **Check GitHub Actions**
   - Go to: https://github.com/school11220/tradesim/actions
   - Look for "Update Stock Prices from Yahoo Finance"
   - Check recent runs - they should show "Real stock prices fetched successfully"

2. **Compare with Real Market**
   - Check a stock price in your system (e.g., AAPL)
   - Compare with: https://finance.yahoo.com/quote/AAPL
   - Prices should match (or be close if delayed)

3. **Check Update Timestamps**
   - In admin panel, each stock has `last_updated` field
   - This shows when Yahoo Finance last updated the price
   - Should be recent (within last 5 minutes during market hours)

4. **Look for Price Patterns**
   - Real prices follow actual market movements
   - Stocks move up/down based on real events
   - After market close, prices freeze until next open

---

## Different Modes Available

Your system has **3 price update modes**:

### Mode 1: Real Yahoo Finance API ✅ (CURRENT)
- **Endpoint**: `/api/update-prices-real`
- **Source**: Yahoo Finance via yfinance library
- **Accuracy**: Real market data (live or 15-min delayed)
- **Use Case**: Production, competitions with real data

### Mode 2: Simulation (NOT USED)
- **Endpoint**: `/api/update-prices` (trigger_price_update)
- **Source**: Random fluctuations (±2% default)
- **Accuracy**: Completely random
- **Use Case**: Testing, demonstrations

### Mode 3: Auto Mode (NOT CONFIGURED)
- **Endpoint**: `/api/update-prices-auto`
- **Source**: Checks database setting, uses Mode 1 or 2
- **Accuracy**: Depends on setting
- **Use Case**: Flexible switching between modes

---

## Current Configuration

Your `.github/workflows/update-prices.yml` is configured to:

```yaml
# Runs every 5 minutes
- cron: '*/5 9-21 * * 1-5'

# Calls this endpoint
curl "https://tradesim-lyart.vercel.app/api/update-prices-real"
```

This means:
✅ **Real Yahoo Finance data**
✅ **Updates every 5 minutes**
✅ **Only during market hours (9 AM - 9 PM UTC)**
✅ **Only on weekdays (Monday-Friday)**

---

## Why Prices Might Look "Random" Locally

On your **local development** server:
- The GitHub Action doesn't run
- Prices are from the initial populate_stocks.py script
- They won't update automatically
- They're just starting values for development

To update prices locally, you can:

### Option 1: Call the API manually
```bash
curl http://127.0.0.1:8000/api/update-prices-real
```

### Option 2: Create a local cron job
Add to your crontab:
```bash
*/5 * * * * curl http://127.0.0.1:8000/api/update-prices-real > /dev/null 2>&1
```

### Option 3: Use admin controls
- Go to Admin → Stocks → Custom Price Control
- Manually set prices for testing

---

## Market Data Accuracy

### Yahoo Finance Data Quality:
- **Delay**: 15 minutes for most stocks (real-time for some)
- **Availability**: All US stocks (NYSE, NASDAQ)
- **Reliability**: Very high (same source used by many apps)
- **Cost**: FREE (with reasonable rate limits)

### Rate Limits:
- Yahoo Finance allows ~2,000 requests per hour
- Your system fetches 188 stocks every 5 minutes = ~37 requests/hour
- Well within limits ✅

---

## Deployment vs Local

| Feature | Local (127.0.0.1:8000) | Deployment (Vercel) |
|---------|------------------------|---------------------|
| Initial Prices | populate_stocks.py | populate_stocks.py |
| Price Updates | Manual only | Automatic every 5 min |
| Data Source | Static | Yahoo Finance API |
| Accuracy | Static/Test values | Real market data |
| Market Hours | N/A | Respects market hours |

---

## Summary

### ✅ To Answer Your Question:

**In Deployment**: Prices come from **Yahoo Finance API** (real market data)
**Locally**: Prices are **static** from populate_stocks.py (test data)

The prices you see in the screenshot are either:
1. Initial values from populate_stocks.py (if never updated)
2. Real Yahoo Finance data (if GitHub Action has run)

To verify which one, check the `last_updated` timestamp on the stocks. If it's recent (within 5 minutes), it's real Yahoo data. If it's older (from when you ran populate_stocks.py), it's static data waiting for the first update.

---

## Next Steps

1. **Deploy your changes** to trigger the GitHub Action
2. **Wait 5 minutes** for the first update to run
3. **Check the prices** - they should match Yahoo Finance
4. **Monitor GitHub Actions** tab to see updates running

Your system is already configured correctly! 🎉
