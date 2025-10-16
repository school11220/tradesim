# 🚀 PRODUCTION DEPLOYMENT GUIDE

## ✅ Code Deployed to Vercel
Your code has been pushed to GitHub and Vercel will automatically deploy it in 1-2 minutes.

Check deployment status: https://vercel.com/school11220/tradesim

---

## 📊 INITIALIZE PRODUCTION DATABASE

You need to initialize the production database (Neon PostgreSQL) with stocks and event data.

### **Option 1: Using Django Management Command (RECOMMENDED)**

SSH into your Vercel deployment or use Vercel CLI:

```bash
# If you have vercel CLI installed:
vercel env pull
python manage.py init_trading_platform
```

### **Option 2: Using Django Shell in Production**

Run this Python code in your production environment:

```python
import os
os.environ['DATABASE_URL'] = 'your-neon-postgres-url'  # Already in env vars

from app1.management.commands.init_trading_platform import Command
command = Command()
command.handle()
```

### **Option 3: Direct SQL in Neon Console (QUICK & EASY)**

Go to your Neon dashboard and run this SQL script:

1. **Create the Event:**
```sql
INSERT INTO app1_event (name, description, start_time, end_time, initial_capital, registration_open, is_active, status, created_at, updated_at)
VALUES (
    'Stock Trading Competition 2025',
    'Annual stock trading competition for teams',
    NOW(),
    NOW() + INTERVAL '30 days',
    100000.00,
    true,
    true,
    'active',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;
```

2. **Create Settings:**
```sql
INSERT INTO app1_simulatorsettings (setting_name, setting_value, description)
VALUES 
    ('default_user_balance', '10000', 'Default balance for new users'),
    ('default_team_balance', '100000', 'Default balance for new teams')
ON CONFLICT (setting_name) DO NOTHING;
```

3. **Create All 63 Stocks:** (This is a large script - see below)

<details>
<summary>Click to expand: SQL for all 63 stocks</summary>

```sql
-- Technology Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, price_change, price_change_percent, volume, market_cap, is_active, last_updated) VALUES
('AAPL', 'Apple Inc.', 'Technology', 150.50, 148.20, 2.30, 1.55, 50000000, 2500000000000, true, NOW()),
('MSFT', 'Microsoft Corporation', 'Technology', 320.75, 318.50, 2.25, 0.71, 25000000, 2400000000000, true, NOW()),
('GOOGL', 'Alphabet Inc.', 'Technology', 125.80, 124.30, 1.50, 1.21, 20000000, 1600000000000, true, NOW()),
('META', 'Meta Platforms Inc.', 'Technology', 305.25, 302.10, 3.15, 1.04, 15000000, 800000000000, true, NOW()),
('NVDA', 'NVIDIA Corporation', 'Technology', 455.60, 450.20, 5.40, 1.20, 40000000, 1100000000000, true, NOW()),
('ADBE', 'Adobe Inc.', 'Technology', 535.80, 532.40, 3.40, 0.64, 3000000, 250000000000, true, NOW()),
('CRM', 'Salesforce Inc.', 'Technology', 215.30, 213.80, 1.50, 0.70, 5000000, 210000000000, true, NOW()),
('ORCL', 'Oracle Corporation', 'Technology', 98.45, 97.20, 1.25, 1.29, 8000000, 270000000000, true, NOW()),
('AMD', 'Advanced Micro Devices', 'Technology', 112.45, 110.80, 1.65, 1.49, 35000000, 180000000000, true, NOW()),

-- Healthcare Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, price_change, price_change_percent, volume, market_cap, is_active, last_updated) VALUES
('JNJ', 'Johnson & Johnson', 'Healthcare', 165.40, 164.20, 1.20, 0.73, 10000000, 435000000000, true, NOW()),
('UNH', 'UnitedHealth Group', 'Healthcare', 485.90, 483.50, 2.40, 0.50, 3000000, 460000000000, true, NOW()),
('PFE', 'Pfizer Inc.', 'Healthcare', 32.75, 32.40, 0.35, 1.08, 25000000, 185000000000, true, NOW()),
('ABT', 'Abbott Laboratories', 'Healthcare', 115.45, 114.30, 1.15, 1.01, 5000000, 200000000000, true, NOW()),
('TMO', 'Thermo Fisher Scientific', 'Healthcare', 520.30, 518.70, 1.60, 0.31, 1500000, 205000000000, true, NOW()),
('MRK', 'Merck & Co.', 'Healthcare', 108.65, 107.80, 0.85, 0.79, 8000000, 275000000000, true, NOW()),
('ABBV', 'AbbVie Inc.', 'Healthcare', 155.70, 154.50, 1.20, 0.78, 6000000, 275000000000, true, NOW()),
('LLY', 'Eli Lilly and Company', 'Healthcare', 585.25, 582.40, 2.85, 0.49, 3000000, 555000000000, true, NOW()),
('BMY', 'Bristol-Myers Squibb', 'Healthcare', 58.90, 58.40, 0.50, 0.86, 9000000, 120000000000, true, NOW()),

-- Financial Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, price_change, price_change_percent, volume, market_cap, is_active, last_updated) VALUES
('JPM', 'JPMorgan Chase & Co.', 'Financial', 145.80, 144.50, 1.30, 0.90, 12000000, 425000000000, true, NOW()),
('BAC', 'Bank of America Corp', 'Financial', 32.45, 32.10, 0.35, 1.09, 45000000, 260000000000, true, NOW()),
('WFC', 'Wells Fargo & Company', 'Financial', 45.75, 45.30, 0.45, 0.99, 20000000, 165000000000, true, NOW()),
('GS', 'Goldman Sachs Group', 'Financial', 365.20, 363.50, 1.70, 0.47, 2500000, 125000000000, true, NOW()),
('MS', 'Morgan Stanley', 'Financial', 88.90, 88.20, 0.70, 0.79, 8000000, 145000000000, true, NOW()),
('BLK', 'BlackRock Inc.', 'Financial', 785.40, 782.30, 3.10, 0.40, 500000, 120000000000, true, NOW()),
('SCHW', 'Charles Schwab Corp', 'Financial', 68.55, 68.10, 0.45, 0.66, 6000000, 125000000000, true, NOW()),
('AXP', 'American Express', 'Financial', 175.30, 174.20, 1.10, 0.63, 3000000, 130000000000, true, NOW()),
('C', 'Citigroup Inc.', 'Financial', 52.80, 52.40, 0.40, 0.76, 15000000, 100000000000, true, NOW()),

-- Consumer Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, price_change, price_change_percent, volume, market_cap, is_active, last_updated) VALUES
('AMZN', 'Amazon.com Inc.', 'Consumer', 135.60, 134.20, 1.40, 1.04, 50000000, 1400000000000, true, NOW()),
('TSLA', 'Tesla Inc.', 'Consumer', 242.85, 240.50, 2.35, 0.98, 100000000, 770000000000, true, NOW()),
('HD', 'Home Depot Inc.', 'Consumer', 315.70, 314.20, 1.50, 0.48, 4000000, 325000000000, true, NOW()),
('MCD', 'McDonald\'s Corporation', 'Consumer', 285.45, 284.30, 1.15, 0.40, 3000000, 210000000000, true, NOW()),
('NKE', 'Nike Inc.', 'Consumer', 108.90, 107.80, 1.10, 1.02, 8000000, 165000000000, true, NOW()),
('SBUX', 'Starbucks Corporation', 'Consumer', 95.75, 95.20, 0.55, 0.58, 7000000, 110000000000, true, NOW()),
('TGT', 'Target Corporation', 'Consumer', 145.60, 144.80, 0.80, 0.55, 5000000, 67000000000, true, NOW()),
('LOW', 'Lowe\'s Companies', 'Consumer', 225.30, 224.50, 0.80, 0.36, 3000000, 140000000000, true, NOW()),
('COST', 'Costco Wholesale', 'Consumer', 565.80, 564.20, 1.60, 0.28, 2000000, 250000000000, true, NOW()),

-- Industrial Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, price_change, price_change_percent, volume, market_cap, is_active, last_updated) VALUES
('BA', 'Boeing Company', 'Industrial', 185.45, 184.30, 1.15, 0.62, 8000000, 115000000000, true, NOW()),
('CAT', 'Caterpillar Inc.', 'Industrial', 285.90, 284.50, 1.40, 0.49, 3000000, 150000000000, true, NOW()),
('GE', 'General Electric', 'Industrial', 115.60, 114.90, 0.70, 0.61, 50000000, 127000000000, true, NOW()),
('MMM', '3M Company', 'Industrial', 98.75, 98.20, 0.55, 0.56, 3000000, 55000000000, true, NOW()),
('HON', 'Honeywell International', 'Industrial', 195.40, 194.60, 0.80, 0.41, 2500000, 130000000000, true, NOW()),
('UPS', 'United Parcel Service', 'Industrial', 165.80, 165.20, 0.60, 0.36, 3000000, 145000000000, true, NOW()),
('LMT', 'Lockheed Martin', 'Industrial', 445.30, 444.20, 1.10, 0.25, 1000000, 115000000000, true, NOW()),
('RTX', 'Raytheon Technologies', 'Industrial', 92.65, 92.30, 0.35, 0.38, 5000000, 135000000000, true, NOW()),
('DE', 'Deere & Company', 'Industrial', 385.70, 384.90, 0.80, 0.21, 1500000, 110000000000, true, NOW()),

-- Energy Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, price_change, price_change_percent, volume, market_cap, is_active, last_updated) VALUES
('XOM', 'Exxon Mobil Corporation', 'Energy', 108.45, 107.80, 0.65, 0.60, 20000000, 450000000000, true, NOW()),
('CVX', 'Chevron Corporation', 'Energy', 155.70, 155.10, 0.60, 0.39, 8000000, 295000000000, true, NOW()),
('COP', 'ConocoPhillips', 'Energy', 118.90, 118.40, 0.50, 0.42, 6000000, 150000000000, true, NOW()),
('SLB', 'Schlumberger Limited', 'Energy', 52.35, 52.10, 0.25, 0.48, 10000000, 75000000000, true, NOW()),
('EOG', 'EOG Resources', 'Energy', 125.80, 125.30, 0.50, 0.40, 3000000, 73000000000, true, NOW()),
('PXD', 'Pioneer Natural Resources', 'Energy', 235.60, 235.10, 0.50, 0.21, 1500000, 57000000000, true, NOW()),
('MPC', 'Marathon Petroleum', 'Energy', 165.45, 165.00, 0.45, 0.27, 4000000, 67000000000, true, NOW()),
('VLO', 'Valero Energy', 'Energy', 135.90, 135.50, 0.40, 0.30, 3000000, 48000000000, true, NOW()),
('PSX', 'Phillips 66', 'Energy', 125.70, 125.40, 0.30, 0.24, 2500000, 57000000000, true, NOW()),

-- Communication Stocks
INSERT INTO app1_stock (symbol, name, sector, current_price, previous_close, price_change, price_change_percent, volume, market_cap, is_active, last_updated) VALUES
('T', 'AT&T Inc.', 'Communication', 18.45, 18.35, 0.10, 0.54, 40000000, 130000000000, true, NOW()),
('VZ', 'Verizon Communications', 'Communication', 42.80, 42.60, 0.20, 0.47, 20000000, 180000000000, true, NOW()),
('CMCSA', 'Comcast Corporation', 'Communication', 45.65, 45.50, 0.15, 0.33, 15000000, 185000000000, true, NOW()),
('DIS', 'Walt Disney Company', 'Communication', 95.85, 95.60, 0.25, 0.26, 12000000, 175000000000, true, NOW()),
('NFLX', 'Netflix Inc.', 'Communication', 425.70, 424.90, 0.80, 0.19, 8000000, 185000000000, true, NOW()),
('TMUS', 'T-Mobile US Inc.', 'Communication', 155.40, 155.10, 0.30, 0.19, 5000000, 185000000000, true, NOW());
```
</details>

---

## 🧪 CREATE TEST TEAM IN PRODUCTION

After initializing the database, create a test team by going to:
**https://tradesim-lyart.vercel.app/team/signup**

Or use Django shell in production to create one programmatically.

---

## ✅ VERIFICATION CHECKLIST

After deployment, verify:

- [ ] Visit: https://tradesim-lyart.vercel.app/admin
  - [ ] Login works
  - [ ] Can view Stocks page (should show 66 stocks)
  - [ ] Can view Teams page
  - [ ] Can view Events page
  - [ ] Can view Users page
  
- [ ] Visit: https://tradesim-lyart.vercel.app/team/signup
  - [ ] Can register a new team
  
- [ ] Visit: https://tradesim-lyart.vercel.app/team/login
  - [ ] Can login with team credentials
  
- [ ] After team login:
  - [ ] /team/stocks shows all 66 stocks in grid
  - [ ] /team/portfolio shows portfolio (empty at first)
  - [ ] Can click on a stock and trade it
  - [ ] /team/dashboard shows team info

---

## 🎯 QUICK START (TL;DR)

1. ✅ Code is deployed (Vercel auto-deploys from GitHub)
2. ⏳ Initialize production database:
   - Go to Neon Console
   - Run the SQL scripts above (Event, Settings, Stocks)
3. ✅ Create a test team at /team/signup
4. ✅ Test everything works!

---

## 📞 SUPPORT

If you encounter any issues:
1. Check Vercel deployment logs
2. Check Neon database connection
3. Verify environment variables are set correctly
4. Run migrations: `python manage.py migrate`

