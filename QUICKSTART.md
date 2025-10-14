# 🎯 Quick Start Guide - Stock Market Simulator

## ✅ What's Been Set Up

Your stock market simulator is now **production-ready** with:

✅ **Admin Control Panel** - Full control over stock prices and user balances
✅ **10 Default Stocks** - AAPL, MSFT, GOOG, META, AMZN, TSLA, NVDA, NFLX, SONY, DIS
✅ **PostgreSQL Support** - Ready for Vercel deployment
✅ **Static Files** - Configured with WhiteNoise
✅ **Management Commands** - Easy initialization and configuration

## 🚀 Your App is Running!

**Local Development Server:** http://127.0.0.1:8000/

## 🔑 Next Steps

### 1. Create Your Admin Account

```bash
/home/shivam/Investa/venv/bin/python manage.py createsuperuser
```

Enter:
- Username (e.g., admin)
- Email (optional)
- Password (make it strong!)

### 2. Access Admin Panel

Go to: http://127.0.0.1:8000/admin/

Login with your superuser credentials.

### 3. Control Your Simulator

#### 📊 Manage Stocks (Admin → Stocks)
- View all 10 default stocks
- **Edit prices manually** - Click any stock to change its price
- **Bulk actions:**
  - Increase/decrease price by 10%
  - Activate/deactivate stocks
  - Reset price changes

#### 💰 Manage Users (Admin → Users)
- View all registered users and their balances
- **Edit balances directly**
- **Bulk actions:**
  - Reset balance to default ($10,000)
  - Add $1,000 bonus
  - Add $5,000 bonus

#### ⚙️ Global Settings (Admin → Simulator Settings)
- `default_user_balance` - Starting balance for new users (default: $10,000)
- `trading_fee_percent` - Optional trading fees (default: 0%)

### 4. Test the Simulator

1. **Sign up as a regular user:** http://127.0.0.1:8000/signup
2. You'll get $10,000 to start trading
3. **Dashboard:** View watchlist and portfolio
4. **Trade stocks:** Click any stock to buy/sell
5. **As admin:** Go back to admin panel and change stock prices
6. **Refresh user dashboard:** See the new prices instantly!

## 🎮 How to Control the Simulator

### Scenario 1: Simulate a Market Crash
1. Go to Admin → Stocks
2. Select all stocks (checkbox)
3. Choose "Decrease price by 10%" from Actions dropdown
4. Click "Go"
5. Users will see the crash immediately!

### Scenario 2: Give Users Bonus Money
1. Go to Admin → Users
2. Select users (checkbox)
3. Choose "Add $5,000 bonus" from Actions dropdown
4. Click "Go"

### Scenario 3: Create a Custom Stock
1. Go to Admin → Stocks → Add Stock
2. Enter:
   - Symbol: YOUR_SYMBOL
   - Name: Company Name
   - Current Price: 100.00
   - Previous Close: 95.00
   - Is Active: ✓
3. Save
4. Users can now trade this stock!

### Scenario 4: Change Default Starting Balance
1. Go to Admin → Simulator Settings
2. Find or create `default_user_balance`
3. Change to desired amount (e.g., 50000 for $50,000)
4. Save
5. New users will start with this amount!

## 📦 Deploy to Production (Vercel)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick Summary:**

1. **Get a Database:**
   - Vercel Postgres: https://vercel.com/storage
   - Or Supabase: https://supabase.com (free tier)
   - Copy your `DATABASE_URL`

2. **Push to GitHub:**
```bash
git add .
git commit -m "Stock market simulator ready for deployment"
git push
```

3. **Deploy on Vercel:**
   - Go to https://vercel.com/new
   - Import your GitHub repo
   - Add environment variables:
     - `DATABASE_URL` = your PostgreSQL URL
     - `DJANGO_SECRET_KEY` = generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
     - `DJANGO_DEBUG` = False
     - `DJANGO_ALLOWED_HOSTS` = .vercel.app
   - Click Deploy!

4. **After Deployment:**
```bash
# Point to production database
export DATABASE_URL='your-production-database-url'

# Run migrations
/home/shivam/Investa/venv/bin/python manage.py migrate

# Initialize stocks
/home/shivam/Investa/venv/bin/python manage.py init_simulator

# Create admin
/home/shivam/Investa/venv/bin/python manage.py createsuperuser
```

## 🎨 Customization Ideas

### Add More Stocks
```bash
/home/shivam/Investa/venv/bin/python manage.py shell
```
```python
from app1.models import Stock

Stock.objects.create(
    symbol='CUSTOM',
    name='Custom Company Inc.',
    current_price=150.00,
    previous_close=148.00,
    is_active=True
)
```

### Change Price Programmatically
```python
from app1.models import Stock

# Crash the market!
for stock in Stock.objects.all():
    stock.current_price *= 0.8  # 20% drop
    stock.save()

# Bull run!
for stock in Stock.objects.all():
    stock.current_price *= 1.2  # 20% increase
    stock.save()
```

### Create a Trading Competition
1. Reset all user balances to $10,000
2. Announce a 1-week competition
3. At the end, check Admin → Users sorted by balance
4. Winner = highest balance!

## 🔧 Useful Commands

```bash
# Activate virtual environment
source /home/shivam/Investa/venv/bin/activate

# Run development server
/home/shivam/Investa/venv/bin/python manage.py runserver

# Create new admin user
/home/shivam/Investa/venv/bin/python manage.py createsuperuser

# Reset and reinitialize stocks
/home/shivam/Investa/venv/bin/python manage.py init_simulator

# Run migrations
/home/shivam/Investa/venv/bin/python manage.py migrate

# Collect static files
/home/shivam/Investa/venv/bin/python manage.py collectstatic --noinput

# Open Django shell
/home/shivam/Investa/venv/bin/python manage.py shell
```

## 🐛 Troubleshooting

### Can't login to admin?
- Did you create a superuser? Run: `/home/shivam/Investa/venv/bin/python manage.py createsuperuser`

### Stock prices not showing?
- Run: `/home/shivam/Investa/venv/bin/python manage.py init_simulator`

### Static files not loading?
- Run: `/home/shivam/Investa/venv/bin/python manage.py collectstatic --noinput`

### Database errors?
- Delete `db.sqlite3` and run migrations again
- Reinitialize: `/home/shivam/Investa/venv/bin/python manage.py init_simulator`

## 📞 Support

Check these files for more info:
- **DEPLOYMENT.md** - Complete Vercel deployment guide
- **README.md** - Project overview and features
- **.env.example** - Environment variable template

---

**🎉 Your stock market simulator is ready! Have fun controlling the market!**
