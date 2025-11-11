# 🎯 COMPLETE GUIDE: Stock Price Updates & Manual Controls

## 📊 How Price Updates Work

### Automatic Price Updates

**Frequency:** Every 5 minutes (12 times per hour)

**Method:** Simulated realistic price movements

**Volatility:** ±1.5% per update (configurable)

**Timeline:**
```
Time 0:00  → AAPL = $230.00
Time 0:05  → AAPL = $228.50 (-0.65%)
Time 0:10  → AAPL = $231.20 (+1.18%)
Time 0:15  → AAPL = $229.80 (-0.61%)
Time 0:20  → AAPL = $232.10 (+1.00%)
... continues every 5 minutes
```

### What Happens Each Update:

1. **GitHub Actions triggers** at :00, :05, :10, :15, :20, :25, etc.
2. **Calls API:** `https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.015`
3. **Each stock:**
   - Current price: $100
   - Random change: -1.5% to +1.5%
   - New price: $98.50 to $101.50
4. **Database updated** with new prices
5. **Teams see changes** immediately on next page refresh

---

## 🔧 Manual Price Controls (Admin Panel)

### Option 1: Custom Price for Individual Stock

**Steps:**
1. Go to: `/admin/app1/stock/`
2. Search for stock (e.g., AAPL)
3. Click on the stock name
4. Change "Current price" field
5. Click "Save"

**What Happens:**
- ✅ Price changes IMMEDIATELY
- ⏰ **Lasts maximum 5 minutes**
- 🔄 Next auto-update (5 min) will OVERWRITE your price
- 📉 New price will be based on your custom price ±1.5%

**Example:**
```
12:00 PM - You set AAPL to $250 (was $230)
12:05 PM - Auto-update: $250 → $248 (-0.8%)
12:10 PM - Auto-update: $248 → $251 (+1.2%)
12:15 PM - Auto-update: $251 → $249 (-0.8%)
... continues from there
```

**Use Case:** Quick shock to create trading opportunity

---

### Option 2: Sector-Wide Adjustment

**Steps:**
1. Go to: `/admin/app1/stock/`
2. Filter by sector (dropdown on right)
3. Select ALL stocks in that sector (checkboxes)
4. Actions dropdown → "Adjust prices by percentage"
5. Enter percentage (e.g., +5 for +5%)
6. Click "Go"

**What Happens:**
- ✅ All selected stocks change by that %
- ⏰ **Lasts maximum 5 minutes**
- 🔄 Next auto-update uses new prices as base

**Example:**
```
All Technology stocks:
AAPL: $230 → $241.50 (+5%)
MSFT: $380 → $399.00 (+5%)
GOOGL: $150 → $157.50 (+5%)

After 5 minutes (auto-update):
AAPL: $241.50 → $239.80 (-0.7%)
MSFT: $399.00 → $404.20 (+1.3%)
GOOGL: $157.50 → $159.90 (+1.5%)
```

**Use Case:** Simulate sector-wide market events

---

### Option 3: Bulk Custom Prices

**Steps:**
1. Go to: `/admin/app1/stock/`
2. Select multiple stocks (checkboxes)
3. Actions → "Set custom price"
4. Enter exact price for each
5. Click "Go"

**What Happens:**
- ✅ Each stock set to exact price
- ⏰ **Lasts maximum 5 minutes**
- 🔄 Auto-updates continue from new prices

---

## ⏰ Stabilization Timeline

### If You Manually Change a Price:

**Immediate Effect:**
- Teams see new price right away
- Can trade at that price

**Short Term (5 minutes):**
- Price stays at your set value
- Then first auto-update hits

**After First Auto-Update (5 min):**
- Price moves ±1.5% from your value
- Now following normal patterns

**Long Term (30+ minutes):**
- Price has moved 6+ times
- "Stabilized" at new baseline
- Market movement continues normally

### Stabilization Formula:

**Your manual change:** +5% ($230 → $241.50)

**Expected range after different times:**

| Time Elapsed | Updates | Price Range | Notes |
|--------------|---------|-------------|-------|
| 0 minutes | 0 | $241.50 | Your exact price |
| 5 minutes | 1 | $238-$245 | First auto-update |
| 10 minutes | 2 | $235-$248 | More variation |
| 30 minutes | 6 | $230-$255 | Significant drift |
| 1 hour | 12 | $225-$265 | Wide range possible |
| 2 hours | 24 | $210-$280 | Natural volatility |

**"Stabilized" means:** Price has undergone enough updates that your manual change is now just part of the historical data. The market is moving naturally again.

---

## 🎮 Recommended Event Strategies

### Strategy 1: Initial Shock + Natural Movement
**Best for creating trading opportunities**

1. **Before event:** Let prices run naturally
2. **Event starts:** Announce "market opens"
3. **15 min in:** Manually adjust sector (+5%)
4. **Announce:** "Tech sector rallies on AI news!"
5. **Let stabilize:** 20-30 minutes of natural movement
6. **Repeat:** Different sector at different times

**Why it works:** Creates clear trading signals, then prices normalize

---

### Strategy 2: News-Driven Price Changes
**Most realistic and engaging**

Instead of manual prices, use **Market News**:

1. Create news in admin: `/admin/app1/marketnews/`
2. Example: "Apple announces iPhone breakthrough"
3. Impact: Positive, Severity: High
4. Affected: ["AAPL"]
5. Teams see news → make trading decisions
6. Prices continue moving naturally

**Advantage:** Teams trade based on information, not just price changes

---

### Strategy 3: Market Volatility Periods
**For advanced traders**

**Calm Period (Normal volatility):**
- Volatility: 0.015 (±1.5%)
- Updates: Every 5 minutes
- Stable, predictable

**High Volatility Period:**
- Change workflow volatility to 0.03 (±3%)
- Announce: "Market volatility increases!"
- Prices swing more dramatically
- Change back after 1 hour

**How to change volatility:**
1. Edit: `.github/workflows/update-prices.yml`
2. Line 37: `volatility=0.015` → `volatility=0.03`
3. Commit and push
4. Next update uses new volatility

---

## 🎯 Specific Scenarios

### Scenario 1: "I want AAPL to crash 10%"

**Steps:**
1. Admin → Stocks → Search "AAPL"
2. Current price: $230
3. Set to: $207 (-10%)
4. Save

**Timeline:**
- **00:00** - You save: $207
- **00:05** - Auto: $204-$210 (±1.5% from $207)
- **00:10** - Auto: $201-$213 (cumulative)
- **00:30** - Auto: $195-$220 (6 updates, drifting)
- **01:00** - Auto: $190-$230 (could return to original!)

**To keep it low:** Create negative news about Apple instead

---

### Scenario 2: "I want entire Tech sector to boom"

**Steps:**
1. Admin → Stocks → Filter: Technology
2. Select all (21 stocks)
3. Actions → "Adjust by +8%"
4. Go

**Timeline:**
- **00:00** - All Tech +8% immediately
- **00:05** - Each stock: original+8% ±1.5%
- **00:30** - Stabilizing, some up, some down from new baseline
- **02:00** - Fully normalized, original +8% is now history

**Better approach:** 
- Create news: "AI Breakthrough Drives Tech Rally"
- Teams see news and rush to buy
- Natural supply/demand affects prices

---

### Scenario 3: "I want price to stay fixed for 30 minutes"

**Not possible with current system!** Auto-updates every 5 minutes.

**Workaround:**
1. **Disable auto-updates temporarily:**
   - Go to: https://github.com/school11220/tradesim/actions
   - Click workflow → "..." → "Disable workflow"
   
2. **Set your prices manually**

3. **Let teams trade for 30 minutes**

4. **Re-enable workflow:**
   - Go back to Actions
   - Enable workflow
   - Prices resume updating

**Warning:** No price changes = boring for teams!

---

### Scenario 4: "I want gradual increase over 2 hours"

**Not directly possible** - random updates don't guarantee direction

**Workaround - Staged Manual Updates:**

```
Hour 0:00 - Set AAPL to $230 (baseline)
Hour 0:30 - Set AAPL to $238 (+3.5%)
Hour 1:00 - Set AAPL to $246 (+7%)
Hour 1:30 - Set AAPL to $254 (+10.4%)
Hour 2:00 - Set AAPL to $262 (+14%)
```

Each gets 30 minutes to stabilize, then you bump it again.

**Better:** Create series of positive news items about Apple throughout event

---

## 📈 Understanding Price Volatility

### Current Setting: 0.015 (1.5%)

**Means:** Each 5-minute update, price can change by -1.5% to +1.5%

**Realistic?** YES - This mimics normal market behavior

**Examples:**

**Low Volatility (0.01 = 1%):**
- Very stable, boring
- Suitable for learning/practice
- Less trading opportunities

**Medium Volatility (0.015 = 1.5%):**
- ✅ **Current setting**
- Realistic market behavior
- Good for events

**High Volatility (0.03 = 3%):**
- Exciting, unpredictable
- Lots of trading opportunities
- Can be stressful for teams

**Extreme Volatility (0.05 = 5%):**
- Wild price swings
- Very risky trades
- Fun but chaotic

---

## 🔧 Admin Controls Quick Reference

### Location: `/admin/app1/stock/`

**Actions Available:**

1. **Set custom price** - Exact price for one stock
2. **Adjust prices by percentage** - % change for selected stocks
3. **Market sector adjustment** - Sector-wide % change
4. **Reset to base price** - Return to original price
5. **Activate/Deactivate stocks** - Hide from trading

### Admin Actions Panel Location:

```
/admin/app1/stock/
↓
[Select stocks with checkboxes]
↓
[Actions dropdown at top]
↓
[Choose action]
↓
[Go button]
```

---

## 🎪 Event Day Playbook

### Pre-Event (30 min before):
- [ ] Check GitHub Actions is running
- [ ] Verify prices are updating (check timestamps)
- [ ] Create 3-5 market news items
- [ ] Test trading with dummy team

### Event Start:
- [ ] Announce "Market opens!"
- [ ] Let prices run naturally for 15-20 min
- [ ] Teams get familiar with platform

### Mid-Event (Hour 2-3):
- [ ] First major news: "Tech sector rallies!"
- [ ] Manually boost tech sector +5%
- [ ] Watch trading volume spike
- [ ] Let stabilize for 30 minutes

### Mid-Event (Hour 4-5):
- [ ] Second news: "Energy stocks decline"
- [ ] Manually drop energy sector -4%
- [ ] Creates buying opportunity for savvy teams
- [ ] Let stabilize

### Mid-Event (Hour 6):
- [ ] Third news: "Healthcare breakthrough!"
- [ ] Boost healthcare sector +6%
- [ ] Final major trading opportunity

### Event End (Hour 7-8):
- [ ] Let prices stabilize naturally
- [ ] No more manual interventions
- [ ] Teams finalize positions
- [ ] Prepare leaderboard

---

## 🐛 Troubleshooting

### "Prices not updating"

**Check:**
1. GitHub Actions: https://github.com/school11220/tradesim/actions
2. Is workflow running every 5 minutes?
3. Are runs successful (green checkmarks)?
4. Check latest run logs for errors

**Fix:**
- Manually trigger: Click "Run workflow"
- Wait 5 minutes
- Refresh stock page

---

### "My manual price disappeared immediately"

**Reason:** You changed price right before auto-update

**Timeline:**
```
12:04:30 - You set price to $250
12:05:00 - Auto-update runs (30 seconds later!)
12:05:01 - Your price replaced
```

**Solution:** Check clock, set price right after an update
- Updates at: :00, :05, :10, :15, :20, :25, etc.
- Set price at: :01, :06, :11, :16, :21, :26, etc.
- Gives you almost 5 full minutes

---

### "I want to pause price updates"

**Steps:**
1. GitHub: https://github.com/school11220/tradesim/actions
2. Click "Update Stock Prices Every 5 Minutes"
3. Click "..." menu (top right)
4. Select "Disable workflow"
5. Prices freeze at current values

**To resume:**
- Same menu → "Enable workflow"
- Manually click "Run workflow" to start immediately

---

## 📊 Price Update API Endpoints

### For Advanced Users / Custom Scripts

**Simulated Update (Current):**
```bash
curl "https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.015"
```

**Response:**
```json
{
  "success": true,
  "mode": "simulated",
  "updated_count": 116,
  "volatility": 0.015,
  "updates": [...]
}
```

**Custom Volatility:**
```bash
# More volatile
curl "https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.03"

# Less volatile
curl "https://tradesim-lyart.vercel.app/api/update-prices?volatility=0.005"
```

---

## 🎓 Key Takeaways

### ✅ **What You Need to Know:**

1. **Prices auto-update every 5 minutes** - No action needed
2. **Manual changes last 5 minutes max** - Then overwritten
3. **Use news for lasting impact** - Teams trade on information
4. **Volatility = 1.5%** - Realistic market behavior
5. **GitHub Actions = FREE** - No Vercel Pro needed
6. **Stabilization = 30 minutes** - 6 updates after manual change

### ⚠️ **Common Mistakes:**

1. ❌ Setting price and expecting it to stay forever
2. ❌ Thinking you need Vercel Pro for updates
3. ❌ Not using market news (more engaging!)
4. ❌ Setting unrealistic volatility (too high/low)
5. ❌ Forgetting to enable GitHub Actions workflow

### ✅ **Best Practices:**

1. ✅ Create news, let teams react
2. ✅ Manual price changes for shock events only
3. ✅ Let prices stabilize 20-30 min between interventions
4. ✅ Use sector-wide changes for major events
5. ✅ Check Actions tab before event starts

---

## 🎯 Quick Command Reference

### Check if updates are working:
```bash
curl -s "https://tradesim-lyart.vercel.app/api/update-prices" | python3 -m json.tool | head -20
```

### Manually trigger update:
1. Visit: https://github.com/school11220/tradesim/actions
2. Click workflow name
3. Click "Run workflow" button

### Change volatility:
1. Edit: `.github/workflows/update-prices.yml`
2. Line ~37: Change `volatility=0.015` to desired value
3. Commit and push

### Disable auto-updates:
1. Actions → Workflow → "..." → Disable

### Enable auto-updates:
1. Actions → Workflow → "..." → Enable

---

## 🎉 You're Ready!

**Your system is configured for:**
- ✅ Automatic price updates every 5 minutes
- ✅ Manual price controls when needed
- ✅ Market news system for engagement
- ✅ Realistic market volatility
- ✅ Free, reliable operation

**For your 8-hour event, you're all set!** 🚀

Questions? Check the troubleshooting section or test with the API endpoints above.

**Good luck with your trading competition!** 📈
