# 📋 Admin Control Cheat Sheet

## 🎯 Quick Actions

### Change a Stock Price
```
1. Go to: http://127.0.0.1:8000/admin/app1/stock/
2. Click stock name (e.g., "AAPL - $178.50")
3. Change "Current price" field
4. Click "Save"
5. Done! Users see new price instantly
```

### Simulate Market Crash (All Stocks)
```
1. Go to: http://127.0.0.1:8000/admin/app1/stock/
2. Check "select all" checkbox at top
3. Select "Decrease price by 10%" from Actions dropdown
4. Click "Go"
5. Crash complete!
```

### Give User Bonus Money
```
1. Go to: http://127.0.0.1:8000/admin/app1/users/
2. Find user and check checkbox
3. Select "Add $5,000 bonus" from Actions dropdown
4. Click "Go"
5. User gets $5,000!
```

### Change Starting Balance for All New Users
```
1. Go to: http://127.0.0.1:8000/admin/app1/simulatorsettings/
2. Click "default_user_balance"
3. Change "Setting value" (e.g., "25000" for $25k)
4. Click "Save"
5. All new signups get this amount!
```

### Add a New Stock
```
1. Go to: http://127.0.0.1:8000/admin/app1/stock/
2. Click "Add Stock" button (top right)
3. Fill in:
   - Symbol: SYMBOL
   - Name: Company Name
   - Current price: 100.00
   - Previous close: 98.00
   - Is active: ✓ (checked)
4. Click "Save"
5. Stock is now tradeable!
```

### Reset All User Balances
```
1. Go to: http://127.0.0.1:8000/admin/app1/users/
2. Check "select all" checkbox
3. Select "Reset balance to default" from Actions
4. Click "Go"
5. Everyone back to $10,000!
```

### Disable Trading on a Stock
```
1. Go to: http://127.0.0.1:8000/admin/app1/stock/
2. Find the stock
3. Uncheck "Is active" checkbox
4. Stock disappears from trading!
```

## 📊 Current Stock Prices

After running `init_simulator`, you have these stocks:

| Symbol | Company | Initial Price | Previous Close |
|--------|---------|---------------|----------------|
| AAPL | Apple Inc. | $178.50 | $175.20 |
| MSFT | Microsoft Corporation | $380.75 | $378.90 |
| GOOG | Alphabet Inc. | $139.25 | $138.00 |
| META | Meta Platforms Inc. | $325.40 | $322.10 |
| AMZN | Amazon.com Inc. | $143.90 | $142.50 |
| TSLA | Tesla Inc. | $242.30 | $238.75 |
| NVDA | NVIDIA Corporation | $495.20 | $485.30 |
| NFLX | Netflix Inc. | $445.60 | $442.00 |
| SONY | Sony Group Corporation | $92.15 | $91.80 |
| DIS | The Walt Disney Company | $91.25 | $90.50 |

## 🎮 Scenario Examples

### Scenario 1: Tech Stock Boom
```
Goal: Simulate tech stocks rising

1. Admin → Stocks
2. Select: AAPL, MSFT, GOOG, META, NVDA
3. Action: "Increase price by 10%"
4. Result: Tech stocks up 10%!
```

### Scenario 2: Netflix Crisis
```
Goal: Simulate NFLX dropping due to bad earnings

1. Admin → Stocks → NFLX
2. Change current price from 445.60 to 380.00
3. Save
4. Result: NFLX down 14.7%!
```

### Scenario 3: Reward Top Traders
```
Goal: Give bonus to users with > $15,000 balance

1. Admin → Users
2. Click "Balance" column to sort (high to low)
3. Select users with $15k+
4. Action: "Add $1,000 bonus"
5. Result: Top traders rewarded!
```

### Scenario 4: Weekly Reset
```
Goal: Start fresh week with equal balances

1. Admin → Users → Select all
2. Action: "Reset balance to default"
3. Result: Everyone back to $10,000!
```

### Scenario 5: Custom Tournament
```
Goal: Create a 1-week trading competition

Day 1:
1. Reset all balances to $10,000
2. Announce competition

During Week:
1. Change stock prices to simulate real events
2. Create volatility

Day 7:
1. Admin → Users → Sort by balance
2. Winner = highest balance!
3. Bonus winner with "Add $5,000 bonus"
```

## 🔑 URLs to Remember

| Page | URL | Purpose |
|------|-----|---------|
| Admin Login | http://127.0.0.1:8000/admin/ | Control panel |
| Manage Stocks | http://127.0.0.1:8000/admin/app1/stock/ | Change prices |
| Manage Users | http://127.0.0.1:8000/admin/app1/users/ | View balances |
| Settings | http://127.0.0.1:8000/admin/app1/simulatorsettings/ | Global config |
| User Dashboard | http://127.0.0.1:8000/dashboard | User view |
| User Signup | http://127.0.0.1:8000/signup | New accounts |

## 🎨 Admin Panel Features

### Stock Admin Features
- ✅ Edit prices directly
- ✅ Color-coded price changes (green ↑, red ↓)
- ✅ Last updated timestamp
- ✅ Active/inactive toggle
- ✅ Bulk price adjustments
- ✅ Search by symbol/name

### User Admin Features
- ✅ View all balances
- ✅ Color-coded balances (green > $10k, orange > $5k, red < $5k)
- ✅ See holdings in JSON
- ✅ Edit balance directly
- ✅ Bulk balance operations
- ✅ Search by username/email

### Settings Features
- ✅ Default starting balance
- ✅ Trading fee percentage
- ✅ Add custom settings
- ✅ Last updated tracking

## 💡 Pro Tips

1. **Test price changes** on one stock first before bulk operations
2. **Keep previous_close updated** - use "Set previous close = current price" to reset changes
3. **Monitor user balances** - see who's making money!
4. **Create volatility** - alternate price increases/decreases for realism
5. **Backup database** before major changes - `cp db.sqlite3 db.backup`
6. **Use color coding** - admin uses colors to show at-a-glance status

## 🔧 Command Line Price Control

For advanced users, control via Django shell:

```bash
/home/shivam/Investa/venv/bin/python manage.py shell
```

```python
from app1.models import Stock

# Crash the market (all stocks down 20%)
for stock in Stock.objects.all():
    stock.current_price *= 0.8
    stock.save()

# Bull run (all stocks up 15%)
for stock in Stock.objects.all():
    stock.current_price *= 1.15
    stock.save()

# Set specific stock price
aapl = Stock.objects.get(symbol='AAPL')
aapl.current_price = 200.00
aapl.save()

# Random volatility
import random
for stock in Stock.objects.all():
    change = random.uniform(0.95, 1.05)  # ±5%
    stock.current_price *= change
    stock.save()
```

## 📞 Quick Reference

**Create Admin:**
```bash
/home/shivam/Investa/venv/bin/python manage.py createsuperuser
```

**Reset Database:**
```bash
rm db.sqlite3
/home/shivam/Investa/venv/bin/python manage.py migrate
/home/shivam/Investa/venv/bin/python manage.py init_simulator
/home/shivam/Investa/venv/bin/python manage.py createsuperuser
```

**Start Server:**
```bash
/home/shivam/Investa/venv/bin/python manage.py runserver
```

---

**🎉 Now go control the market!**
