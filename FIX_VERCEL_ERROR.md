# 🔧 Fixing Vercel Deployment Crash

## 🚨 Current Issue

**Error:** `500: INTERNAL_SERVER_ERROR`
**Code:** `FUNCTION_INVOCATION_FAILED`

This means your Django app is crashing on Vercel. Most likely causes:
1. Database migrations not run
2. Database connection issue
3. Missing environment variables
4. Static files issue

---

## 🔍 Step 1: Check Vercel Logs

First, let's see the actual error:

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com/dashboard
   - Click on your project

2. **View Logs:**
   - Click "Deployments" tab
   - Click on your latest deployment
   - Click "Functions" tab
   - Click on `api/wsgi`
   - You should see error logs

**Look for errors like:**
- `relation "app1_users" does not exist` → Migrations not run
- `could not connect to database` → Wrong DATABASE_URL
- `No module named 'dj_database_url'` → Requirements issue

**Tell me what error you see, or continue to Step 2.**

---

## 🗄️ Step 2: Run Migrations on Neon Database

Your database is empty! You need to run migrations.

### A. Connect to Your Neon Database

```bash
# Set your Neon DATABASE_URL
export DATABASE_URL='your-neon-database-url'

# Test connection
cd /home/shivam/Investa
/home/shivam/Investa/venv/bin/python manage.py dbshell
# If it connects, press Ctrl+D to exit
```

### B. Run Migrations

```bash
# Still in /home/shivam/Investa with DATABASE_URL set
/home/shivam/Investa/venv/bin/python manage.py migrate

# You should see:
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying app1.0001_initial... OK
#   ... (many more)
```

### C. Initialize Stocks

```bash
/home/shivam/Investa/venv/bin/python manage.py init_simulator

# You should see:
# Initializing stock market simulator...
# ✓ Created stock: AAPL - Apple Inc.
# ... (10 stocks)
```

### D. Create Superuser

```bash
/home/shivam/Investa/venv/bin/python manage.py createsuperuser

# Enter:
# Username: admin
# Email: your@email.com
# Password: <strong-password>
```

### E. Clear Environment Variable

```bash
unset DATABASE_URL
```

---

## ⚙️ Step 3: Verify Vercel Environment Variables

Make sure these are set in Vercel:

1. **Go to Vercel Dashboard** → Your Project → Settings → Environment Variables

2. **Check these exist:**

```bash
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.vercel.app
DATABASE_URL=<your-neon-database-url>
```

3. **If any are missing, add them and redeploy:**
   - Click "Redeploy" button in Deployments tab

---

## 🔧 Step 4: Fix Common Issues

### Issue A: Database URL Format

Neon gives you a URL like:
```
postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname
```

Make sure it's in Vercel environment variables **exactly as given** by Neon.

### Issue B: ALLOWED_HOSTS

Update Vercel environment variable:
```bash
# If your Vercel URL is: https://tradesim-abc123.vercel.app
DJANGO_ALLOWED_HOSTS=tradesim-abc123.vercel.app,.vercel.app
```

Or get your actual Vercel URL and add it.

### Issue C: Missing Dependencies

Your `requirements.txt` should have (it does):
```
dj-database-url==2.1.0
psycopg[binary]==3.1.18
```

---

## 🚀 Step 5: Force Redeploy

After running migrations:

1. **Go to Vercel Dashboard** → Your Project
2. **Deployments** tab
3. Click "..." menu on latest deployment
4. Click "Redeploy"
5. Wait for deployment to complete

---

## 🧪 Step 6: Test Deployment

Visit these URLs (replace with your actual Vercel URL):

```bash
# Root (should redirect to login)
https://your-app.vercel.app/

# Login page (should show purple UI)
https://your-app.vercel.app/login

# Admin (should show login)
https://your-app.vercel.app/admin/
```

---

## 🐛 Advanced Debugging

If still failing, let's debug step by step:

### A. Test Database Connection Locally

```bash
# Set Neon DATABASE_URL
export DATABASE_URL='your-neon-url'

# Test Django can connect
cd /home/shivam/Investa
/home/shivam/Investa/venv/bin/python manage.py check --database default

# Should say: System check identified no issues
```

### B. Test WSGI Endpoint Locally

```bash
# With DATABASE_URL still set
cd /home/shivam/Investa
/home/shivam/Investa/venv/bin/python api/wsgi.py

# Should start a simple server
# Press Ctrl+C to stop
```

### C. Check for Missing Tables

```bash
# Connect to Neon database
export DATABASE_URL='your-neon-url'
/home/shivam/Investa/venv/bin/python manage.py dbshell

# In PostgreSQL prompt:
\dt  -- List all tables

# You should see tables like:
# app1_users
# app1_stock
# app1_simulatorsettings
# django_migrations
# auth_permission
# ... etc

# Exit:
\q
```

---

## 📋 Quick Troubleshooting Checklist

```
[ ] Migrations run on Neon database
[ ] init_simulator run (10 stocks created)
[ ] Superuser created
[ ] All environment variables set in Vercel
[ ] DATABASE_URL in Vercel matches Neon URL
[ ] DJANGO_ALLOWED_HOSTS includes Vercel domain
[ ] Redeployed after setting variables
[ ] Checked Vercel function logs for specific error
```

---

## 🆘 Most Common Fix

**99% of the time, it's migrations not run.** Run this:

```bash
# Copy your Neon DATABASE_URL from Vercel dashboard
export DATABASE_URL='postgresql://user:pass@ep-xxx.neon.tech/dbname'

# Run migrations
cd /home/shivam/Investa
/home/shivam/Investa/venv/bin/python manage.py migrate
/home/shivam/Investa/venv/bin/python manage.py init_simulator
/home/shivam/Investa/venv/bin/python manage.py createsuperuser

# Clear
unset DATABASE_URL

# Then in Vercel: Redeploy
```

---

## 📞 Need More Help?

**Tell me:**
1. What error you see in Vercel function logs
2. Did migrations run successfully?
3. Your Vercel URL so I can help debug

**Or try this quick diagnostic:**

```bash
# Test everything locally with Neon DB
export DATABASE_URL='your-neon-url'
cd /home/shivam/Investa

# This should work without errors:
/home/shivam/Investa/venv/bin/python manage.py check
/home/shivam/Investa/venv/bin/python manage.py migrate --check
/home/shivam/Investa/venv/bin/python manage.py showmigrations

# If any fail, that's your issue!
```

---

## 🎯 Expected Result

After fixing, visiting `https://your-app.vercel.app/login` should show:
- Purple gradient "TradeSim" UI
- "Welcome Back" heading
- Modern login form
- No error pages

---

**Start with Step 2 (Run Migrations) - that's the most likely fix!** 🚀
