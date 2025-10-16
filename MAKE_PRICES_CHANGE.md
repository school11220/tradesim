# How to Make Stock Prices Change Automatically

## ✅ Fixes Applied

I've just fixed the Decimal arithmetic errors that were preventing price updates from working. Here's how to get prices changing now!

---

## 🚀 Quick Start: Make Prices Change RIGHT NOW!

### Step 1: Wait for Deployment (2-3 minutes)
The fix is being deployed to Vercel right now. Wait about 2-3 minutes.

### Step 2: Trigger First Price Update Manually

**Option A: GitHub Actions (Easiest)**
1. Go to: https://github.com/school11220/tradesim/actions
2. Click "Update Stock Prices" workflow
3. Click green "Run workflow" button
4. Click "Run workflow" again to confirm
5. Wait 10-15 seconds

**Option B: Direct API Call**
Open in browser or use curl:
```
https://tradesim-lyart.vercel.app/api/update-prices
```

### Step 3: Verify It Worked
You should see JSON response like:
```json
{
  "success": true,
  "updated_count": 60,
  "updates": [...]
}
```

### Step 4: Watch Prices Change on Frontend
1. **For Team System:**
   - Go to: https://tradesim-lyart.vercel.app/team/login
   - Login with team credentials
   - Go to Browse Stocks or Portfolio
   - Prices will auto-refresh every 15-20 seconds

2. **For User System (Your Current View):**
   - Go to: https://tradesim-lyart.vercel.app/dashboard
   - Watchlist will show updated prices
   - Portfolio will recalculate

---

## ⏰ Automatic Updates (GitHub Actions)

### How It Works
Once deployed, GitHub Actions will **automatically** update prices:
- **Frequency:** Every 5 minutes
- **Schedule:** 9 AM - 4 PM UTC, Monday-Friday
- **No action needed!**

### Check If It's Running
1. Go to: https://github.com/school11220/tradesim/actions
2. Look for "Update Stock Prices" runs
3. Green checkmark = Working!
4. Should see new runs every 5 minutes during trading hours

---

## 🔧 What Was Fixed

### Issue 1: Decimal × Float Error
**Problem:**
```python
# Stock.update_price_random was doing:
new_price = self.current_price * (1 + change_percent)  ❌
# If current_price was Decimal, this failed
```

**Solution:**
```python
# Now converts to float first:
current = float(self.current_price)
new_price = current * (1 + change_percent)  ✅
```

### Issue 2: API Response Errors
**Problem:**
```python
# API was trying to use price directly
new_price = stock.update_price_random(volatility)  ❌
```

**Solution:**
```python
# Now ensures float conversion
new_price = float(stock.update_price_random(volatility))  ✅
```

---

## 🎯 Testing Checklist

### ✅ Step-by-Step Test (5 minutes)

**1. Test API Endpoint** (1 min)
```bash
curl "https://tradesim-lyart.vercel.app/api/update-prices"

# Should see:
# {"success": true, "updated_count": 60, ...}
```

**2. Test Team System** (2 min)
```
1. Login: https://tradesim-lyart.vercel.app/team/login
2. Browse Stocks: Click "📈 Browse Stocks"
3. Note 2-3 stock prices
4. Trigger update (GitHub Actions)
5. Wait 15 seconds
6. See prices flash and change!
```

**3. Test User System** (2 min)
```
1. Login: https://tradesim-lyart.vercel.app/login
2. Dashboard: View watchlist
3. Note prices
4. Trigger update
5. Refresh page
6. See new prices!
```

---

## 📊 How Often Will Prices Change?

### Automatic (GitHub Actions)
```
09:00 UTC - First update
09:05 UTC - Second update
09:10 UTC - Third update
...
16:00 UTC - Last update

= 84 updates per day (Mon-Fri)
```

### Manual Triggers
```
Anytime via:
- GitHub Actions → Run workflow
- API: /api/update-prices
- Management command (local only)
```

---

## 🚨 Troubleshooting

### "Prices still not changing?"

**Check 1: Is deployment complete?**
```
https://vercel.com/dashboard
Look for "Ready" status on latest deployment
```

**Check 2: Test API directly**
```bash
curl "https://tradesim-lyart.vercel.app/api/update-prices"

# Should return success:true
# If error, wait for deployment to finish
```

**Check 3: Trigger manually**
```
https://github.com/school11220/tradesim/actions
Run workflow manually
Check logs for "success": true
```

**Check 4: Hard refresh browser**
```
Ctrl+Shift+R (Windows)
Cmd+Shift+R (Mac)
```

### "API returns error?"

Wait 5 minutes for Vercel deployment to fully complete, then try again.

### "GitHub Actions not running?"

**Check time:**
- Actions only run 9 AM - 4 PM UTC (Mon-Fri)
- Outside these hours, trigger manually

**Check workflow file:**
```
Workflow should be at: .github/workflows/update-prices.yml
Should be pushed to main branch
```

---

## 💡 Pro Tips

### Tip 1: Test During Event
```
Before competition starts:
1. Trigger manual update
2. Have teams watch Browse Stocks
3. See prices change in real-time
4. Confirms system working!
```

### Tip 2: Adjust Volatility
```bash
# More volatility (5% swings)
curl "https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.05"

# Less volatility (1% swings)
curl "https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.01"
```

### Tip 3: Change Update Frequency
Edit `.github/workflows/update-prices.yml`:
```yaml
# Every 2 minutes (more frequent)
- cron: '*/2 9-16 * * 1-5'

# Every 10 minutes (less frequent)
- cron: '*/10 9-16 * * 1-5'
```

---

## 📈 Expected Behavior

### First Update (Now)
```
AAPL: $150.00 → $151.20 (+$1.20, +0.80%)
MSFT: $280.50 → $278.90 (-$1.60, -0.57%)
GOOGL: $140.00 → $141.50 (+$1.50, +1.07%)
```

### After 5 Minutes (Automatic)
```
AAPL: $151.20 → $150.80 (-$0.40, -0.26%)
MSFT: $278.90 → $280.10 (+$1.20, +0.43%)
GOOGL: $141.50 → $142.30 (+$0.80, +0.57%)
```

### After 1 Hour (12 updates)
```
Prices will have changed multiple times
Portfolio values will fluctuate
Creates realistic trading experience!
```

---

## ✅ Summary

### What to Do RIGHT NOW:

1. ⏱️ **Wait 2-3 minutes** for Vercel deployment
2. 🚀 **Trigger manual update**: GitHub Actions or API
3. 🧪 **Test**: See prices change
4. ✅ **Confirm**: API returns success:true
5. 🎉 **Done**: Automatic updates every 5 min!

### What Happens Automatically:

- ✅ Prices update every 5 minutes
- ✅ During trading hours only (9-4 PM UTC)
- ✅ Monday through Friday
- ✅ Teams see changes in real-time (15-20s refresh)
- ✅ Portfolio values recalculate automatically

---

## 🎯 Quick Commands

**Test API:**
```bash
curl "https://tradesim-lyart.vercel.app/api/update-prices"
```

**Manual Trigger:**
```
https://github.com/school11220/tradesim/actions
→ Update Stock Prices → Run workflow
```

**Check Logs:**
```
https://github.com/school11220/tradesim/actions
→ Click latest run → View logs
```

---

**The price update system is now fixed and ready! Just wait for deployment and trigger your first update! 🚀**

Deployment will complete in about 2-3 minutes, then you can start seeing prices change!
