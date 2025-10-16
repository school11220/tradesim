# Stock Price Update System - October 16, 2025

## ✅ Automatic Price Updates Implemented!

Your TradeSim platform now has **automatic stock price updates** that simulate real market fluctuations!

---

## 🎯 How It Works

### 1. **Price Update API Endpoint**
**URL:** `/api/update-prices`

This endpoint triggers an update of all active stock prices with random fluctuations.

**Parameters:**
- `volatility` (optional): Price change percentage (default: 0.02 = ±2%)

**Example Usage:**
```bash
# Update with default 2% volatility
https://tradesim-lyart.vercel.app/api/update-prices

# Update with custom 5% volatility
https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.05
```

**Response:**
```json
{
  "success": true,
  "updated_count": 60,
  "volatility": 0.02,
  "updates": [
    {
      "symbol": "AAPL",
      "old_price": 150.25,
      "new_price": 151.50,
      "change": 1.25,
      "change_percent": 0.83
    },
    ...
  ]
}
```

### 2. **GitHub Actions Workflow**
**File:** `.github/workflows/update-prices.yml`

**Schedule:**
- Runs **every 5 minutes**
- During trading hours: **9 AM - 4 PM UTC** (Mon-Fri)
- Automatically calls the price update API

**Manual Trigger:**
You can also manually trigger updates:
1. Go to: https://github.com/school11220/tradesim/actions
2. Select "Update Stock Prices" workflow
3. Click "Run workflow"

---

## 🚀 What's Automated

### ✅ Price Changes Every 5 Minutes
- All 60 stocks update automatically
- Random fluctuations within ±2% (configurable)
- Simulates real market behavior
- No manual intervention needed

### ✅ Smart Scheduling
- Only runs during business hours
- Monday through Friday
- No weekend updates (markets closed)
- Saves resources

### ✅ Real-Time Updates on Frontend
- Browse Stocks page auto-refreshes every 15s
- Portfolio page auto-refreshes every 20s
- Flash animations when prices change
- Color-coded gains (green) and losses (red)

---

## 📊 How Prices Update

### Random Fluctuation Algorithm
```python
# For each stock:
1. Generate random change: ±2% (default)
2. Calculate new price = current_price * (1 + change)
3. Ensure price stays above $0.01
4. Save previous price for change calculation
5. Update current price
6. Save to database
```

### Example:
```
Stock: AAPL
Current Price: $150.00
Random Change: +1.5%
New Price: $152.25
Price Change: +$2.25 (▲)
```

---

## 🎮 How Teams See Changes

### Browse Stocks Page
- **Every 15 seconds**: AJAX call to get latest prices
- **Flash Animation**: 
  - Green flash when price increases
  - Red flash when price decreases
- **Price Display**: Shows change with ▲/▼ arrows
- **Owned Badge**: Highlights stocks in portfolio

### Portfolio Page
- **Every 20 seconds**: Recalculates all values
- **Live P&L**: Updates profit/loss automatically
- **Market Value**: Recalculates based on current prices
- **Summary Cards**: All 4 cards update in real-time

### Dashboard
- **Real-time**: Portfolio value updates live
- **Total P&L**: Refreshes automatically
- **Holdings Count**: Shows current positions

---

## 🔧 Manual Price Updates

### Option 1: GitHub Actions (Recommended)
```
1. Go to: https://github.com/school11220/tradesim/actions
2. Click "Update Stock Prices"
3. Click "Run workflow" → "Run workflow"
4. Wait ~10 seconds
5. Check TradeSim - prices updated!
```

### Option 2: Direct API Call
```bash
curl "https://tradesim-lyart.vercel.app/api/update-prices"
```

### Option 3: Management Command (Local Only)
```bash
# Single update
python manage.py update_stock_prices

# Continuous updates every 30 seconds
python manage.py update_stock_prices --continuous

# Custom interval (10 seconds)
python manage.py update_stock_prices --continuous --interval 10

# Higher volatility (5%)
python manage.py update_stock_prices --volatility 0.05
```

---

## ⚙️ Configuration

### Adjust Update Frequency
Edit `.github/workflows/update-prices.yml`:

```yaml
# Every 2 minutes
- cron: '*/2 9-16 * * 1-5'

# Every 10 minutes
- cron: '*/10 9-16 * * 1-5'

# Every hour
- cron: '0 9-16 * * 1-5'
```

### Adjust Volatility
Change the curl command in the workflow:

```yaml
# Higher volatility (5%)
curl "https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.05"

# Lower volatility (1%)
curl "https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.01"
```

### Trading Hours
Adjust cron schedule for different timezones:

```yaml
# 9 AM - 4 PM EST (add 5 hours to UTC)
- cron: '*/5 14-21 * * 1-5'

# 9 AM - 4 PM PST (add 8 hours to UTC)
- cron: '*/5 17-0 * * 1-5'
```

---

## 🧪 Testing

### Test API Endpoint
```bash
# Test in browser or curl
https://tradesim-lyart.vercel.app/api/update-prices

# Should return JSON with:
# - success: true
# - updated_count: 60
# - updates: [array of stock changes]
```

### Verify Frontend Updates
1. **Login to team**
2. **Go to Browse Stocks**
3. **Note a few stock prices**
4. **Trigger manual update** (GitHub Actions or API)
5. **Wait 15 seconds** (auto-refresh interval)
6. **Watch prices change** with flash animations!

### Check Logs
GitHub Actions logs show each price update:
```
Updating stock prices...
{
  "success": true,
  "updated_count": 60,
  ...
}
Stock prices updated!
```

---

## 📈 Price Update Statistics

### Default Settings
- **Frequency**: Every 5 minutes
- **Volatility**: ±2% per update
- **Active Hours**: 7 hours/day (9 AM - 4 PM)
- **Updates/Day**: ~84 updates
- **Updates/Week**: ~420 updates (Mon-Fri)

### Price Movement Example
Starting Price: $100.00

After 1 hour (12 updates at ±2%):
- Best case: $126.82 (+26.82%)
- Worst case: $78.85 (-21.15%)
- Typical: $98-$102 (±2-3%)

---

## 🎯 Benefits

### For Teams
- ✅ **Realistic trading** - Prices change like real markets
- ✅ **Strategy testing** - Buy low, sell high
- ✅ **Risk management** - Learn to handle volatility
- ✅ **Live excitement** - Watch portfolio values change

### For Admins
- ✅ **Fully automatic** - No manual intervention
- ✅ **Configurable** - Adjust frequency and volatility
- ✅ **Serverless** - Works on Vercel without persistent server
- ✅ **Free** - GitHub Actions included in free tier

### For Competition
- ✅ **Fair** - All teams see same price changes
- ✅ **Engaging** - Keeps teams checking back
- ✅ **Educational** - Teaches market dynamics
- ✅ **Competitive** - Real-time leaderboard changes

---

## 🚨 Troubleshooting

### Prices Not Changing?

**Check GitHub Actions:**
```
1. Go to: https://github.com/school11220/tradesim/actions
2. Look for "Update Stock Prices" runs
3. Check if workflow is running (green checkmark)
4. View logs for any errors
```

**Manual Trigger:**
```
Run workflow manually to test:
1. Actions → Update Stock Prices
2. Run workflow
3. Check logs for success
4. Verify frontend shows changes
```

**Check API Endpoint:**
```bash
# Test API directly
curl "https://tradesim-lyart.vercel.app/api/update-prices"

# Should return success:true
```

### Frontend Not Showing Updates?

**Check Auto-Refresh:**
- Browse Stocks: Refreshes every 15s
- Portfolio: Refreshes every 20s
- Wait for next refresh cycle
- Or click manual "Refresh" button

**Hard Refresh Browser:**
- Ctrl+Shift+R (Windows)
- Cmd+Shift+R (Mac)
- Clears cached JavaScript

---

## 📝 Summary

### What Was Added
1. ✅ **API Endpoint**: `/api/update-prices`
2. ✅ **GitHub Workflow**: `.github/workflows/update-prices.yml`
3. ✅ **Automatic Schedule**: Every 5 minutes, trading hours only
4. ✅ **Manual Trigger**: Available in GitHub Actions
5. ✅ **Frontend Updates**: Already implemented (15s/20s refresh)

### What It Does
- Updates all 60 stock prices every 5 minutes
- Random fluctuations within ±2%
- Runs automatically during trading hours
- Teams see changes in real-time on frontend
- No manual intervention needed

### How to Use
- **Automatic**: Just works! Prices update every 5 min
- **Manual**: Go to GitHub Actions → Run workflow
- **Testing**: Call `/api/update-prices` endpoint
- **Monitor**: Check GitHub Actions logs

---

**Your TradeSim platform now has live, automatic stock price updates! 🎉📈**

Prices will start changing within the next 5-minute interval during trading hours!
