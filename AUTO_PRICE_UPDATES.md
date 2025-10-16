# 📊 Automatic Stock Price Updates

This feature simulates real-world stock market behavior by automatically updating stock prices with random fluctuations.

## 🎯 Features

- **Random Price Fluctuation**: Stocks move up/down by ±2% by default
- **Continuous Updates**: Prices update every 30 seconds (configurable)
- **Market Simulation**: Realistic price movements with volatility
- **Admin Controls**: Manual price updates via admin panel
- **Safe Boundaries**: Prices never go below $0.01

## 🚀 Usage Methods

### Method 1: Automatic Updates (Background Process)

Run this to continuously update prices every 30 seconds:

```bash
# Using the helper script
./start_price_updater.sh

# Or directly with manage.py
python manage.py update_stock_prices --continuous
```

**Custom interval:**
```bash
# Update every 10 seconds
python manage.py update_stock_prices --continuous --interval 10

# Update every 60 seconds (1 minute)
python manage.py update_stock_prices --continuous --interval 60
```

**Custom volatility:**
```bash
# More volatile (±5% changes)
python manage.py update_stock_prices --continuous --volatility 0.05

# Less volatile (±1% changes)
python manage.py update_stock_prices --continuous --volatility 0.01
```

### Method 2: Single Update

Update prices once without looping:

```bash
python manage.py update_stock_prices
```

### Method 3: Admin Panel

1. Go to **Django Admin** → **Stocks**
2. Select stocks you want to update
3. Choose **"📊 Apply random fluctuation (±2%)"** from Actions dropdown
4. Click "Go"

## 🎮 How It Works

1. **Random Change**: Each stock gets a random price change between -2% and +2%
2. **Price Update**: New price = Current price × (1 + random change)
3. **History Tracking**: Previous price is saved before update
4. **Display**: Shows gainers/losers and percentage changes

## 📈 Example Output

```
📊 Update #1 at 14:35:22
   Updating 63 stocks...

   AAPL   $150.50 → $152.30  +$1.80 (+1.20%)
   GOOGL  $125.80 → $124.50  -$1.30 (-1.03%)
   TSLA   $242.85 → $247.10  +$4.25 (+1.75%)
   ...

   📈 Gainers: 35
      Top: NVDA +1.98%
   📉 Losers: 28
      Top: META -1.87%
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔧 Configuration

Edit `app1/models.py` Stock model:

```python
# Default volatility in update_price_random method
def update_price_random(self, volatility=0.02):  # ±2%
    # Change this value to adjust default volatility
```

## 💡 Tips

### For Development
```bash
# Quick volatile changes for testing
python manage.py update_stock_prices --continuous --interval 5 --volatility 0.05
```

### For Production
```bash
# Realistic market simulation
python manage.py update_stock_prices --continuous --interval 30 --volatility 0.02
```

### Running in Background
```bash
# Linux/Mac - run in background
nohup python manage.py update_stock_prices --continuous &

# Check if running
ps aux | grep update_stock_prices

# Stop it
pkill -f update_stock_prices
```

## 🎯 Best Practices

1. **Start updater before competition**: Let prices fluctuate naturally
2. **Monitor volatility**: Adjust based on competition duration
3. **Use tmux/screen**: Keep updater running even if terminal closes
4. **Log output**: Redirect to file for monitoring

```bash
# Run with logging
python manage.py update_stock_prices --continuous > price_updates.log 2>&1 &
```

## 🛑 Stopping the Updater

Press `Ctrl+C` in the terminal where it's running, or:

```bash
# Find and kill the process
pkill -f update_stock_prices
```

## 🎨 Integration with Team Dashboard

Stock prices on the team dashboard will automatically reflect the latest values when they refresh the page. No additional code needed!

## 🔮 Future Enhancements

- Sector-specific volatility (tech stocks more volatile)
- Market hours (trading only during certain times)
- News events that trigger price spikes
- Volume-based price changes
- Circuit breakers for extreme moves
