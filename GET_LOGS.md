# 🔍 Getting Vercel Function Logs

## Current Status
You're getting **"Server Error (500)"** - this means:
- ✅ Environment variables are being read
- ✅ Python function is starting
- ❌ Something in Django is throwing an error

We need to see the actual Python traceback to fix it.

---

## 📋 How to View Vercel Function Logs

### Method 1: Via Vercel Dashboard (Easiest)

1. **Go to:** https://vercel.com/dashboard
2. **Click:** Your "tradesim" project
3. **Click:** "Deployments" tab
4. **Click:** The latest deployment (top one)
5. **Click:** "Functions" tab
6. **Click:** "api/wsgi" function
7. **Look for:** Red error messages with Python tracebacks

**Take a screenshot of the error and show me!**

---

### Method 2: Via Vercel CLI

Run this in your terminal:

```bash
cd /home/shivam/Investa

# Get your latest deployment URL
vercel ls

# View logs for the latest deployment
# Copy the URL from the output above and use it here:
vercel logs <your-deployment-url>
```

---

## 🔧 Common 500 Errors and Fixes

While you're getting the logs, here are the most common issues:

### Issue 1: Static Files (Most Likely)

Django can't find static files in production. Let's check if this is the issue.

**Fix:** Update `settings.py` to handle static files better:

```python
# In demostocks/settings.py, check if you have:
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# And STORAGES config for WhiteNoise
```

### Issue 2: Template Loading

Django can't find templates.

**Check in settings.py:**
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Should be absolute path
        ...
    }
]
```

### Issue 3: Database Query Error

Something wrong with how we're querying the database.

**Test locally with production DB:**
```bash
export DATABASE_URL='postgresql://neondb_owner:npg_4jyo1HKiJPtO@ep-divine-sun-a1ceqydv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
export DJANGO_DEBUG='True'  # Enable debug to see errors
cd /home/shivam/Investa
/home/shivam/Investa/venv/bin/python manage.py runserver
```

Then visit http://localhost:8000/login and see if you get an error.

---

## 🚀 Quick Test Commands

Run these to diagnose:

```bash
cd /home/shivam/Investa

# Test 1: Check if settings load
export DATABASE_URL='postgresql://neondb_owner:npg_4jyo1HKiJPtO@ep-divine-sun-a1ceqydv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
export DJANGO_DEBUG='False'
export DJANGO_SECRET_KEY='qlg(g9)cuh9rnq7(cjai&e4pa0n$ap(g-(dx!y^=c7@mukw1+d'
export DJANGO_ALLOWED_HOSTS='tradesim-lyart.vercel.app,.vercel.app'

/home/shivam/Investa/venv/bin/python manage.py check

# Test 2: Try to import WSGI
/home/shivam/Investa/venv/bin/python -c "
import os
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_4jyo1HKiJPtO@ep-divine-sun-a1ceqydv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_SECRET_KEY'] = 'qlg(g9)cuh9rnq7(cjai&e4pa0n\$ap(g-(dx!y^=c7@mukw1+d'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'tradesim-lyart.vercel.app,.vercel.app'

from api.wsgi import app
print('✅ WSGI loaded successfully!')
print('App:', app)
"

# Test 3: Test a view
/home/shivam/Investa/venv/bin/python manage.py shell -c "
from app1.views import health_check
from django.test import RequestFactory
rf = RequestFactory()
request = rf.get('/health')
try:
    response = health_check(request)
    print('✅ View executed:', response.content)
except Exception as e:
    print('❌ View error:', e)
    import traceback
    traceback.print_exc()
"
```

---

## 📸 What to Send Me

1. **Screenshot of Vercel function logs** (most important!)
2. **Output of the test commands above**
3. **Or tell me what error you see**

Without seeing the actual Python error, I'm guessing. The function logs will tell us exactly what's wrong!

---

## 🎯 Most Likely Fix

Based on typical Django + Vercel issues, it's probably one of these:

1. **Static files issue** - Django can't serve static files
2. **ALLOWED_HOSTS mismatch** - Domain not matching
3. **Missing dependency** - Some package not installed

**Go check those function logs and let me know what you see!** 🔍
