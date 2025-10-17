# 📊 Stock Market Integration & Event System

## 🎯 Overview

TradeSim now features a **comprehensive stock market control system** that combines:
1. **Real Stock API Integration** (Yahoo Finance via yfinance)
2. **Market Events Dashboard** (News-driven price movements)
3. **Custom Percentage Control** (Precise sector/stock adjustments)
4. **Sector News Feed** (Real-time event notifications for teams)

---

## 🚀 Features

### 1. **Real Stock Market API Integration**
- ✅ Live prices from Yahoo Finance (FREE, no API key needed)
- ✅ Toggle between REAL and SIMULATED modes
- ✅ Automatic updates via GitHub Actions
- ✅ Manual update commands

### 2. **Market Events Dashboard**
- ✅ Create news-driven market events
- ✅ Trigger sector-wide price changes with storylines
- ✅ Track which stocks/sectors were affected
- ✅ Schedule future events or trigger immediately

### 3. **Custom Percentage Input**
- ✅ Apply ANY percentage change to sectors
- ✅ Quick preset buttons (+5%, +10%, -5%, -10%)
- ✅ Custom input field for precise control (e.g., +7.3%)
- ✅ Affects entire sectors or specific stocks

### 4. **Sector News Feed**
- ✅ Teams see market events in real-time
- ✅ News ticker on dashboard
- ✅ Auto-refreshes every 30 seconds
- ✅ Shows why prices are moving (educational!)

---

## 📦 Installation

### 1. Install Dependencies
```bash
pip install yfinance==0.2.28
```

Already included in `requirements.txt`!

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the `MarketEvent` model.

---

## 🎮 How to Use

### **Admin Control Panel**

#### Access Market Control Center:
1. Go to: `/admin/app1/stock/market-control/`
2. Or click **"Market Control"** from Stock admin page

#### Quick Actions Available:
- **📈 Fetch Real Prices** - Get live data from Yahoo Finance
- **🎲 Randomize Prices** - Apply ±2% volatility
- **📰 Create Market Event** - News + price impact

---

### **Option 1: Real Market Data Mode**

#### Enable Real Prices:
1. Go to Market Control Center
2. Click **"Switch Mode"** button
3. Prices now come from Yahoo Finance!

#### Update Manually:
```bash
python manage.py update_real_prices
```

#### Continuous Updates (every 60 seconds):
```bash
python manage.py update_real_prices --continuous --interval 60
```

#### Update Specific Stocks:
```bash
python manage.py update_real_prices --symbols AAPL MSFT GOOGL
```

---

### **Option 2: Market Events Dashboard**

#### Create a Market Event:
1. Go to: `/admin/app1/marketevent/add/`
2. Fill in:
   - **Title**: "Tech Sector Rally on AI Breakthrough"
   - **Description**: "Major tech companies surge as new AI chip announced"
   - **Event Type**: Sector Rally
   - **Affected Sector**: Technology
   - **Severity**: Major (+10%)
   - **Is Positive**: ✅ Yes

3. Save the event

#### Trigger the Event:
**Method A - From Event List:**
1. Go to `/admin/app1/marketevent/`
2. Select your event
3. Actions → **"⚡ TRIGGER selected events"**
4. Click "Go"

**Method B - Auto-trigger on Save:**
Events are automatically applied when created!

#### What Happens:
- ✅ All stocks in "Technology" sector increase by 10%
- ✅ Teams see the event in their news feed
- ✅ Event shows as "Triggered" in admin
- ✅ Tracks how many stocks were affected

---

### **Option 3: Custom Percentage Control**

#### From Stock Admin:
1. Go to `/admin/app1/stock/`
2. Select stocks from ANY sector
3. Actions → **"⚙️ Apply CUSTOM % change"**
4. Enter percentage (e.g., `7.5` or `-3.2`)
5. Click "Apply Changes"

#### From Market Control Panel:
1. Go to Market Control Center
2. Select a sector from dropdown
3. **Quick Buttons:**
   - 📈 +5% | 🚀 +10%
   - 📉 -5% | 💥 -10%
4. **Custom Input:**
   - Enter any % (e.g., `12.75`)
   - Click "Apply Custom %"

---

### **Sector-Based Actions**

Available actions when you select stocks in admin:

| Action | Description | Impact |
|--------|-------------|--------|
| 📈 Fetch REAL market prices | Updates from Yahoo Finance | Live data |
| 📊 Sector Rally +5% | Increases entire sector | +5% |
| 🚀 Major Sector Rally +10% | Major sector increase | +10% |
| 📉 Sector Crash -5% | Decreases entire sector | -5% |
| 💥 Major Sector Crash -10% | Major sector decrease | -10% |
| ⚙️ Apply CUSTOM % change | User-defined percentage | Any % |

---

## 📰 News Feed for Teams

### Where Teams See Events:
Teams see the market events feed on:
- **Dashboard** (if included)
- **Browse Stocks page** (add `{% include 'components/market_events_feed.html' %}`)
- **Portfolio page** (optional)

### Add News Feed to Any Page:
```django
{% include 'components/market_events_feed.html' %}
```

### Features:
- ✅ Shows last 24 hours of events
- ✅ Auto-refreshes every 30 seconds
- ✅ Color-coded (Green = Bullish, Red = Bearish)
- ✅ Shows affected sector + percentage
- ✅ Timestamp of when event occurred

---

## 🤖 API Endpoints

### For GitHub Actions / External Systems:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/update-prices` | POST | Simulated update (±2%) |
| `/api/update-prices-real` | POST | Real Yahoo Finance data |
| `/api/update-prices-auto` | POST | Auto (checks setting) |
| `/api/toggle-price-mode` | POST | Switch real/simulated |
| `/api/adjust-sector` | POST | Adjust sector by % |
| `/api/market-events` | GET | Get recent events |

### Example API Call:
```bash
# Update with real prices
curl -X POST https://yoursite.com/api/update-prices-real

# Adjust Technology sector by +5%
curl -X POST https://yoursite.com/api/adjust-sector \
  -H "Content-Type: application/json" \
  -d '{"sector": "Technology", "percentage": 5.0}'
```

---

## 🎓 Teaching Use Cases

### **Real Market Mode:**
- Live trading competitions during market hours
- Learning technical analysis with real patterns
- Understanding news impact on stock prices
- Correlating events to market movements

### **Market Events:**
- **Scenario 1:** "FDA Approval" → Healthcare sector +15%
  - Teaches: Regulatory impact on stocks
  
- **Scenario 2:** "Oil Crisis" → Energy sector -10%
  - Teaches: Supply/demand economics
  
- **Scenario 3:** "Tech Earnings Beat" → Technology +8%
  - Teaches: Earnings reports matter

- **Scenario 4:** "Interest Rate Hike" → All sectors -3%
  - Teaches: Macro-economic factors

### **Custom Percentage:**
- Simulate specific market conditions
- Create quiz scenarios ("What if sector X drops 7%?")
- Test student strategies under different volatilities

---

## 🛠️ Configuration

### Default Mode:
Set in SimulatorSettings:
```python
# Admin → Simulator Settings → Add new:
setting_name: use_real_prices
setting_value: false  # or true
description: Use real stock market prices from Yahoo Finance
```

### GitHub Actions Auto-Update:
File: `.github/workflows/update-prices.yml`

```yaml
on:
  schedule:
    - cron: '*/2 6-23 * * 1-5'  # Every 2 minutes, trading hours
```

Mode determined by `use_real_prices` setting automatically!

---

## 📊 Database Schema

### MarketEvent Model:
```python
title = "Tech Sector Rally"
description = "AI breakthrough drives tech stocks higher"
event_type = 'sector_rally'  # sector_rally, sector_crash, market_news, etc.
affected_sector = "Technology"
severity = 'major'  # minor (±2%), moderate (±5%), major (±10%), extreme (±15%), custom
custom_percentage = 12.50  # Optional: precise control
is_positive = True  # Price increase?
is_triggered = False  # Has event happened?
triggered_at = None  # When triggered
stocks_affected = 0  # Count of stocks changed
total_impact = "{...}"  # JSON of all changes
```

---

## 🎯 Quick Start Guide

### **Scenario: Simulate a Market Crash**

1. **Create Event:**
   - Admin → Market Events → Add
   - Title: "Market Crash: Global Recession Fears"
   - Description: "Concerns over economy trigger sell-off"
   - Event Type: Market News
   - Affected Sector: (Leave empty for ALL sectors)
   - Severity: Major (-10%)
   - Is Positive: ❌ No

2. **Trigger Event:**
   - Select event → Actions → Trigger
   - ALL stocks drop 10%!

3. **Teams See:**
   - News feed shows: "📉 Market Crash: Global Recession Fears"
   - Prices drop across portfolio
   - Time to buy the dip? 📊

---

## 🔥 Pro Tips

### **Combine All 3 Options:**

**Morning:** Use real prices for market open
```bash
# 9:30 AM - Switch to real mode
Toggle: Real Market Mode ON
```

**Midday:** Create news event
```bash
# 12:00 PM - Breaking news!
Event: "Apple Announces New iPhone"
Sector: Technology +7%
```

**Afternoon:** Custom adjustment
```bash
# 2:00 PM - Sector-specific move
Healthcare +3.5% (custom)
```

**Evening:** Back to simulated for after-hours
```bash
# 4:00 PM - Market closed
Toggle: Simulated Mode ON
```

---

## ✅ Checklist

After setup, verify:
- [ ] yfinance installed
- [ ] Migrations run (MarketEvent model created)
- [ ] Can toggle Real/Simulated mode
- [ ] Can fetch real prices manually
- [ ] Can create and trigger Market Events
- [ ] News feed shows events on team pages
- [ ] Custom % control works for sectors
- [ ] GitHub Actions updating automatically

---

## 🆘 Troubleshooting

### **"yfinance not installed"**
```bash
pip install yfinance==0.2.28
# Then redeploy
```

### **"No active stocks found"**
- Go to `/admin/app1/stock/`
- Make sure stocks have `is_active = True`

### **Events not showing for teams**
- Check event `is_active = True`
- Check event `is_triggered = True`
- Add news feed component to team pages:
  ```django
  {% include 'components/market_events_feed.html' %}
  ```

### **Prices not updating with real mode**
- Verify internet connection
- Check stock symbols are valid (Yahoo Finance format)
- Try manual update: `python manage.py update_real_prices`

---

## 🎉 Summary

You now have a **professional-grade stock market control system** with:
- ✅ Real API integration (Yahoo Finance)
- ✅ Market events with news storylines
- ✅ Custom percentage control
- ✅ Live news feed for teams
- ✅ Toggle between real/simulated
- ✅ Fully automated updates

**Your students can now experience realistic market dynamics while you control the narrative!** 📈🎓

---

**Need help?** Check the admin panel at `/admin/app1/stock/market-control/` for the visual control center!
