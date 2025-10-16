# 🚀 Database Initialization Guide

## ⚠️ IMPORTANT: You MUST initialize the database before using the app!

The app will show errors if the database doesn't have stocks. Follow these steps:

## Option 1: Using Management Command (Recommended)

Run this command on your Vercel deployment or local environment:

```bash
python manage.py init_competition_stocks
```

This will create all 63 stocks in the database.

## Option 2: Using Django Shell

1. Open Django shell:
```bash
python manage.py shell
```

2. Run the initialization:
```python
exec(open('init_db.py').read())
```

## Option 3: Using Admin Panel

1. Go to `/admin` and login
2. Navigate to **Stocks** → **Add Stock**
3. Manually add stocks one by one with:
   - Symbol (e.g., AAPL)
   - Name (e.g., Apple Inc.)
   - Current Price (e.g., 150.00)
   - Previous Close (e.g., 150.00)
   - Is Active (checked)

## Option 4: Quick Setup Script

Run this in your terminal where manage.py is located:

```bash
python init_db.py
```

## What Gets Created:

### 1. Stocks (63 total)
- **Technology**: AAPL, MSFT, GOOG, META, AMZN, TSLA, NVDA, ORCL, INTC, AMD, CRM, ADBE, CSCO, IBM, NFLX
- **Finance**: JPM, BAC, WFC, GS, MS, V, MA, AXP, BLK, SCHW
- **Healthcare**: JNJ, PFE, UNH, ABBV, TMO, MRK, ABT, BMY, LLY, AMGN
- **Energy**: XOM, CVX, COP, SLB, EOG, MPC, PSX
- **Consumer**: WMT, HD, MCD, NKE, SBUX, TGT, LOW, TJX, DG, COST
- **Industrial**: BA, CAT, GE, UPS, HON
- **Telecom**: VZ, T, TMUS
- **Entertainment**: DIS, SONY, CMCSA

All stocks start at $100.00 per share.

### 2. Simulator Settings
- Default user balance: $10,000

### 3. Default Event
- Name: "Default Trading Competition"
- Duration: 30 days
- Initial capital: $100,000 per team
- Registration: Open
- Status: Inactive (you can activate it in admin)

## Verifying Initialization

After running initialization, check:

1. **Admin Panel**: `/admin/app1/stock/` should show 63 stocks
2. **Dashboard**: Should load without errors
3. **Stock Details**: Should be able to view individual stocks

## Troubleshooting

### Error: "Stock has no field named 'current_price_display'"
**Solution**: This error is now fixed in the latest deployment. The admin panel has error handling.

### Error: "No stocks available"
**Solution**: Run the initialization command/script as shown above.

### Error: "Database connection failed"
**Solution**: Check your DATABASE_URL environment variable is set correctly.

### Error: "Table doesn't exist"
**Solution**: Run migrations first:
```bash
python manage.py migrate
```

## Post-Initialization Steps

1. **Create Superuser** (if not already created):
```bash
python manage.py createsuperuser
```

2. **Access Admin Panel**:
- Go to `/admin`
- Login with superuser credentials

3. **Activate Event**:
- Go to Events in admin
- Select your event
- Choose "▶️ START selected events"

4. **Test the System**:
- Create a test user account
- Try buying/selling stocks
- Check dashboard displays correctly

## For Vercel Deployment

Since Vercel is serverless, you need to initialize the production database:

### Method 1: Using Vercel CLI
```bash
vercel exec python manage.py init_competition_stocks
```

### Method 2: Via Shell Script
Create `init_vercel.sh`:
```bash
#!/bin/bash
python manage.py migrate
python manage.py init_competition_stocks
```

### Method 3: One-time Admin Script
Access your database directly (Neon/Postgres) and run SQL to insert stocks.

## Current Status

As of the latest deployment:
- ✅ Admin panel errors fixed
- ✅ Error handling added
- ✅ Display methods protected
- ⚠️ **Database needs initialization**

---

**Bottom Line**: The app code is working, but you need to populate the database with stocks for it to function properly!
