# 🚀 Complete Deployment Guide - TradeSim to Vercel

## 📋 Current Status

✅ **Code is ready and committed locally!**
- All changes committed: `635c0d1`
- 28 files changed with new UI and features
- Ready to push to GitHub

⚠️ **GitHub Authentication Issue**
- Error: Permission denied (403)
- Current Git user: school11220
- Repository: sakshamssr/Investa

---

## 🔧 Step 1: Fix GitHub Authentication

You need to authenticate with the correct GitHub account. Choose one method:

### Method A: Using Personal Access Token (Recommended)

1. **Generate a Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a name: "TradeSim Deployment"
   - Select scopes: `repo` (all repo permissions)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

2. **Update your Git remote:**
   ```bash
   cd /home/shivam/Investa
   
   # Remove old remote
   git remote remove origin
   
   # Add new remote with token
   git remote add origin https://YOUR_TOKEN@github.com/sakshamssr/Investa.git
   
   # Or use your username
   git remote add origin https://sakshamssr:YOUR_TOKEN@github.com/sakshamssr/Investa.git
   ```

3. **Push to GitHub:**
   ```bash
   git push origin main
   ```

### Method B: Using SSH (Alternative)

1. **Generate SSH key (if you don't have one):**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter for all prompts
   ```

2. **Add SSH key to GitHub:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   - Copy the output
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste the key and save

3. **Update your Git remote:**
   ```bash
   cd /home/shivam/Investa
   git remote remove origin
   git remote add origin git@github.com:sakshamssr/Investa.git
   git push origin main
   ```

### Method C: GitHub CLI (Easiest)

1. **Install GitHub CLI:**
   ```bash
   sudo apt install gh
   ```

2. **Authenticate:**
   ```bash
   gh auth login
   # Follow prompts: GitHub.com → HTTPS → Yes → Login with browser
   ```

3. **Push:**
   ```bash
   cd /home/shivam/Investa
   git push origin main
   ```

---

## 🗄️ Step 2: Setup PostgreSQL Database

Choose one option:

### Option A: Vercel Postgres (Recommended - Easiest)

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com/dashboard
   - Sign in (use GitHub account for easy integration)

2. **Create Database:**
   - Click "Storage" tab
   - Click "Create Database"
   - Select "Postgres"
   - Choose region closest to you
   - Click "Create"

3. **Get Connection String:**
   - After creation, click on your database
   - Go to ".env.local" tab
   - Copy the `POSTGRES_URL` value
   - This is your `DATABASE_URL`

### Option B: Supabase (Free Tier Available)

1. **Create Account:**
   - Go to: https://supabase.com
   - Sign up with GitHub

2. **Create Project:**
   - Click "New Project"
   - Name: "TradeSim"
   - Password: Create strong password
   - Region: Choose closest
   - Click "Create new project"

3. **Get Connection String:**
   - Go to Project Settings → Database
   - Find "Connection string" → "URI"
   - **Use Connection pooling URL** (better for production)
   - Copy the URL
   - Replace `[YOUR-PASSWORD]` with your actual password

### Option C: Railway (Also Free Tier)

1. **Create Account:**
   - Go to: https://railway.app
   - Sign up with GitHub

2. **Create Database:**
   - New Project → Provision PostgreSQL
   - Click on PostgreSQL service
   - Variables tab → Copy `DATABASE_URL`

---

## 🚀 Step 3: Deploy to Vercel

### A. Create Vercel Account

1. Go to: https://vercel.com/signup
2. Sign up with your GitHub account
3. This makes importing repos easier!

### B. Import Project

1. **Go to Dashboard:**
   - Visit: https://vercel.com/new

2. **Import Git Repository:**
   - Click "Import Git Repository"
   - Find "sakshamssr/Investa"
   - Click "Import"

3. **Configure Project:**
   - **Project Name:** `tradesim` (or your choice)
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** Leave empty (not needed for Django)
   - **Output Directory:** Leave empty

### C. Add Environment Variables

Click "Environment Variables" and add these:

```bash
# Django Settings
DJANGO_SECRET_KEY=<generate-new-secret-below>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.vercel.app

# Database (from Step 2)
DATABASE_URL=<your-postgresql-url-from-step-2>
```

**Generate SECRET_KEY:**
```bash
/home/shivam/Investa/venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and use it as `DJANGO_SECRET_KEY`.

### D. Deploy

1. Click "Deploy"
2. Wait 2-3 minutes for deployment
3. You'll get a URL like: `https://tradesim-xxx.vercel.app`

---

## 🔄 Step 4: Initialize Production Database

After deployment succeeds, you need to run migrations on your production database.

### Method 1: Using Local Connection

1. **Set environment variable temporarily:**
   ```bash
   export DATABASE_URL='your-production-postgresql-url'
   ```

2. **Run migrations:**
   ```bash
   cd /home/shivam/Investa
   /home/shivam/Investa/venv/bin/python manage.py migrate
   ```

3. **Initialize stocks:**
   ```bash
   /home/shivam/Investa/venv/bin/python manage.py init_simulator
   ```

4. **Create superuser:**
   ```bash
   /home/shivam/Investa/venv/bin/python manage.py createsuperuser
   ```
   - Username: admin (or your choice)
   - Email: your email
   - Password: Create strong password

5. **Clear environment variable:**
   ```bash
   unset DATABASE_URL
   ```

### Method 2: Using Database Client

1. **Install PostgreSQL client:**
   ```bash
   sudo apt install postgresql-client
   ```

2. **Connect to production database:**
   ```bash
   psql "your-production-database-url"
   ```

3. **Verify connection:**
   ```sql
   \dt  -- List tables (should show Django tables after migration)
   \q   -- Quit
   ```

---

## ✅ Step 5: Test Your Deployment

### A. Visit Your Site

1. **Main Site:**
   ```
   https://your-app.vercel.app/
   ```
   - Should redirect to login page

2. **Login Page:**
   ```
   https://your-app.vercel.app/login
   ```
   - Should see new purple TradeSim UI

3. **Signup Page:**
   ```
   https://your-app.vercel.app/signup
   ```
   - Create a test account
   - You'll get $10,000 starting balance

4. **Admin Panel:**
   ```
   https://your-app.vercel.app/admin/
   ```
   - Login with superuser credentials
   - Should see "TradeSim Admin Panel"
   - Test changing stock prices

### B. Test Admin Controls

1. **Go to Admin → Stocks**
2. Click any stock (e.g., AAPL)
3. Change price from 178.50 to 200.00
4. Save
5. Login as regular user
6. Try to buy the stock
7. Verify new price shows up

### C. Test Trading

1. **Login as regular user**
2. **Dashboard:** Should show $10,000 balance
3. **Buy stock:** Try buying AAPL
4. **Check balance:** Should decrease
5. **Sell stock:** Try selling
6. **Check balance:** Should increase

---

## 🎯 Complete Deployment Checklist

### ✅ Pre-Deployment (Done!)
- [x] Code committed locally
- [x] UI redesigned (TradeSim purple theme)
- [x] Admin controls added
- [x] PostgreSQL support configured
- [x] Vercel configuration (`vercel.json`)
- [x] Environment example (`.env.example`)
- [x] Documentation created

### 🔄 Deployment Steps (Do Now)
- [ ] **Step 1:** Fix GitHub authentication
- [ ] **Step 1:** Push code to GitHub (`git push origin main`)
- [ ] **Step 2:** Create PostgreSQL database (Vercel/Supabase/Railway)
- [ ] **Step 2:** Copy DATABASE_URL
- [ ] **Step 3:** Sign up for Vercel account
- [ ] **Step 3:** Import GitHub repository
- [ ] **Step 3:** Add environment variables
- [ ] **Step 3:** Deploy project
- [ ] **Step 4:** Run migrations on production database
- [ ] **Step 4:** Initialize stocks (`init_simulator`)
- [ ] **Step 4:** Create superuser
- [ ] **Step 5:** Test login page
- [ ] **Step 5:** Test admin panel
- [ ] **Step 5:** Test trading functionality

---

## 📝 Environment Variables Summary

For Vercel, you need these environment variables:

| Variable | Value | How to Get |
|----------|-------|------------|
| `DJANGO_SECRET_KEY` | Random string | Run command above |
| `DJANGO_DEBUG` | `False` | Set to False for production |
| `DJANGO_ALLOWED_HOSTS` | `.vercel.app` | Or your custom domain |
| `DATABASE_URL` | PostgreSQL URL | From Vercel Postgres/Supabase |

---

## 🐛 Troubleshooting

### GitHub Push Fails (403)
**Problem:** Permission denied
**Solution:** Follow Step 1 above to fix authentication

### Vercel Build Fails
**Problem:** Build errors
**Solution:** 
- Check Vercel logs
- Verify `vercel.json` exists
- Ensure `api/wsgi.py` exists

### Database Connection Error
**Problem:** Can't connect to database
**Solution:**
- Verify `DATABASE_URL` is correct
- Check database is created and running
- Ensure IP whitelist includes Vercel IPs (if using Supabase)

### Static Files Not Loading
**Problem:** CSS/JS not working
**Solution:**
- Already fixed with WhiteNoise
- Verify `collectstatic` ran successfully locally
- Check STORAGES setting in `settings.py`

### Admin Panel 404
**Problem:** /admin returns 404
**Solution:**
- Verify migrations ran on production
- Check `urls.py` includes admin URLs
- Ensure superuser created

### Stock Prices Not Showing
**Problem:** No stocks available
**Solution:**
- Run `init_simulator` command on production database
- Check admin panel → Stocks
- Verify database migrations completed

---

## 🎉 After Successful Deployment

### Share Your Site!
Your deployed URLs will be:
- **Main Site:** `https://your-app.vercel.app`
- **Login:** `https://your-app.vercel.app/login`
- **Admin:** `https://your-app.vercel.app/admin`

### Configure Custom Domain (Optional)
1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update `DJANGO_ALLOWED_HOSTS` to include your domain

### Monitor Your App
- **Vercel Dashboard:** Monitor deployments and logs
- **Database Dashboard:** Monitor database usage
- **Admin Panel:** Control stocks and users

---

## 📞 Need Help?

### Quick Links
- **Vercel Docs:** https://vercel.com/docs
- **Supabase Docs:** https://supabase.com/docs
- **Django Docs:** https://docs.djangoproject.com

### Check These Files
- `DEPLOYMENT.md` - Detailed deployment guide
- `QUICKSTART.md` - Local development guide
- `ADMIN_CHEATSHEET.md` - Admin panel usage
- `SETUP_COMPLETE.md` - What's been done

---

## 🚀 Ready to Deploy!

**Start with Step 1:** Fix GitHub authentication and push your code!

```bash
# Quick command reference:
cd /home/shivam/Investa

# After fixing auth (follow Step 1):
git push origin main

# Then continue with Steps 2-5!
```

**Your TradeSim is ready to go live! 🎉**
