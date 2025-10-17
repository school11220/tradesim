# 📈 Investa - Stock Market Simulator

A Django-based stock market trading simulator with **full admin control** over stock prices and user balances. Perfect for learning, testing trading strategies, or running simulated trading competitions.

## ✨ Key Features

### For Administrators
- 🎛️ **Control Stock Prices**: Set and adjust stock prices manually through admin panel
- 💰 **Manage User Balances**: View, modify, and reset user balances
- ⚙️ **Configure Settings**: Set default starting balance and trading parameters
- 📊 **Bulk Actions**: Update multiple stocks or users at once
- 🔄 **Real-time Updates**: Changes reflect immediately for all users

### For Users

* **Create Your Account:** Sign up to start using Investa.
* **Demo Money:** Once registered, you'll receive $10,000 in virtual money to begin trading.
* **Buying Stocks:** Use your demo money to buy stocks. Simply search for the stocks you're interested in, and purchase them directly from your personalized dashboard.
* **Real-Time Updates:** Stock prices update automatically using realistic market simulation with sentiment and sector correlations, providing dynamic market data without external APIs.
* **Track Your Portfolio:** Monitor your assets and watch their performance over time. Your interactive dashboard makes it easy to see how your investments are doing and make informed decisions.

## Dashboard
Dashboard displays a watchlist with an interactive graph, a portfolio overview of the holding stocks, and the total stock allocation. 
Your Investa dashboard is your personal trading hub! Here's what it shows:

* **Total Balance:** See the total value of your account, investments.
* **Profit/Loss:** Track your overall gains or losses in real-time.
* **Market Status:** Know whether the market is closed, regular, pre-market, or post-market.
* **Watchlist:** Keep an eye on the stocks you're interested in.
* **Watchlist Graphs:** Visualize the performance of stocks on your watchlist.
* **Portfolio Overview:** Get a detailed summary of all your investments.
* **Asset Allocations:** See how your investments are distributed across different assets.

![Home Page](images/dashboard.png)

## Details (Buy/Sell) Page
This page allows users to monitor graphs and live stock prices, as well as buy and trade virtual stocks.
The search page is your go-to for detailed stock information and trading. Here's what you can do:

* **View Stock Details:** See the current price, previous close, and detailed stats like 52-week high/low, market day high/low.
* **Real-Time Price Chart:** Track the stock's performance with an up-to-date price chart.
* **Market Status:** Know whether the market is closed or open.
* **Buy/Sell Stocks:** If you hold stocks, you can easily buy or sell directly from this page.
* **Watchlist:** Add stocks to your watchlist for future tracking.

![Search Page](images/searchPage.png)

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/sakshamssr/Investa.git
cd Investa

# 2. Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Initialize simulator with default stocks
python manage.py init_simulator

# 5. Create admin account
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Start development server
python manage.py runserver
```

**Access the app:**
- Main app: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 🎮 Admin Controls

After logging into `/admin`, you can:

### Control Stock Prices
1. Navigate to **Stocks** section
2. Click any stock to edit its price manually
3. Use bulk actions:
   - Increase/decrease prices by 10%
   - Activate/deactivate stocks
   - Reset price changes

### Manage User Balances
1. Navigate to **Users** section
2. View all user balances and holdings
3. Use bulk actions:
   - Reset balance to default
   - Add $1,000 or $5,000 bonus
   - Or edit individual balances directly

### Configure Settings
1. Navigate to **Simulator Settings**
2. Set `default_user_balance` (default: $10,000)
3. Configure trading fees and other parameters

## ☁️ Deploy to Vercel

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

**Quick deploy:**
1. Push to GitHub
2. Connect to Vercel
3. Add environment variables (DATABASE_URL, SECRET_KEY, etc.)
4. Run migrations on production database
5. Create admin account and initialize stocks

## 🗄️ Database Models

- **User**: Balance, holdings (stockbuy), watchlist, trading history
- **Stock**: Symbol, name, current_price, previous_close, is_active
- **SimulatorSettings**: Global settings like default_user_balance
5. Access the application by visiting http://localhost:8000 in your web browser.
```
http://localhost:8000
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

