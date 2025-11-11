# 🚀 TradeWars - Complete Local Development Guide

## Prerequisites

### Required Software:
1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Git** - [Download](https://git-scm.com/downloads/)
3. **Code Editor** - VS Code recommended

### NOT Required:
- ❌ **Vercel Pro** - NOT needed for local development
- ❌ **Node.js** - Only needed for deployment
- ❌ **External API keys** - Stock prices are simulated

---

## 🏁 Quick Start (5 Minutes)

### Step 1: Clone the Repository
```bash
cd ~
git clone https://github.com/school11220/tradesim.git
cd tradesim
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
# Run migrations
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser
# Enter username, email, and password when prompted
```

### Step 5: Run the Server
```bash
python manage.py runserver
```

### Step 6: Access the Platform
Open your browser and go to:
- **Main site**: http://127.0.0.1:8000/
- **Admin panel**: http://127.0.0.1:8000/admin/
- **Team login**: http://127.0.0.1:8000/team/login
- **Team signup**: http://127.0.0.1:8000/team/signup

---

## 📊 Stock Price Updates - Complete Guide

### How Price Updates Work

**NO VERCEL PRO NEEDED!** The system has 3 ways to update prices:

### Method 1: Automatic Updates (Production Only)
**Location**: GitHub Actions (`.github/workflows/update-prices.yml`)

- Runs every **1 minute** during trading hours
- Only works when deployed on Vercel
- Free GitHub Actions (no cost)
- Calls: `https://your-site.vercel.app/api/update-prices-real`

**For Local Dev**: This won't work locally (needs public URL)

---

### Method 2: Manual Updates via Admin Panel ⭐ **BEST FOR LOCAL**

#### Step-by-Step:

1. **Start your local server**:
   ```bash
   python manage.py runserver
   ```

2. **Login to Admin**:
   - Go to: http://127.0.0.1:8000/admin/
   - Enter your superuser credentials

3. **Navigate to Market Control**:
   - Look for "APP1" section
   - Click "Stocks" (or go directly to: http://127.0.0.1:8000/admin/app1/stock/)
   - Click "Stock Market Control" button at top

4. **Update Prices**:
   
   **Option A - Realistic Simulation**:
   - Click "🎲 Run Simulation Now" button
   - Updates all stocks with market sentiment
   - Includes sector trends and volatility
   
   **Option B - Random Fluctuation**:
   - Click "🎲 Randomize Prices Now" button
   - Simple ±2% random changes
   
   **Option C - Sector Adjustments**:
   - Select a sector (Technology, Healthcare, etc.)
   - Click "+5%", "-5%", "+10%", "-10%" buttons
   - OR enter custom % (like 1.2%, 0.9%, -3.5%)
   - Click "Apply Custom %"
   
   **Option D - All Sectors**:
   - Scroll to "Apply Change to ALL Sectors"
   - Enter custom % (e.g., 2.5%)
   - Click "Apply to All Sectors"

---

### Method 3: API Endpoints (For Scripts/Testing)

You can trigger price updates via API calls:

#### A. Realistic Simulation:
```bash
# Using curl (Linux/Mac/Git Bash)
curl http://127.0.0.1:8000/api/update-prices-real

# Using Python
import requests
response = requests.get('http://127.0.0.1:8000/api/update-prices-real')
print(response.json())
```

#### B. Random Fluctuation:
```bash
curl http://127.0.0.1:8000/api/update-prices
```

#### C. Sector Adjustment:
```bash
# Adjust Technology sector by +5%
curl -X POST http://127.0.0.1:8000/api/adjust-sector \
  -H "Content-Type: application/json" \
  -d '{"sector": "Technology", "percentage": 5.0}'

# Note: Requires admin authentication
```

#### D. All Sectors:
```bash
curl -X POST http://127.0.0.1:8000/api/adjust-all-sectors \
  -H "Content-Type: application/json" \
  -d '{"percentage": 2.5}'
```

---

### Method 4: Django Management Command

Create a custom script to run price updates:

```bash
# Run one-time update
python manage.py update_real_prices

# Run continuously (every 60 seconds)
python manage.py update_real_prices --continuous --interval 60
```

---

## 🎮 Testing Stock Prices Locally

### Create a Quick Test Script:

Create `test_prices.py` in project root:

```python
#!/usr/bin/env python
import os
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
django.setup()

from app1.models import Stock

def update_prices():
    """Update all stock prices with simulation"""
    print("🔄 Updating stock prices...")
    
    stocks = Stock.objects.filter(is_active=True)
    updated = 0
    
    for stock in stocks:
        old_price = float(stock.current_price)
        new_price = float(stock.update_price_random(0.02))  # ±2% volatility
        change = new_price - old_price
        change_pct = (change / old_price) * 100
        
        print(f"  {stock.symbol:6s} ${old_price:8.2f} → ${new_price:8.2f}  {change:+7.2f} ({change_pct:+.2f}%)")
        updated += 1
    
    print(f"✅ Updated {updated} stocks\n")

if __name__ == "__main__":
    print("🎲 Stock Price Simulator - Press Ctrl+C to stop\n")
    
    try:
        while True:
            update_prices()
            time.sleep(60)  # Update every 60 seconds
    except KeyboardInterrupt:
        print("\n🛑 Stopped")
```

Run it:
```bash
python test_prices.py
```

---

## 🔧 Database Setup & Management

### Initialize with Sample Data:

1. **Create stocks** (if not already created):
   ```bash
   python init_db.py
   # OR
   python quick_init.py
   ```

2. **Create test event and teams**:
   ```bash
   python create_test_team.py
   ```

### View Database:

```bash
# SQLite browser (GUI)
# Download from: https://sqlitebrowser.org/

# Or use Django shell
python manage.py shell

# Then in shell:
from app1.models import Stock, Team, Event
Stock.objects.count()  # See how many stocks
Stock.objects.all()[:5]  # See first 5
```

---

## 📁 Project Structure

```
tradesim/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # Local database
├── app1/                 # Main app
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── apis.py           # API endpoints ⭐
│   ├── admin.py          # Admin interface
│   └── management/       # Custom commands
│       └── commands/
│           └── update_real_prices.py
├── demostocks/           # Project settings
│   ├── settings.py       # Configuration
│   └── urls.py           # URL routing
└── templates/            # HTML templates
    ├── main/             # Team pages
    └── login/            # Auth pages
```

---

## ⚙️ Configuration

### Settings File: `demostocks/settings.py`

**Debug Mode** (for local development):
```python
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

**Database** (SQLite by default):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 🎯 Common Tasks

### 1. Add New Stocks:
```bash
python manage.py shell
```
```python
from app1.models import Stock

Stock.objects.create(
    symbol='TSLA',
    name='Tesla Inc.',
    sector='Consumer',
    current_price=250.00,
    previous_close=248.00,
    is_active=True
)
```

### 2. Adjust Stock Prices Manually:
```python
from app1.models import Stock

# Get stock
aapl = Stock.objects.get(symbol='AAPL')

# Change price
aapl.current_price = 230.00
aapl.save()
```

### 3. Create Trading Event:
```python
from app1.models import Event
from django.utils import timezone
from datetime import timedelta

Event.objects.create(
    name='Spring Trading Competition 2025',
    start_time=timezone.now(),
    end_time=timezone.now() + timedelta(days=30),
    initial_capital=500000.00,
    is_active=True
)
```

### 4. Reset Prices:
```bash
python manage.py shell
```
```python
from app1.models import Stock

# Reset all to previous close
for stock in Stock.objects.all():
    stock.current_price = stock.previous_close
    stock.save()
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'django'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Table doesn't exist"
```bash
# Run migrations
python manage.py migrate
```

### Issue: "Port already in use"
```bash
# Kill existing process
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
python manage.py runserver 8001
```

### Issue: "Stock prices not updating"
```bash
# Check if stocks exist
python manage.py shell
from app1.models import Stock
print(Stock.objects.count())

# If 0, initialize:
python init_db.py
```

### Issue: "Admin panel not accessible"
```bash
# Create superuser
python manage.py createsuperuser

# Collect static files (if needed)
python manage.py collectstatic
```

---

## 🚀 Deployment (Optional)

### Deploy to Vercel (Free):

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

3. **Set Environment Variables** (in Vercel dashboard):
   - `DJANGO_SECRET_KEY`: Your secret key
   - `PYTHON_VERSION`: 3.9

### GitHub Actions (Automatic Price Updates):
- Already configured in `.github/workflows/update-prices.yml`
- Runs every 1 minute during trading hours
- Free with GitHub Actions
- NO VERCEL PRO NEEDED

---

## 💡 Tips for Local Development

### 1. **Keep Server Running**:
```bash
# Terminal 1: Run server
python manage.py runserver

# Terminal 2: Run price updater (optional)
python test_prices.py
```

### 2. **Test Trading Flow**:
- Create teams at: http://127.0.0.1:8000/team/signup
- Login and trade stocks
- Watch prices update
- Check portfolio

### 3. **Admin Panel Shortcuts**:
- Stocks: http://127.0.0.1:8000/admin/app1/stock/
- Teams: http://127.0.0.1:8000/admin/app1/team/
- Events: http://127.0.0.1:8000/admin/app1/event/
- Market Control: http://127.0.0.1:8000/admin/app1/stock/ (click "Stock Market Control")

### 4. **Quick Price Update**:
```bash
# In browser console (F12) on any team page:
fetch('/api/update-prices-real').then(r => r.json()).then(console.log)
```

---

## 📊 Price Update Frequency Recommendations

### Local Development:
- **Manual updates**: As needed via admin panel
- **Script**: Every 60-120 seconds (if testing)
- **Don't overdo it**: Your computer isn't a server

### Production (Vercel):
- **GitHub Actions**: Every 1 minute (already configured)
- **No cost**: Free GitHub Actions
- **Automatic**: No manual intervention needed

---

## 🎓 Summary

### To Run Locally:
1. Install Python 3.8+
2. Clone repo
3. Create virtual environment
4. Install dependencies (`pip install -r requirements.txt`)
5. Run migrations (`python manage.py migrate`)
6. Create superuser (`python manage.py createsuperuser`)
7. Run server (`python manage.py runserver`)
8. Access at http://127.0.0.1:8000/

### To Update Stock Prices:
**NO VERCEL PRO NEEDED!**

**Best Methods for Local Dev:**
1. ⭐ **Admin Panel** - Click "Run Simulation Now"
2. 🔧 **Python Script** - Run `test_prices.py`
3. 🌐 **API Call** - `curl http://127.0.0.1:8000/api/update-prices-real`
4. 💻 **Django Command** - `python manage.py update_real_prices`

**For Production:**
- GitHub Actions (free) handles automatic updates
- No Vercel Pro required
- Already configured

---

## 🆘 Need Help?

### Check:
1. Virtual environment is activated
2. Dependencies installed (`pip list`)
3. Migrations run (`python manage.py showmigrations`)
4. Server is running (check terminal)
5. Port 8000 is free

### Common Commands:
```bash
# Check Django version
python manage.py --version

# Check database tables
python manage.py dbshell
.tables

# Check stock count
python manage.py shell
from app1.models import Stock
Stock.objects.count()

# Reset database (DANGER - deletes all data)
rm db.sqlite3
python manage.py migrate
python init_db.py
```

---

**You're ready to develop TradeWars locally! No Vercel Pro needed!** 🎉
