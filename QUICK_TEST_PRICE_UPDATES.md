# Quick Start: Test Price Updates Right Now!

## 🚀 Immediate Testing (2 minutes)

### Step 1: Manual Trigger (Choose One)

**Option A: GitHub Actions** (Recommended)
1. Go to: https://github.com/school11220/tradesim/actions
2. Click "Update Stock Prices" workflow
3. Click "Run workflow" button (green)
4. Click "Run workflow" again to confirm
5. Wait 10-15 seconds for completion

**Option B: Direct API Call**
```bash
curl "https://tradesim-lyart.vercel.app/api/update-prices"
```

Or open in browser:
```
https://tradesim-lyart.vercel.app/api/update-prices
```

### Step 2: Watch It Work!
1. **Login to TradeSim**: https://tradesim-lyart.vercel.app/team/login
2. **Go to Browse Stocks**: Click "📈 Browse Stocks"
3. **Note some prices**: Write down 2-3 stock prices
4. **Trigger update**: Use Option A or B above
5. **Wait 15 seconds**: Let auto-refresh cycle complete
6. **See changes!**: Prices should flash green/red and update

---

## ⏰ Automatic Updates

Once deployed (2-3 minutes from your last push):

### During Trading Hours (9 AM - 4 PM UTC, Mon-Fri)
- ✅ Updates happen **every 5 minutes automatically**
- ✅ No action needed from you!
- ✅ Check GitHub Actions to see them running

### Outside Trading Hours
- 📅 Workflow pauses (weekends, evenings)
- 🔧 Use manual trigger to test anytime
- 📊 Or call API endpoint directly

---

## 🎯 What You'll See

### Before Price Update
```
AAPL: $150.25  ▲ $2.50
MSFT: $280.75  ▼ -$1.25
GOOGL: $140.00  ▲ $0.75
```

### After Price Update (15s later)
```
AAPL: $151.50  ▲ $1.25  [GREEN FLASH!]
MSFT: $279.50  ▼ -$1.25  [RED FLASH!]
GOOGL: $141.10  ▲ $1.10  [GREEN FLASH!]
```

### Portfolio Updates Too!
```
Before: Portfolio Value: $100,523.50
After:  Portfolio Value: $101,234.75  [+$711.25]
```

---

## 🔍 Verify It's Working

### Check 1: GitHub Actions
```
https://github.com/school11220/tradesim/actions

✅ Green checkmark = Success
❌ Red X = Check logs
🟡 Yellow spinner = Running
```

### Check 2: API Response
```bash
curl "https://tradesim-lyart.vercel.app/api/update-prices"

# Should see:
{
  "success": true,
  "updated_count": 60,
  "updates": [...]
}
```

### Check 3: Frontend
```
1. Browse Stocks page
2. Portfolio page
3. Dashboard

All should show updated prices within 15-20 seconds
```

---

## 📊 First 5 Minutes After Deployment

**Minute 0:** Push deployed to Vercel
**Minute 1:** Vercel build completes
**Minute 2:** API endpoint is live
**Minute 3:** GitHub Actions enables workflow
**Minute 4:** Wait for next 5-minute interval
**Minute 5:** First automatic update runs! 🎉

**Or skip waiting:** Trigger manually via GitHub Actions!

---

## 🎮 Test Scenario

### Full Test (5 minutes):

1. **Login to team account** (30 seconds)
   ```
   https://tradesim-lyart.vercel.app/team/login
   ```

2. **Browse Stocks - Note Prices** (30 seconds)
   ```
   Write down 3 stock prices
   Example: AAPL $150.25, MSFT $280.75, GOOGL $140.00
   ```

3. **Trigger Manual Update** (30 seconds)
   ```
   GitHub Actions → Update Stock Prices → Run workflow
   ```

4. **Wait for Auto-Refresh** (20 seconds)
   ```
   Count to 20, or watch for flash animations
   ```

5. **See Price Changes!** (10 seconds)
   ```
   Prices should be different!
   Flash animations should appear!
   ```

6. **Check Portfolio** (1 minute)
   ```
   Go to Portfolio page
   Your portfolio value should be recalculated
   ```

7. **Trigger Again** (1 minute)
   ```
   Run another update
   Wait 20 seconds
   See portfolio value change again!
   ```

8. **Success!** 🎉
   ```
   Prices are updating!
   Frontend is refreshing!
   System is working!
   ```

---

## 🚨 Quick Troubleshoot

### "No changes visible?"
✅ Wait 15-20 seconds for auto-refresh
✅ Click manual "Refresh" button
✅ Hard refresh browser (Ctrl+Shift+R)

### "API returns error?"
✅ Check Vercel deployment finished
✅ Verify database connection
✅ Check if stocks exist in database

### "GitHub Actions not running?"
✅ Check it's a weekday 9-4 PM UTC
✅ Or trigger manually
✅ Check workflow file was pushed

---

## 🎯 Expected Results

### Immediate (After Manual Trigger)
- ✅ API returns success
- ✅ 60 stocks updated
- ✅ Changes logged

### Within 15-20 Seconds
- ✅ Browse Stocks shows new prices
- ✅ Flash animations appear
- ✅ Price change values update

### Within 1 Minute
- ✅ Portfolio recalculates
- ✅ P&L values change
- ✅ Dashboard updates

### Ongoing (Every 5 Minutes)
- ✅ Automatic updates
- ✅ Continuous price changes
- ✅ Real trading simulation

---

**Go ahead and test it now! The system is deployed and ready! 🚀**
