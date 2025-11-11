# 🎯 TEAM DASHBOARD FILES LOCATION

## 📁 Template Files (Frontend)

### 1. **Team Login Page**
**File:** `templates/login/team_login.html`
- Login form with team code and password
- TradeWars branding
- Redirects to team dashboard after login

### 2. **Team Dashboard** 
**File:** `templates/main/team_dashboard.html`
- Main dashboard after login
- Shows team balance, P&L, top performers
- Quick trade section
- Market status

### 3. **Team Portfolio**
**File:** `templates/main/team_portfolio.html`
- Shows all team holdings
- Real-time P&L calculations
- Current value, gains/losses
- Sector allocation charts

### 4. **Team Signup**
**File:** `templates/login/team_signup.html`
- New team registration
- Team name, password, event selection

### 5. **Base Template**
**File:** `templates/main/team_base.html`
- Shared layout for all team pages
- Navigation bar with Dashboard, Browse Stocks, Portfolio, News
- Footer and common styles

---

## 🐍 View Functions (Backend)

### Location: `app1/views.py`

1. **Team Login View:** `team_login()` (around line 750)
2. **Team Dashboard View:** `team_dashboard()` (around line 800)
3. **Team Portfolio View:** `team_portfolio()` (around line 900)
4. **Team News View:** `team_news()` (around line 960)

---

## 🔧 URL Routes

### Location: `app1/urls.py`

```python
# Team Auth
path("team/login", team_login, name="team_login")
path("team/signup", team_signup, name="team_signup")
path("team/dashboard", team_dashboard, name="team_dashboard")
path("team/logout", team_logout, name="team_logout")

# Team Trading
path("team/stocks", team_stocks, name="team_stocks")
path("team/trade/<str:symbol>", team_trade, name="team_trade")
path("team/portfolio", team_portfolio, name="team_portfolio")
path("team/news", team_news, name="team_news")
```

---

## 📊 Models (Database)

### Location: `app1/models.py`

1. **Team Model:** Line ~150-230
2. **Event Model:** Line ~115-150
3. **MarketNews Model:** Line ~232-323
4. **Stock Model:** Line ~35-78

---

## 🎨 Styling

All team pages use inline CSS in their respective templates or inherit from `team_base.html`.

**Theme:**
- Primary: Blue gradient (#1e40af to #1e3a8a)
- Success: Green (#10b981)
- Danger: Red (#ef4444)
- Background: Light gray (#f8fafc)
