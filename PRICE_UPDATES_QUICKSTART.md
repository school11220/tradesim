# 🎯 STOCK PRICE AUTO-UPDATE - QUICK START GUIDE

## ✅ What We've Added

Your stock trading platform now **simulates a real stock market** with automatic price fluctuations!

## 🚀 Three Ways to Use It

### 1️⃣ Quick Demo (5-second updates, high volatility)
```bash
./demo_price_updates.sh
```
- Updates every **5 seconds**
- ±3% price changes (dramatic for demo)
- Perfect for showing off the feature!

### 2️⃣ Realistic Mode (30-second updates)
```bash
./start_price_updater.sh
```
- Updates every **30 seconds**
- ±2% price changes (realistic)
- Run this during competitions

### 3️⃣ Custom Settings
```bash
# Update every 10 seconds with ±1% changes
python manage.py update_stock_prices --continuous --interval 10 --volatility 0.01

# Single update (no loop)
python manage.py update_stock_prices
```

### 4️⃣ Admin Panel (Manual Control)
1. Go to Django Admin → Stocks
2. Select stocks
3. Action: **"📊 Apply random fluctuation (±2%)"**
4. Click "Go"

## 📺 See It In Action

### Terminal View:
```
📊 Update #1 at 09:51:44
   Updating 66 stocks...
   
   AAPL   $150.50 → $152.30  +$1.80 (+1.20%)
   GOOGL  $125.80 → $124.50  -$1.30 (-1.03%)
   TSLA   $242.85 → $247.10  +$4.25 (+1.75%)
   ...
   
   📈 Gainers: 37
      Top: LOW +1.97%
   📉 Losers: 29
      Top: PSX -1.91%
```

### Team Dashboard:
- Visit: `http://127.0.0.1:8000/team/stocks`
- Refresh page to see new prices
- Green/red arrows show changes
- Portfolio values update automatically

## 🎮 How It Works

1. **Random Fluctuation**: Each stock moves ±2% randomly
2. **Continuous Updates**: Runs in background every 30 seconds
3. **Safe Boundaries**: Prices never go below $0.01
4. **History Tracking**: Previous close is saved for change calculation

## 💡 Tips

### During Development:
```bash
# Fast updates for testing (every 5 seconds)
python manage.py update_stock_prices --continuous --interval 5
```

### During Competition:
```bash
# Realistic updates (every 30 seconds)
./start_price_updater.sh
```

### In Production:
```bash
# Run in background (keeps running even if terminal closes)
nohup python manage.py update_stock_prices --continuous > prices.log 2>&1 &

# Check if running
ps aux | grep update_stock_prices

# Stop it
pkill -f update_stock_prices
```

## 🛠️ What Changed

### New Files:
- `app1/management/commands/update_stock_prices.py` - Main updater command
- `start_price_updater.sh` - Helper script for realistic mode
- `demo_price_updates.sh` - Demo script with fast updates
- `AUTO_PRICE_UPDATES.md` - Full documentation

### Modified Files:
- `app1/models.py` - Added `update_price_random()` method to Stock model
- `app1/admin.py` - Added "Apply random fluctuation" action

## 🎯 Try It Now!

### Terminal 1: Start the server
```bash
source venv/bin/activate
python manage.py runserver
```

### Terminal 2: Start price updates
```bash
./demo_price_updates.sh
```

### Browser:
- Open: `http://127.0.0.1:8000/team/stocks`
- Watch prices change every 5 seconds!
- Refresh to see updates

## 🔥 Demo Script

Want to show it off? Run this:
```bash
# Terminal 1
python manage.py runserver

# Terminal 2
./demo_price_updates.sh

# Browser
# Open /team/stocks and keep refreshing
```

## 📊 Features

✅ Automatic price updates  
✅ Random fluctuations (±2%)  
✅ Continuous or single update  
✅ Customizable interval  
✅ Customizable volatility  
✅ Admin panel integration  
✅ Real-time market simulation  
✅ Gainers/losers tracking  
✅ Color-coded changes  

## 🎉 Next Steps

1. **Test locally**: Run `./demo_price_updates.sh`
2. **Fix production DB**: Run the `COMPLETE_FIX.sql` in Neon console
3. **Deploy**: Push to production
4. **Enable auto-updates**: Run updater script on production server

Need help? Check `AUTO_PRICE_UPDATES.md` for full docs!
