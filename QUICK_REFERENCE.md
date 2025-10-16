# TradeSim Quick Reference

## Server Running
```bash
cd /home/shivam/Investa
/home/shivam/Investa/venv/bin/python manage.py runserver
```
Server: http://127.0.0.1:8000

## Team Pages

### Browse Stocks
URL: `/team/stocks`
- Grid layout with stock cards
- Real-time updates every 15s
- Search functionality
- Shows owned stocks
- Blue professional theme

### Portfolio
URL: `/team/portfolio`
- Summary cards (Balance, Value, Investment, P&L)
- Holdings table
- Real-time calculations
- Auto-refresh every 20s

### Trade
URL: `/team/trade/<symbol>`
- Buy/sell interface
- Quantity presets
- Real-time cost calculator

## Real-Time Updates

**Browse Stocks:**
- Auto-refresh: 15 seconds
- Manual refresh button
- Flash animation on price changes
- Green flash = price up
- Red flash = price down

**Portfolio:**
- Auto-refresh: 20 seconds
- Manual refresh button
- Recalculates P&L on each update
- Updates summary cards

## Color Scheme
```
Primary: #1e40af (Blue)
Success: #10b981 (Green)
Danger: #ef4444 (Red)
Warning: #f59e0b (Orange)
```

## Navigation
All team pages have consistent nav:
- 🏠 Dashboard
- 📈 Browse Stocks
- 💼 Portfolio  
- 🚪 Logout

## Files Structure
```
templates/main/
├── team_base.html          # Navigation & layout
├── team_stocks.html        # Browse stocks (NEW)
├── team_portfolio.html     # Portfolio view (NEW)
├── team_trade.html         # Trading page
└── team_dashboard.html     # Dashboard
```

## Deploy to Production

1. **Commit changes:**
```bash
git add .
git commit -m "Frontend overhaul: TradeSim branding, real-time updates, new UI"
git push
```

2. **Vercel will auto-deploy**

3. **Run price updater on server:**
```bash
python manage.py update_stock_prices --continuous --interval 30
```

4. **Test URLs:**
- https://your-domain.vercel.app/team/login
- https://your-domain.vercel.app/team/stocks
- https://your-domain.vercel.app/team/portfolio

## Quick Test Checklist

✅ Login as team
✅ Browse stocks page loads
✅ Search works
✅ Prices update (wait 15s)
✅ Portfolio shows holdings
✅ P&L calculates correctly
✅ Trade page works
✅ Mobile responsive
✅ TradeSim branding visible

---

**Everything is working! 🎉**
