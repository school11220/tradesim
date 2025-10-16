# 🔧 PRODUCTION FIX GUIDE - Complete Solution

## 🚨 Root Cause Analysis

Your production is failing because:
1. ✅ **Code is deployed** (latest version on Vercel)
2. ❌ **Database is NOT initialized** (missing columns, no data)
3. ❌ **Migrations weren't run** on production database

---

## ✅ THE FIX (Do This NOW)

### **Step 1: Run Database Fix Script** ⚠️ CRITICAL

1. Open Neon Dashboard: https://console.neon.tech/
2. Select your database
3. Click "SQL Editor"
4. **Copy and paste the ENTIRE `PRODUCTION_FIX_V2.sql` file**
5. Click "Run" or press Ctrl+Enter
6. Wait for "Database setup complete!" message

---

### **Step 2: Verify It Worked**

Run this in Neon SQL Editor:

```sql
-- Should return 1 (one event)
SELECT COUNT(*) FROM app1_event;

-- Should return 2 (two settings)
SELECT COUNT(*) FROM app1_simulatorsettings;

-- Should return 25+ (stocks)
SELECT COUNT(*) FROM app1_stock;
```

If all three queries return numbers (not errors), **YOU'RE FIXED!** ✅

---

### **Step 3: Test Admin Pages**

Go to your production URL and test:

1. `/admin/` - Login
2. `/admin/app1/stock/` - Should show stocks ✅
3. `/admin/app1/simulatorsettings/` - Should show settings ✅
4. `/admin/app1/event/` - Should show event ✅

---

## 🎯 Why This Fixes Everything

The SQL script:
- ✅ Adds missing columns (`allow_short_selling`, `sector`, `created_at`, etc.)
- ✅ Creates initial event (required for teams)
- ✅ Creates settings (required for admin)
- ✅ Adds 25 stocks (can add more later)
- ✅ Safe to run multiple times (uses WHERE NOT EXISTS)

---

## 📊 After The Fix

### Portfolio Values Will Update When:
1. Teams create accounts at `/team/signup`
2. Teams make trades (buy/sell stocks)
3. The `portfolio` JSON field gets populated

### To Test:
```bash
# Create a test team
1. Go to /team/signup
2. Fill in: Team Name, Email, Code, Password
3. Login at /team/login
4. Go to /team/stocks - You should see 25 stocks!
5. Click "Trade" on any stock
6. Buy some shares
7. Go to /team/portfolio - Should show your holdings!
```

---

## 🐛 If Problems Persist

### "Still getting errors"
**Check which error:**
- Column doesn't exist → Rerun SQL script
- No stocks showing → Check stock count in SQL
- Can't login → Check if event exists

### "Portfolio not showing values"
**Normal!** Portfolio is empty until you trade. After buying stocks:
```sql
-- Check if trade worked
SELECT balance, portfolio::text, total_trades 
FROM app1_team 
WHERE team_code = 'YOUR_CODE';
```

### "Values not changing"
The values change when:
1. Admin updates stock prices (manual)
2. Price updater runs (automatic - needs to be started)
3. Page is refreshed

---

## 🚀 Enable Auto Price Updates (Optional)

After everything works, enable live price fluctuation:

**If you have SSH access to production:**
```bash
python manage.py update_stock_prices --continuous &
```

**If using Vercel** (no background processes):
- Use a cron job service
- Or manually update prices via admin panel
- Or use a separate worker dyno (Heroku) / service

---

## ✨ Summary

**CRITICAL STEP**: Run `PRODUCTION_FIX_V2.sql` in Neon → This fixes 90% of issues

**Then test**: Admin pages, team signup, stock trading, portfolio

**If stuck**: Check the exact error message and compare to this guide

---

**START WITH THE SQL SCRIPT. Everything else depends on it working!** 🎯
