# 🐛 Debugging Vercel Serverless Function Crash

## Current Issue
Your Django app crashes when accessed via Vercel with:
```
500: INTERNAL_SERVER_ERROR
Code: FUNCTION_INVOCATION_FAILED
```

## ✅ What's Working
- ✅ Neon database connected (10 stocks, migrations applied)
- ✅ Local Django app works fine
- ✅ Authentication removed (no more login screen)
- ✅ Vercel deployment successful

## ❌ What's Broken
The Python function is crashing when invoked. This is usually caused by:

1. **Missing or incorrect environment variables**
2. **Import errors in production**
3. **ALLOWED_HOSTS mismatch**
4. **Django settings issue in production**

---

## 🔧 Step 1: Check Environment Variables in Vercel

Go to: **Vercel Dashboard → tradesim → Settings → Environment Variables**

You MUST have these set:

```bash
DATABASE_URL=postgresql://neondb_owner:npg_4jyo1HKiJPtO@ep-divine-sun-a1ceqydv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

DJANGO_SECRET_KEY=<any-long-random-string>

DJANGO_DEBUG=False

DJANGO_ALLOWED_HOSTS=tradesim-lyart.vercel.app,.vercel.app
```

**Action:** 
1. Check if DATABASE_URL is set correctly
2. Check if DJANGO_SECRET_KEY exists
3. Check if DJANGO_ALLOWED_HOSTS includes your domain

---

## 🔧 Step 2: Check Vercel Function Logs

1. Go to **Vercel Dashboard**
2. Click **"tradesim"** project
3. Click **"Deployments"** tab
4. Click on the latest deployment
5. Click **"Functions"** tab
6. Click **"api/wsgi"**
7. Look for **Python error messages**

Common errors you might see:
- `ModuleNotFoundError: No module named 'X'` → Missing dependency
- `DisallowedHost at /` → ALLOWED_HOSTS issue
- `OperationalError: could not connect to database` → DATABASE_URL wrong
- `ImproperlyConfigured: SECRET_KEY` → Missing SECRET_KEY

---

## 🔧 Step 3: Test Local Production Settings

Test if your app works with production settings locally:

```bash
cd /home/shivam/Investa

# Set production environment
export DATABASE_URL='postgresql://neondb_owner:npg_4jyo1HKiJPtO@ep-divine-sun-a1ceqydv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
export DJANGO_DEBUG='False'
export DJANGO_SECRET_KEY='test-secret-key-12345'
export DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'

# Test if Django starts
/home/shivam/Investa/venv/bin/python manage.py check --deploy

# Test if WSGI loads
/home/shivam/Investa/venv/bin/python -c "from api.wsgi import app; print('✅ WSGI loaded successfully')"
```

If this fails locally, you'll see the actual error!

---

## 🔧 Step 4: Most Common Fixes

### Fix A: Update ALLOWED_HOSTS Environment Variable

The domain changed! Update in Vercel:

```bash
# Old (wrong):
DJANGO_ALLOWED_HOSTS=.vercel.app

# New (correct):
DJANGO_ALLOWED_HOSTS=tradesim-lyart.vercel.app,.vercel.app,tradesim-lyart.vercel.app
```

### Fix B: Ensure DATABASE_URL is Correct

In Vercel environment variables, make sure DATABASE_URL has:
```
postgresql://neondb_owner:npg_4jyo1HKiJPtO@ep-divine-sun-a1ceqydv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

**Important:** No spaces, no quotes in Vercel UI!

### Fix C: Add DJANGO_SECRET_KEY

If missing, generate one:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then add it to Vercel environment variables.

---

## 🔧 Step 5: Force Redeploy

After updating environment variables:

1. **In Vercel Dashboard:**
   - Go to Deployments
   - Click "..." menu on latest deployment
   - Click "Redeploy"
   - Wait for new deployment

2. **OR via CLI:**
```bash
cd /home/shivam/Investa
vercel --prod --force
```

---

## 🎯 Quick Diagnostic Commands

Run these to check your local setup:

```bash
cd /home/shivam/Investa

# 1. Check if all imports work
export DATABASE_URL='postgresql://neondb_owner:npg_4jyo1HKiJPtO@ep-divine-sun-a1ceqydv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
/home/shivam/Investa/venv/bin/python -c "
import django
import dj_database_url
import psycopg2
from demostocks import settings
from api import wsgi
print('✅ All imports successful')
"

# 2. Check database connection
/home/shivam/Investa/venv/bin/python manage.py check --database default

# 3. Check WSGI app
/home/shivam/Investa/venv/bin/python api/wsgi.py &
sleep 2
curl -I http://127.0.0.1:8000/health
pkill -f "api/wsgi.py"
```

---

## 📋 Checklist Before Asking for Help

```
[ ] Checked Vercel environment variables are set
[ ] DATABASE_URL is correct (copy-pasted from Neon)
[ ] DJANGO_SECRET_KEY exists
[ ] DJANGO_ALLOWED_HOSTS includes tradesim-lyart.vercel.app
[ ] Checked Vercel function logs for actual error
[ ] Tested production settings locally (works?)
[ ] Redeployed after changing variables
[ ] Waited 1-2 minutes for deployment to complete
```

---

## 🆘 Next Steps

**Tell me:**
1. What do you see in Vercel Function Logs? (Step 2)
2. Do the diagnostic commands work locally? (Step 5)
3. Are all environment variables set in Vercel? (Step 1)

**Or I can help you:**
- Navigate to the function logs
- Set environment variables correctly
- Test the app with production settings locally

---

## 💡 Most Likely Issue

Based on the error, it's probably one of these:

1. **ALLOWED_HOSTS** doesn't include `tradesim-lyart.vercel.app`
2. **DATABASE_URL** not set in Vercel
3. **Missing psycopg2-binary** (we fixed this, but worth checking)

Let me know what you find in the Vercel function logs! 🔍
