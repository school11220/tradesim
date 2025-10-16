# 🚨 TROUBLESHOOTING GUIDE - "Still Not Working"

## ⚠️ FIRST - Tell Me EXACTLY What's Not Working

Before I can help, I need to know:

### 1. Did you run the SQL script?
- [ ] YES - I ran PRODUCTION_FIX_V2.sql in Neon console
- [ ] NO - I haven't run it yet
- [ ] TRIED - I got an error when running it

### 2. What page is giving errors?
- [ ] `/admin/app1/stock/` - Error: _________________________
- [ ] `/admin/app1/simulatorsettings/` - Error: _________________________
- [ ] `/admin/app1/event/` - Error: _________________________
- [ ] `/team/stocks` - Error: _________________________
- [ ] `/team/portfolio` - Error: _________________________
- [ ] Something else: _________________________

### 3. What does the error say?
Copy the EXACT error message here:
```
(paste error here)
```

---

## 🔍 STEP-BY-STEP DIAGNOSTIC

### **Option 1: You HAVEN'T run the SQL yet**

**DO THIS NOW:**
1. Open Neon: https://console.neon.tech/
2. Go to SQL Editor
3. Copy ALL of `PRODUCTION_FIX_V2.sql`
4. Paste and run it
5. Come back and tell me what happened

---

### **Option 2: You RAN the SQL but still getting errors**

**Run the DIAGNOSTIC.sql to see what's in your database:**

1. Open Neon SQL Editor
2. Copy ALL of `DIAGNOSTIC.sql`
3. Run it
4. Take a screenshot of the results
5. Share what you see

This will show me:
- What tables exist
- What columns are in each table
- How many rows of data exist
- What the actual data looks like

---

### **Option 3: SQL gave you an error**

**Tell me what error you got when running the SQL:**
- Syntax error?
- Permission denied?
- Table doesn't exist?
- Something else?

---

## 🎯 COMMON ISSUES & FIXES

### Issue: "Column does not exist"

**Diagnosis:**
```sql
-- Run this in Neon:
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'app1_stock';
```

**Expected columns for app1_stock:**
- symbol, name, sector, current_price, previous_close
- is_active, last_updated, created_at

**If missing:** Run PRODUCTION_FIX_V2.sql

---

### Issue: "No stocks showing"

**Diagnosis:**
```sql
-- Run this in Neon:
SELECT COUNT(*) FROM app1_stock;
```

**Expected:** Should return 25

**If 0:** The INSERT statements didn't run. Try running just the stock inserts manually.

---

### Issue: "Portfolio showing nothing"

**This is NORMAL if:**
- You haven't created a team yet
- You haven't made any trades

**To test:**
1. Go to `/team/signup` - Create team
2. Login at `/team/login`
3. Go to `/team/stocks` - Should see stocks
4. Click a stock → Buy some shares
5. Go to `/team/portfolio` - NOW you'll see values

---

### Issue: "ValueError at /admin/app1/stock/"

**This was the format string issue - should be fixed in latest deployment**

**Verify:**
```bash
# Check if you're on latest version
git log --oneline -1
# Should show: "Fix admin action descriptions..."
```

**If not latest:**
```bash
git pull origin main
vercel --prod
```

---

## 🔧 DETAILED DEBUGGING STEPS

### Step 1: Check Database Schema

Run `DIAGNOSTIC.sql` and verify:

**app1_event should have:**
- allow_short_selling (boolean)
- max_trades_per_team (integer)
- trading_fee_percentage (numeric)

**app1_stock should have:**
- sector (varchar)
- created_at (timestamp)

**app1_simulatorsettings should have:**
- setting_name (NOT setting_key)
- setting_value
- description

---

### Step 2: Check Data Exists

```sql
-- Should all return numbers, not 0
SELECT COUNT(*) FROM app1_event;      -- Should be >= 1
SELECT COUNT(*) FROM app1_simulatorsettings;  -- Should be >= 2
SELECT COUNT(*) FROM app1_stock;      -- Should be >= 25
```

---

### Step 3: Test Specific Pages

Try each URL and note EXACT error:

1. **Admin Login**: `/admin/`
   - Can you login? YES / NO
   - Error: _______________

2. **Stocks Page**: `/admin/app1/stock/`
   - Does it load? YES / NO
   - Error: _______________

3. **Settings Page**: `/admin/app1/simulatorsettings/`
   - Does it load? YES / NO
   - Error: _______________

4. **Team Stocks**: `/team/stocks`
   - After creating team and logging in
   - Do you see stocks? YES / NO
   - How many? _______________

---

## 📸 WHAT I NEED FROM YOU

To help you, please provide:

1. **Screenshot** of the error page
2. **Result** of running DIAGNOSTIC.sql
3. **Confirmation** that you ran PRODUCTION_FIX_V2.sql
4. **Exact URL** that's giving problems
5. **Exact error message** (full text)

---

## 🎯 MOST LIKELY ISSUES

### 90% Chance:
- You haven't run PRODUCTION_FIX_V2.sql in Neon yet

### 9% Chance:
- SQL ran but had errors you didn't notice
- Tables exist but data wasn't inserted

### 1% Chance:
- There's a new code issue we need to fix

---

## ⚡ QUICK FIX CHECKLIST

Run these commands in Neon SQL Editor:

```sql
-- 1. Check Event table
SELECT * FROM app1_event LIMIT 1;

-- 2. Check Settings table  
SELECT * FROM app1_simulatorsettings;

-- 3. Check Stock table
SELECT * FROM app1_stock LIMIT 5;

-- 4. Check column exists
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'app1_stock' AND column_name = 'sector';
```

**What to expect:**
- Query 1: Should return 1 event
- Query 2: Should return 2 settings
- Query 3: Should return 5 stocks
- Query 4: Should return "sector"

**If any fail:** That's the problem! Tell me which one.

---

## 💬 TELL ME:

1. **What specific page URL is not working?**
2. **What is the EXACT error message?**
3. **Did you run PRODUCTION_FIX_V2.sql? (YES/NO)**
4. **What did DIAGNOSTIC.sql show?**

**I can't fix "not working" without knowing what's actually broken!** 😊

Copy the error messages and paste them so I can see exactly what's happening.
