# 🎲 Stock Price Simulation System

## Overview
This system uses **realistic market simulation** instead of external APIs to generate stock price movements.

### ✅ Benefits
- **100% Reliable** - No API failures or rate limits
- **Completely Free** - No API keys needed
- **Realistic** - Market sentiment, sector correlations, and proper volatility
- **Fast** - Updates all stocks instantly without network calls

---

## 🎯 How It Works

### Market Simulation Features

1. **Market Sentiment** (Changes each update)
   - 60% chance: Neutral market (±0.1% drift)
   - 20% chance: Bullish market (+0.1% to +0.5% drift)
   - 20% chance: Bearish market (-0.5% to -0.1% drift)

2. **Sector Correlations**
   - Stocks in the same sector move together
   - Each sector gets a random trend (-1% to +1%)
   - Technology, Healthcare, Finance, etc. move as groups

3. **Realistic Volatility**
   - Base volatility: 0.5% to 2% per update
   - Follows normal distribution (Gaussian)
   - Mimics real market price movements

4. **Safety Limits**
   - Price bounds: $1 minimum, $50,000 maximum
   - Max single change: ±15% per update
   - Prevents unrealistic price jumps

### Price Calculation Formula
```
New Price = Old Price × (1 + Total Change%)

Where Total Change = 
  Market Drift (sentiment-based)
  + Sector Trend × 0.3
  + Random Volatility (Gaussian distribution)
```

---

## 🔄 Automation Schedule

### Current Settings
- **Frequency:** Every 1 minute
- **Hours:** 9 AM - 9 PM UTC
- **Days:** Monday - Friday
- **Method:** Both GitHub Actions + Vercel Cron

### Update Frequency
Configured in `.github/workflows/update-prices.yml`:
```yaml
- cron: '* 9-21 * * 1-5'  # Every minute
```

And in `vercel.json`:
```json
"crons": [{
  "path": "/api/update-prices-real",
  "schedule": "* 9-21 * * 1-5"
}]
```

---

## 🎮 Admin Controls

### Manual Sector Adjustments

Admins can **manually override** simulation with sector-wide changes:

1. **Increase Sector by 5%** - Boost entire sector
2. **Decrease Sector by 5%** - Drop entire sector
3. **Increase Sector by 10%** - Major sector rally
4. **Decrease Sector by 10%** - Major sector crash
5. **Apply Custom Percentage** - Any custom % change

These controls work **in addition to** the simulation, allowing you to simulate news events, market reactions, etc.

### Force Update Button

Click "Fetch Real Prices Now" in admin to trigger immediate simulation update for all stocks.

---

## 📊 Testing the System

### Test via API
```bash
curl "https://tradesim-lyart.vercel.app/api/update-prices-real"
```

Expected response:
```json
{
  "success": true,
  "mode": "realistic_simulation",
  "market_sentiment": "bullish",
  "updated_count": 60,
  "total_stocks": 60,
  "message": "Successfully simulated 60 stock prices (Market: bullish)"
}
```

### Test via Management Command
```bash
python manage.py update_real_prices
```

Output will show:
- Current market sentiment (🐂 Bullish / 🐻 Bearish / ➡️ Neutral)
- Each stock's price change with visual indicators
- Summary of updates

### Continuous Updates (Testing)
```bash
python manage.py update_real_prices --continuous --interval 10
```

---

## 🔧 Customization

### Adjust Volatility
Edit `app1/apis.py` or `app1/management/commands/update_real_prices.py`:

```python
# Current: 0.5% to 2%
base_volatility = random.uniform(0.5, 2.0)

# More volatile (2% to 5%)
base_volatility = random.uniform(2.0, 5.0)

# Less volatile (0.1% to 0.5%)
base_volatility = random.uniform(0.1, 0.5)
```

### Change Market Sentiment Distribution
```python
# Current: 60% neutral, 20% bullish, 20% bearish
sentiment_weights = [0.60, 0.20, 0.20]

# More bullish market: 40% neutral, 40% bullish, 20% bearish
sentiment_weights = [0.40, 0.40, 0.20]

# Bear market: 30% neutral, 10% bullish, 60% bearish
sentiment_weights = [0.30, 0.10, 0.60]
```

### Adjust Price Bounds
```python
# Current: $1 to $50,000
new_price = max(1.0, min(50000.0, new_price))

# Penny stocks: $0.01 to $100
new_price = max(0.01, min(100.0, new_price))

# High-value stocks: $10 to $10,000
new_price = max(10.0, min(10000.0, new_price))
```

---

## 📝 Implementation Details

### Files Modified
1. **`app1/apis.py`** - `update_prices_real()` function
   - API endpoint: `/api/update-prices-real`
   - Used by GitHub Actions and Vercel Cron
   
2. **`app1/management/commands/update_real_prices.py`**
   - Django management command
   - Can be run manually or continuously
   
3. **`.github/workflows/update-prices.yml`**
   - GitHub Actions automation
   - Triggers every minute during market hours
   
4. **`vercel.json`**
   - Vercel Cron configuration
   - Redundant backup to GitHub Actions

### No Changes Needed
- **Admin controls** - Still work perfectly
- **Database schema** - No changes required
- **Frontend** - Displays prices as before
- **User experience** - Identical to real data

---

## 🚀 Deployment

### Current Status
✅ Simulation implemented in both API and management command  
✅ Admin sector controls preserved  
✅ Automation running every 1 minute  
✅ No external dependencies required  

### To Deploy Changes
```bash
git add .
git commit -m "Replace API calls with realistic simulation"
git push origin main
```

Vercel will automatically deploy the changes.

---

## 💡 Why Simulation Instead of APIs?

### Problems with APIs
- ❌ Rate limits (25-250 calls/day)
- ❌ Reliability issues (90% failure rates)
- ❌ Free tier restrictions
- ❌ Need API keys and setup
- ❌ Network latency and timeouts

### Advantages of Simulation
- ✅ Zero failures - always works
- ✅ Instant updates - no network calls
- ✅ Unlimited frequency - no rate limits
- ✅ No setup required - works immediately
- ✅ Fully controllable - adjust any parameter
- ✅ Realistic movements - better than many free APIs

---

## 📞 Support

The simulation system is self-contained and requires no external services. All price movements are generated locally using Python's `random` module with realistic statistical distributions.

For questions about customization or extending the simulation, refer to the code comments in:
- `app1/apis.py` (lines 274-390)
- `app1/management/commands/update_real_prices.py` (lines 58-173)
