# Stock Market Simulator - Deployment Guide

A Django-based stock market simulator where you can control stock prices and user balances through the admin panel.

## 🎯 Features

- **Admin Control Panel**: Control stock prices, user balances, and simulator settings
- **User Accounts**: Users start with a default balance (configurable via admin)
- **Stock Trading**: Buy and sell stocks with real-time balance updates
- **Portfolio Management**: Track holdings, watchlists, and trading history
- **Price Control**: Manually set stock prices through admin interface

## 🚀 Quick Start (Local Development)

### 1. Setup Environment

```bash
# Navigate to project directory
cd /home/shivam/Investa

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Initialize Simulator

```bash
# This creates default stocks (AAPL, MSFT, GOOG, etc.) and settings
python manage.py init_simulator
```

### 4. Create Admin Account

```bash
python manage.py createsuperuser
```

### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit:
- Main app: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 🔧 Admin Controls

### Stock Price Control

1. Go to `/admin/app1/stock/`
2. Click on any stock to edit its price
3. Or use bulk actions:
   - Increase/decrease price by 10%
   - Activate/deactivate stocks
   - Set previous close = current price

### User Balance Control

1. Go to `/admin/app1/users/`
2. View all user balances
3. Use bulk actions:
   - Reset balance to default
   - Add $1,000 or $5,000 bonus
   - Or edit individual user balances

### Global Settings

1. Go to `/admin/app1/simulatorsettings/`
2. Control:
   - `default_user_balance`: Starting balance for new users (default: $10,000)
   - `trading_fee_percent`: Trading fee percentage (default: 0%)

## 📦 Deploying to Vercel

### Prerequisites

- GitHub account
- Vercel account (free tier works)
- PostgreSQL database (Vercel Postgres, Supabase, or Railway)

### Step 1: Setup Database

**Option A: Vercel Postgres (Recommended)**

1. Go to Vercel Dashboard → Storage → Create Database
2. Select PostgreSQL
3. Copy the `DATABASE_URL` connection string

**Option B: Supabase (Free tier available)**

1. Create project at https://supabase.com
2. Go to Settings → Database
3. Copy the connection string (use "Connection pooling" URL for production)

### Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - Stock Market Simulator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 3: Deploy on Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Configure environment variables (see below)
4. Click "Deploy"

### Step 4: Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables, add:

```
DJANGO_SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.vercel.app,yourdomain.com
DATABASE_URL=postgresql://username:password@host:port/database
```

**Generate a secure SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Run Migrations on Production

You need to run migrations against your production database. There are two options:

**Option A: Run locally pointing to production DB**

```bash
# Set production DATABASE_URL temporarily
export DATABASE_URL='your-production-database-url'

# Run migrations
python manage.py migrate

# Initialize simulator
python manage.py init_simulator

# Create admin account
python manage.py createsuperuser
```

**Option B: Use Vercel CLI**

```bash
# Install Vercel CLI
npm i -g vercel

# Link to your project
vercel link

# Run command on Vercel
vercel env pull .env.local
python manage.py migrate --settings=demostocks.settings
```

### Step 6: Access Your Deployed App

- Main app: `https://your-project.vercel.app/`
- Admin panel: `https://your-project.vercel.app/admin/`

## 🎮 How to Use the Simulator

### As Administrator:

1. Login to `/admin/`
2. **Create Stocks**:
   - Go to Stocks → Add Stock
   - Set symbol, name, and initial price
   - Mark as active
3. **Control Prices**:
   - Edit stock prices directly
   - Use bulk actions to simulate market movements
4. **Manage Users**:
   - View user balances and holdings
   - Give bonuses or reset balances
   - Set default starting balance for new users

### As User:

1. **Sign Up**: Create account at `/signup`
2. **Dashboard**: View watchlist and portfolio
3. **Trade Stocks**: 
   - Click on any stock to see details
   - Buy with available balance
   - Sell from holdings
4. **Portfolio**: Track your investments at `/portfolio`

## 📁 Project Structure

```
Investa/
├── app1/                       # Main application
│   ├── models.py              # User, Stock, SimulatorSettings models
│   ├── views.py               # Trading views
│   ├── admin.py               # Enhanced admin interface
│   ├── apis.py                # API endpoints
│   ├── management/commands/   # Management commands
│   │   └── init_simulator.py # Initialize stocks & settings
│   └── migrations/            # Database migrations
├── demostocks/                # Django project settings
│   ├── settings.py            # Main settings (DB, static files)
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI config
├── api/
│   └── wsgi.py                # Vercel entrypoint
├── static/                    # Static files (JS, CSS)
├── templates/                 # HTML templates
├── requirements.txt           # Python dependencies
├── vercel.json                # Vercel configuration
└── README.md                  # This file
```

## 🔒 Security Notes

⚠️ **Important for Production:**

1. Never commit `.env` files or expose `SECRET_KEY`
2. Always set `DEBUG=False` in production
3. Use strong passwords for admin accounts
4. Regularly backup your database
5. Consider rate limiting for API endpoints
6. Use HTTPS (Vercel provides this automatically)

## 🛠️ Troubleshooting

### Collectstatic fails
```bash
# Make sure STORAGES setting is configured (already done in settings.py)
python manage.py collectstatic --noinput
```

### Migration errors
```bash
# Reset migrations if needed (WARNING: deletes data)
python manage.py migrate app1 zero
python manage.py migrate
```

### Stock prices not updating
- Check that stocks are marked as `is_active=True` in admin
- Verify admin changes are saving (check last_updated timestamp)

### Users can't login
- Verify AUTH_USER_MODEL is set to 'app1.users'
- Check password is stored correctly (not hashed in current implementation)

## 📊 Database Models

### User Model
- `balance`: Current cash balance
- `stockbuy`: JSON of currently held stocks
- `stocksold`: JSON of sold stocks history
- `watchlist`: JSON of favorite stocks

### Stock Model
- `symbol`: Stock ticker (primary key)
- `name`: Company name
- `current_price`: Current trading price
- `previous_close`: Previous closing price
- `is_active`: Whether stock can be traded

### SimulatorSettings Model
- `default_user_balance`: Starting balance for new users
- `trading_fee_percent`: Optional trading fees

## 🤝 Contributing

To modify the simulator:

1. Update models in `app1/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Update admin interface in `app1/admin.py`
5. Test locally before deploying

## 📄 License

This is a learning/demo project. Feel free to use and modify.

## 🆘 Support

For issues:
1. Check this README first
2. Verify environment variables are set correctly
3. Check Vercel deployment logs
4. Ensure database migrations ran successfully

---

**Happy Trading! 📈**
