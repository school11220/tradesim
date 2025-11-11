# TradeWars - Quick Admin Reference 🚀

## 📊 Stock Management

### View All Stocks
**URL**: `/admin/app1/stock/`
- Browse all 188 stocks across 10 sectors
- Search by symbol or name
- Filter by sector or active status
- Sort by any column

---

## 💰 Price Control Methods

### Method 1: Custom Price Control Panel
**URL**: `/admin/app1/stock/custom-price-control/`

**Use Case**: Set exact prices for multiple stocks at once

**Steps**:
1. Click "Custom Price Control" button on stocks admin page
2. Enter desired price for each stock
3. Click "Update Individual Prices"
4. Stocks update immediately

**Pro Tip**: Leave fields blank for stocks you don't want to change

---

### Method 2: Sector Control Panel
**URL**: `/admin/app1/stock/sector-control/`

**Use Case**: Adjust entire sectors by percentage

**Steps**:
1. Click "Sector Control" button on stocks admin page
2. Enter percentage for each sector (e.g., `5` for +5%, `-3` for -3%)
3. Click "Update Sector Prices"
4. All stocks in those sectors adjust proportionally

**Example**:
- Technology: `10` → All tech stocks increase by 10%
- Energy: `-5` → All energy stocks decrease by 5%
- Healthcare: (leave blank) → No change

**Sectors Available**:
- Technology (28 stocks)
- Healthcare (20 stocks)
- Financial (20 stocks)
- Consumer (20 stocks)
- Energy (20 stocks)
- Industrial (20 stocks)
- Telecommunications (15 stocks)
- Real Estate (15 stocks)
- Materials (15 stocks)
- Utilities (15 stocks)

---

### Method 3: Admin Action (Custom Percentage)
**Use Case**: Apply percentage to selected specific stocks

**Steps**:
1. Go to stocks admin page `/admin/app1/stock/`
2. Check boxes next to stocks you want to adjust
3. Select "Apply custom percentage change" from Actions dropdown
4. Click "Go"
5. Enter percentage (positive or negative)
6. Click "Apply"

**Example**:
- Select AAPL, MSFT, GOOGL
- Action: Apply custom percentage change
- Enter: `7.5`
- Result: These 3 stocks increase by 7.5%

---

## 📰 Market News Management

### Create News
**URL**: `/admin/app1/marketnews/add/`

**Required Fields**:
- **Title**: Catchy headline (e.g., "Tech Sector Surges on AI Breakthrough")
- **Content**: Detailed description (2-3 paragraphs recommended)
- **Impact Direction**: 
  - `positive` → Green indicator
  - `negative` → Red indicator
  - `neutral` → Blue indicator
  - `mixed` → Orange indicator
- **Severity**:
  - `low` → Minor market movement
  - `medium` → Moderate impact
  - `high` → Significant impact
  - `critical` → Major market event

**Optional Fields**:
- **Affected Sectors**: JSON array format: `["Technology", "Healthcare"]`
- **Affected Stocks**: JSON array format: `["AAPL", "MSFT", "GOOGL"]`
- **Trading Hint**: Guidance for traders (e.g., "Consider buying tech stocks before close")
- **Published At**: When to display (default: now)
- **Expires At**: When to hide (optional)
- **Is Active**: Checkbox to publish/unpublish

### News Examples

#### Positive Tech News
```
Title: Apple Announces Record Q4 Earnings
Impact: positive
Severity: high
Affected Sectors: ["Technology"]
Affected Stocks: ["AAPL"]
Trading Hint: Strong buy signal for AAPL and related tech stocks
```

#### Negative Energy News
```
Title: Oil Prices Drop Amid Supply Concerns
Impact: negative
Severity: medium
Affected Sectors: ["Energy"]
Affected Stocks: ["XOM", "CVX", "COP"]
Trading Hint: Consider taking profits on energy positions
```

#### Mixed Market News
```
Title: Fed Announces Interest Rate Decision
Impact: mixed
Severity: critical
Affected Sectors: ["Financial", "Real Estate", "Utilities"]
Trading Hint: Monitor rate-sensitive sectors closely
```

---

## 👥 Team Management

### View Teams
**URL**: `/admin/app1/team/`
- See all registered teams
- View portfolio values
- Check profit/loss
- See rankings

### Adjust Team Balance
1. Select team(s)
2. Choose action:
   - "Add 1000 dollar bonus"
   - "Add 5000 dollar bonus"  
   - "Reset balance to default"
3. Click "Go"

---

## ⚙️ Simulator Settings

### Default User Balance
**URL**: `/admin/app1/simulatorsettings/default_5Fuser_5Fbalance/change/`
- Change starting balance for new teams
- Default: $100,000
- Affects: New teams only (existing teams unchanged)

### Update Mode Settings
**URL**: `/admin/app1/simulatorsettings/`
- Configure price update intervals
- Set market volatility
- Control simulation parameters

---

## 🎯 Quick Commands

### Apply 5% Increase to Technology Sector
1. Go to Sector Control
2. Technology: `5`
3. Update

### Apply 10% Decrease to Energy Sector
1. Go to Sector Control
2. Energy: `-10`
3. Update

### Set AAPL to $200
1. Go to Custom Price Control
2. Find AAPL row
3. Enter `200`
4. Update Individual Prices

### Create Breaking News
1. Go to Market News → Add
2. Title: "Breaking: Major Tech Merger Announced"
3. Severity: `critical`
4. Impact: `positive`
5. Is Active: ✓
6. Save

---

## 📈 Monitoring

### Check Portfolio Performance
1. Go to Teams admin
2. View "Portfolio Value" column
3. View "Profit/Loss" column (color-coded)
4. View "P/L Percent" column

### View Active Events
1. Go to Events admin
2. Filter: Is Active = Yes
3. Check team count
4. Monitor registration status

---

## 🔍 Search & Filter

### Find Specific Stocks
- Use search box (symbol or name)
- Example: "Apple" or "AAPL"

### Filter by Sector
- Use sector filter dropdown
- Select one or multiple sectors

### Filter by Activity
- Active stocks only
- Inactive stocks only
- All stocks

---

## 💡 Pro Tips

1. **Sector Adjustments**: Use for market-wide trends
2. **Custom Prices**: Use for individual stock events
3. **Admin Actions**: Use for quick bulk adjustments on selected stocks
4. **News Timing**: Set Published At for future announcements
5. **Trading Hints**: Keep concise and actionable
6. **Severity**: Use 'critical' sparingly for maximum impact
7. **Affected Stocks**: List 3-5 most impacted stocks
8. **Affected Sectors**: Usually 1-2 sectors per news item

---

## 🚨 Common Scenarios

### Scenario: Tech Boom
1. Sector Control → Technology: `15`
2. Create News: "Tech Sector Rally Continues"
3. Impact: `positive`, Severity: `high`

### Scenario: Market Crash
1. Sector Control → All sectors: `-10` to `-20`
2. Create News: "Market Correction Underway"
3. Impact: `negative`, Severity: `critical`

### Scenario: Company Earnings
1. Custom Price Control → Find stock
2. Set new price (e.g., AAPL: `185`)
3. Create News: "Apple Beats Earnings Expectations"
4. Affected Stocks: `["AAPL"]`

### Scenario: Sector Rotation
1. Sector Control → Healthcare: `8`, Technology: `-5`
2. Create News: "Investors Rotate to Defensive Sectors"
3. Impact: `mixed`, Severity: `medium`

---

## 📱 Access Points

- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **Stock Admin**: `http://127.0.0.1:8000/admin/app1/stock/`
- **Custom Price Control**: `http://127.0.0.1:8000/admin/app1/stock/custom-price-control/`
- **Sector Control**: `http://127.0.0.1:8000/admin/app1/stock/sector-control/`
- **Market News**: `http://127.0.0.1:8000/admin/app1/marketnews/`
- **Teams**: `http://127.0.0.1:8000/admin/app1/team/`

---

## 🎓 Learning Curve

**Beginner**: Start with Sector Control (simplest)
**Intermediate**: Use Custom Price Control for specific events
**Advanced**: Combine all methods + create coordinated news

---

## ✅ Best Practices

1. **Test Small**: Start with 1-2 stocks before bulk changes
2. **News First**: Create news before price changes for context
3. **Consistent Updates**: Update prices regularly for realism
4. **Clear Hints**: Make trading hints specific and actionable
5. **Severity Matters**: Use critical sparingly (once per week max)
6. **Track Changes**: Note what you changed for consistency
7. **Balance Sectors**: Don't favor one sector too long
8. **Team Fairness**: Give teams time to react to news

---

**Happy Trading! 📊💰**
