# 🏆 TradeSim Competition Platform - Complete Design

## 🎯 Event Overview
A live stock trading competition where:
- **Admin** controls the entire event (start/stop, prices, rules)
- **Teams** compete to maximize portfolio value
- **Real-time leaderboard** shows rankings
- **Winner** is determined by highest portfolio value at event end

---

## 📋 Feature Breakdown

### 1. Event Management System

**Event Model:**
```python
class Event(models.Model):
    name = models.CharField(max_length=200)  # "Spring Trading Challenge 2025"
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    initial_capital = models.DecimalField(default=100000)  # $100,000 per team
    is_active = models.BooleanField(default=False)
    registration_open = models.BooleanField(default=True)
    allow_short_selling = models.BooleanField(default=False)
    max_trades_per_team = models.IntegerField(null=True, blank=True)
    trading_fee_percentage = models.DecimalField(default=0)  # 0% = free trading
```

**Admin Controls:**
- ✅ Create multiple events
- ✅ Set start/end times
- ✅ Control registration open/closed
- ✅ Start/stop event with one click
- ✅ Adjust initial capital anytime
- ✅ Configure trading rules

---

### 2. Team Registration System

**Team Model:**
```python
class Team(models.Model):
    event = models.ForeignKey(Event)
    team_name = models.CharField(max_length=100)
    team_code = models.CharField(unique=True)  # Auto-generated: TEAM-A3B9
    leader_name = models.CharField(max_length=100)
    leader_email = models.EmailField()
    members = models.JSONField()  # ['Member 1', 'Member 2', 'Member 3']
    balance = models.DecimalField()
    portfolio = models.JSONField()  # {stock: {quantity, avg_price}}
    total_trades = models.IntegerField(default=0)
    registration_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
```

**Registration Flow:**
1. Team visits `/register`
2. Fills form: team name, leader info, member names
3. System generates unique team code (e.g., `TEAM-X7K2`)
4. Team receives code via email/display
5. Team logs in with team code + password

**Benefits:**
- No need for individual user accounts
- Easy team management
- Unique codes prevent confusion
- Admin can bulk import teams

---

### 3. Expanded Stock Database

**50+ Real Companies Across Sectors:**

**Technology (15):**
- AAPL - Apple Inc.
- MSFT - Microsoft
- GOOG - Alphabet
- META - Meta Platforms
- AMZN - Amazon
- TSLA - Tesla
- NVDA - NVIDIA
- ORCL - Oracle
- INTC - Intel
- AMD - Advanced Micro Devices
- CRM - Salesforce
- ADBE - Adobe
- CSCO - Cisco
- IBM - IBM
- NFLX - Netflix

**Finance (10):**
- JPM - JPMorgan Chase
- BAC - Bank of America
- WFC - Wells Fargo
- GS - Goldman Sachs
- MS - Morgan Stanley
- V - Visa
- MA - Mastercard
- AXP - American Express
- BLK - BlackRock
- SCHW - Charles Schwab

**Healthcare (8):**
- JNJ - Johnson & Johnson
- PFE - Pfizer
- UNH - UnitedHealth
- ABBV - AbbVie
- TMO - Thermo Fisher
- MRK - Merck
- ABT - Abbott
- BMY - Bristol Myers

**Energy (7):**
- XOM - Exxon Mobil
- CVX - Chevron
- COP - ConocoPhillips
- SLB - Schlumberger
- EOG - EOG Resources
- MPC - Marathon Petroleum
- PSX - Phillips 66

**Consumer (10):**
- WMT - Walmart
- HD - Home Depot
- MCD - McDonald's
- NKE - Nike
- SBUX - Starbucks
- TGT - Target
- LOW - Lowe's
- TJX - TJX Companies
- DG - Dollar General
- COST - Costco

---

### 4. Admin Dashboard Features

**Main Control Panel:**
```
┌─────────────────────────────────────────────┐
│  📊 Event: Spring Trading Challenge 2025   │
│  ⏰ Time Remaining: 02:34:18               │
│  👥 Active Teams: 24                       │
│  💹 Total Trades: 1,247                    │
└─────────────────────────────────────────────┘

[▶️ START EVENT]  [⏸️ PAUSE TRADING]  [🏁 END EVENT]

📈 Live Leaderboard (Top 5)
1. Team Alpha         $187,450  (+87.5%)
2. Team Quantum       $165,230  (+65.2%)
3. Team Bulls         $142,890  (+42.9%)
4. Team Phoenix       $138,700  (+38.7%)
5. Team Nexus         $125,400  (+25.4%)

🎛️ Quick Actions:
• Adjust Stock Price    • Reset Team Balance
• Freeze Specific Team  • Broadcast Announcement
• Export Leaderboard    • View Trading Activity

📊 Statistics:
• Most Traded: TSLA (234 trades)
• Biggest Gainer: Team Alpha (+$87,450)
• Most Active: Team Bulls (89 trades)
```

**Stock Price Control:**
- Real-time or manual price updates
- Bulk price adjustments
- Market events (crash simulation, bull run)
- Freeze specific stocks

**Team Management:**
- View all team portfolios
- Reset specific team
- Disqualify team (if rules broken)
- Add bonus/penalty to balance

---

### 5. Real-Time Leaderboard

**Public Leaderboard Page (`/leaderboard`):**
```
🏆 SPRING TRADING CHALLENGE 2025 - LIVE RANKINGS

⏱️ Event Ends In: 02:34:18

┌──────┬─────────────────┬──────────────┬─────────────┬──────────┐
│ Rank │ Team Name       │ Portfolio    │ Profit/Loss │ Trades   │
├──────┼─────────────────┼──────────────┼─────────────┼──────────┤
│  🥇  │ Team Alpha      │ $187,450.00  │ +87.5% 📈  │ 67       │
│  🥈  │ Team Quantum    │ $165,230.00  │ +65.2% 📈  │ 54       │
│  🥉  │ Team Bulls      │ $142,890.00  │ +42.9% 📈  │ 89       │
│  4   │ Team Phoenix    │ $138,700.00  │ +38.7% 📈  │ 45       │
│  5   │ Team Nexus      │ $125,400.00  │ +25.4% 📈  │ 71       │
│  6   │ Team Warriors   │ $118,230.00  │ +18.2% 📈  │ 38       │
│  7   │ Team Sigma      │ $112,450.00  │ +12.5% 📈  │ 52       │
│  8   │ Team Delta      │ $105,670.00  │ +5.7% 📈   │ 61       │
│  9   │ Team Nova       │ $98,340.00   │ -1.7% 📉   │ 44       │
│  10  │ Team Apex       │ $87,560.00   │ -12.4% 📉  │ 33       │
└──────┴─────────────────┴──────────────┴─────────────┴──────────┘

🔄 Auto-refreshes every 5 seconds
```

**Features:**
- Color-coded P/L (green = profit, red = loss)
- Medal icons for top 3
- Auto-refresh without page reload
- Export to PDF/CSV
- Projector-friendly full-screen mode

---

### 6. Team Dashboard

**Team View (`/dashboard`):**
```
👥 Team Alpha                           🏆 Rank: #1 of 24

💰 Portfolio Value: $187,450.00
📊 Profit/Loss: +$87,450.00 (+87.5%)
💵 Available Cash: $45,230.00
📈 Holdings Value: $142,220.00

⏱️ Event Status: ACTIVE | Time Remaining: 02:34:18

─────────────────────────────────────────────────────

📦 YOUR HOLDINGS (7 stocks)

Stock     Qty    Avg Price   Current    Value      P/L
AAPL      50     $150.00     $175.50    $8,775    +$1,275 📈
TSLA      30     $200.00     $245.80    $7,374    +$1,374 📈
NVDA      40     $450.00     $520.30    $20,812   +$2,812 📈
MSFT      60     $280.00     $310.00    $18,600   +$1,800 📈
...

─────────────────────────────────────────────────────

🔍 AVAILABLE STOCKS (50+)

Search: [____________]  Filter: [All Sectors ▾]

Symbol  Company          Price      Change    Action
AAPL    Apple Inc.       $175.50    +2.5% 📈  [BUY] [SELL]
TSLA    Tesla            $245.80    +5.2% 📈  [BUY] [SELL]
GOOG    Alphabet         $142.30    -0.8% 📉  [BUY] [SELL]
...

─────────────────────────────────────────────────────

📜 RECENT TRADES (Last 10)

Time      Type   Stock   Qty   Price     Total
14:23:45  BUY    NVDA    10    $520.30   $5,203.00
14:15:22  SELL   AAPL    20    $175.50   $3,510.00
...

─────────────────────────────────────────────────────

📊 YOUR RANKING TREND
[Chart showing position over time]
```

---

### 7. Trading Rules & Restrictions

**Configurable by Admin:**

1. **Trade Limits:**
   - Max trades per team: 100
   - Max trades per stock per day: 10
   - Min holding period: 5 minutes

2. **Position Limits:**
   - Max position per stock: 30% of portfolio
   - Max single trade value: $50,000

3. **Trading Costs:**
   - Transaction fee: 0.1% (optional)
   - No hidden costs by default

4. **Allowed Actions:**
   - ✅ Buy stocks
   - ✅ Sell stocks
   - ❌ Short selling (configurable)
   - ❌ Margin trading (configurable)
   - ❌ Options/derivatives

5. **Anti-Cheating:**
   - Log all trades with timestamps
   - Detect suspicious patterns
   - Admin can review any trade
   - Freeze team if needed

---

### 8. Event Lifecycle

**Phase 1: Registration (Before Event)**
```
├─ Admin creates event
├─ Sets start/end times
├─ Configures rules
├─ Opens registration
├─ Teams register
└─ Admin reviews registrations
```

**Phase 2: Pre-Event (30 min before)**
```
├─ Admin finalizes team list
├─ System initializes balances
├─ Countdown timer shows on all pages
├─ Teams can log in but not trade
└─ Leaderboard shows "Event Starting Soon"
```

**Phase 3: Live Event**
```
├─ Admin clicks "START EVENT"
├─ Trading enabled for all teams
├─ Live leaderboard updates
├─ Admin monitors in real-time
├─ Teams compete
└─ Prices updated (real-time or manual)
```

**Phase 4: Event End**
```
├─ Timer reaches 0:00:00 OR admin ends early
├─ Trading automatically disabled
├─ Final rankings calculated
├─ Winner announced
├─ Certificates/prizes generated
└─ Results exported
```

---

### 9. Additional Features

**For Teams:**
- 📱 Mobile-friendly interface
- 📊 Portfolio analytics charts
- 📜 Complete trade history
- 🔔 Notifications for rank changes
- 💡 Stock news feed (optional)

**For Admins:**
- 📈 Real-time analytics dashboard
- 📥 Export data (CSV, Excel, PDF)
- 📢 Broadcast announcements to all teams
- 🎥 Screen projection mode for leaderboard
- 🔒 Audit log of all admin actions

**For Spectators:**
- 🏆 Public leaderboard view
- 📊 Live statistics
- 🎬 Event replay after end
- 📱 QR code for mobile access

---

### 10. Tech Stack Enhancements

**Backend:**
- Django Channels for WebSocket (real-time updates)
- Redis for caching leaderboard
- Celery for scheduled tasks (price updates)
- PostgreSQL for robust transactions

**Frontend:**
- HTMX for dynamic updates (lightweight)
- Chart.js for portfolio graphs
- Tailwind CSS (already using)
- Alpine.js for interactive components

**Deployment:**
- Vercel (current) + Redis Cloud
- OR migrate to Railway/Render for WebSocket support

---

## 🎬 Implementation Plan

### Quick Win Version (2-3 hours)
✅ Add Event model
✅ Team registration
✅ Expand to 50+ stocks
✅ Basic leaderboard
✅ Admin start/stop controls

### Full Version (1-2 days)
✅ All features listed above
✅ Real-time WebSocket updates
✅ Advanced analytics
✅ Mobile optimization
✅ Complete testing

---

## 🚀 Suggested Flow for Your Event

### Before Event Day:
1. **Create event** in admin panel
2. **Send registration link** to participants
3. **Teams register** with team details
4. **Admin reviews** and approves teams
5. **Test trading** with a practice event

### Event Day:
1. **10 min before:** Final announcements
2. **Click START:** Trading begins
3. **Monitor:** Watch leaderboard live
4. **During event:** Can adjust prices, pause if needed
5. **Event ends:** Trading stops automatically
6. **Winner announcement:** Top 3 teams displayed

### After Event:
1. **Export results**
2. **Generate certificates**
3. **Share leaderboard screenshot**
4. **Analyze team strategies**

---

## 📊 Sample Event Configuration

```python
Event: "TechFest 2025 Trading Challenge"
Duration: 3 hours
Initial Capital: $100,000 per team
Teams: 30
Stocks: 50+
Rules:
  - Max 5 trades per minute
  - Max 30% in single stock
  - No short selling
  - Real-time price updates every 30 seconds
Prize: Top 3 teams
```

---

## 🎯 Key Success Factors

1. **Simple Registration:** Teams register in < 2 minutes
2. **Clear Rules:** Display rules prominently
3. **Visible Leaderboard:** Large screen projection
4. **Admin Control:** One-click start/stop
5. **Fair Pricing:** Use real Yahoo Finance data OR manual control
6. **Engagement:** Show live updates, rank changes
7. **Winner Clarity:** Automatic calculation, no disputes

---

## 🔥 Pro Tips

1. **Use Real Data:** Yahoo Finance API for live prices
2. **OR Manual Mode:** Admin controls all prices (more fun!)
3. **Practice Run:** Do a 30-min test event first
4. **Backup Plan:** Have fallback if tech issues
5. **Engage Audience:** Show leaderboard on projector
6. **Prizes:** Make it exciting with good prizes
7. **Photos:** Capture winner moments
8. **Feedback:** Survey teams after event

---

Would you like me to start implementing this? I'll begin with:
1. ✅ Event and Team models
2. ✅ Team registration page
3. ✅ 50+ stocks initialization
4. ✅ Admin dashboard with start/stop
5. ✅ Basic leaderboard

This will give you a working competition platform quickly!
