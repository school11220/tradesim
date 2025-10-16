# ⚡ Quick Deployment Commands

## 🔐 Step 1: Push to GitHub

### Fix Authentication First:
```bash
# Method 1: Personal Access Token (Recommended)
# 1. Create token at: https://github.com/settings/tokens
# 2. Copy token
# 3. Run:
cd /home/shivam/Investa
git remote remove origin
git remote add origin https://YOUR_TOKEN@github.com/sakshamssr/Investa.git
git push origin main
```

**OR use GitHub CLI (easier):**
```bash
sudo apt install gh
gh auth login  # Follow prompts
cd /home/shivam/Investa
git push origin main
```

---

## 🗄️ Step 2: Create Database

### Option A: Vercel Postgres
1. Go to: https://vercel.com/dashboard
2. Storage → Create Database → Postgres
3. Copy `POSTGRES_URL` value

### Option B: Supabase (Free)
1. Go to: https://supabase.com
2. New Project → Create
3. Settings → Database → Copy "Connection pooling" URL

---

## 🚀 Step 3: Deploy on Vercel

1. **Visit:** https://vercel.com/new
2. **Import:** sakshamssr/Investa repository
3. **Add Environment Variables:**

```bash
DJANGO_SECRET_KEY=<generate-below>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.vercel.app
DATABASE_URL=<from-step-2>
```

4. **Generate SECRET_KEY:**
```bash
/home/shivam/Investa/venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. **Click "Deploy"**

---

## 🔄 Step 4: Initialize Production Database

```bash
# Set production database URL
export DATABASE_URL='your-production-postgresql-url'

# Run migrations
cd /home/shivam/Investa
/home/shivam/Investa/venv/bin/python manage.py migrate

# Create default stocks
/home/shivam/Investa/venv/bin/python manage.py init_simulator

# Create admin account
/home/shivam/Investa/venv/bin/python manage.py createsuperuser

# Clear environment variable
unset DATABASE_URL
```

---

## ✅ Step 5: Test Your Deployment

Visit these URLs (replace with your actual Vercel URL):
- **Login:** https://your-app.vercel.app/login
- **Signup:** https://your-app.vercel.app/signup
- **Admin:** https://your-app.vercel.app/admin/

---

## 🎯 Quick Checklist

```
[ ] Fix GitHub auth (Step 1)
[ ] Push code: git push origin main
[ ] Create PostgreSQL database (Step 2)
[ ] Copy DATABASE_URL
[ ] Deploy on Vercel (Step 3)
[ ] Add environment variables
[ ] Wait for deployment
[ ] Run migrations (Step 4)
[ ] Initialize stocks
[ ] Create superuser
[ ] Test login page
[ ] Test admin panel
[ ] Test trading
```

---

## 🆘 Common Issues

### Git Push Fails (403)
```bash
# Use GitHub CLI (easiest):
sudo apt install gh
gh auth login
git push origin main
```

### Can't Generate SECRET_KEY
```bash
# Alternative method:
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Migrations Fail
```bash
# Check database connection:
export DATABASE_URL='your-url'
/home/shivam/Investa/venv/bin/python manage.py dbshell
# If connects, try migrate again
```

---

## 📱 Your Deployed URLs

After deployment, you'll have:
- Main Site: `https://[your-project].vercel.app`
- Login: `https://[your-project].vercel.app/login`
- Admin: `https://[your-project].vercel.app/admin`

---

## 🎉 That's It!

Follow these steps in order and your TradeSim will be live!

**Start here:** Fix GitHub auth and push your code (Step 1)
