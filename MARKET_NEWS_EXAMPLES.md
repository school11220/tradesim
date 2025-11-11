# Market News Examples - Admin Guide

## How to Add News in Django Admin

When adding Market News in the admin panel, you'll see fields for **Affected Sectors** and **Affected Stocks**. These are JSON fields that need proper formatting.

---

## Example News Stories with Correct JSON Inputs

### Example 1: Tech Sector Positive News
**Title:** Apple Announces Revolutionary AI Chip

**Content:** 
```
Apple has unveiled its groundbreaking M4 chip with advanced AI capabilities, 
promising 10x faster machine learning performance. Industry analysts predict 
this could give Apple a significant edge in the AI race.
```

**Impact Direction:** 📈 Positive (Bullish)

**Severity:** High Impact

**Affected Sectors (JSON):**
```json
["Technology", "Consumer Electronics"]
```

**Affected Stocks (JSON):**
```json
["AAPL", "NVDA", "AMD"]
```

**Trading Hint:**
```
Consider buying AAPL and related AI chip manufacturers. 
Tech sector expected to rally on this news.
```

---

### Example 2: Energy Sector Negative News
**Title:** OPEC Announces Major Production Increase

**Content:**
```
OPEC+ has agreed to increase oil production by 2 million barrels per day 
starting next month, potentially flooding the market and driving prices down. 
Energy stocks expected to face downward pressure.
```

**Impact Direction:** 📉 Negative (Bearish)

**Severity:** Critical Impact

**Affected Sectors (JSON):**
```json
["Energy", "Oil & Gas"]
```

**Affected Stocks (JSON):**
```json
["XOM", "CVX", "COP", "SLB"]
```

**Trading Hint:**
```
Short energy stocks or sell holdings in oil companies. 
Consider rotating into defensive sectors.
```

---

### Example 3: Healthcare Breakthrough
**Title:** FDA Approves Breakthrough Cancer Treatment

**Content:**
```
The FDA has granted emergency approval to a revolutionary cancer treatment 
developed by multiple pharmaceutical companies. Clinical trials showed 
an 85% success rate in treating advanced stage cancers.
```

**Impact Direction:** 📈 Positive (Bullish)

**Severity:** High Impact

**Affected Sectors (JSON):**
```json
["Healthcare", "Pharmaceuticals", "Biotechnology"]
```

**Affected Stocks (JSON):**
```json
["PFE", "JNJ", "MRNA", "ABBV", "BMY"]
```

**Trading Hint:**
```
Buy pharmaceutical and biotech stocks. Healthcare sector 
expected to surge on this breakthrough news.
```

---

### Example 4: Federal Reserve Policy Change
**Title:** Fed Signals Interest Rate Cuts Coming

**Content:**
```
Federal Reserve Chair announced today that the central bank is considering 
rate cuts in the coming months due to cooling inflation. This marks a 
significant shift in monetary policy and is expected to boost market 
sentiment across all sectors.
```

**Impact Direction:** 📈 Positive (Bullish)

**Severity:** Critical Impact

**Affected Sectors (JSON):**
```json
["Financials", "Real Estate", "Technology", "Consumer Discretionary"]
```

**Affected Stocks (JSON):**
```json
["JPM", "BAC", "WFC", "MS", "GS"]
```

**Trading Hint:**
```
Market-wide rally expected. Consider increasing equity positions. 
Banks and growth stocks particularly well-positioned to benefit.
```

---

### Example 5: Retail Sector Mixed News
**Title:** E-commerce Growth Slows as Consumers Return to Stores

**Content:**
```
Latest retail data shows online shopping growth declining while brick-and-mortar 
stores see increased foot traffic. This mixed signal creates uncertainty 
for retail investors as the industry transitions.
```

**Impact Direction:** 🔀 Mixed

**Severity:** Medium Impact

**Affected Sectors (JSON):**
```json
["Retail", "Consumer Discretionary"]
```

**Affected Stocks (JSON):**
```json
["AMZN", "WMT", "TGT", "COST", "HD"]
```

**Trading Hint:**
```
Be cautious with retail stocks. Consider diversifying between 
e-commerce and traditional retail to hedge risk.
```

---

### Example 6: Market-Wide Neutral News
**Title:** Economic Data Meets Expectations

**Content:**
```
Latest GDP and employment reports came in exactly as analysts predicted, 
showing steady but unspectacular economic growth. No major surprises 
in the data.
```

**Impact Direction:** ➡️ Neutral

**Severity:** Low Impact

**Affected Sectors (JSON):**
```json
[]
```
*(Leave empty for market-wide news with no specific sector focus)*

**Affected Stocks (JSON):**
```json
[]
```
*(Leave empty for general market news)*

**Trading Hint:**
```
Hold current positions. No immediate action needed based on this data.
```

---

### Example 7: Automotive Industry Disruption
**Title:** Tesla Slashes Prices, Sparking Industry Price War

**Content:**
```
Tesla announced aggressive price cuts across its entire vehicle lineup, 
reducing prices by up to 20%. Competitors are expected to follow suit, 
potentially squeezing profit margins industry-wide.
```

**Impact Direction:** 📉 Negative (Bearish)

**Severity:** High Impact

**Affected Sectors (JSON):**
```json
["Automotive", "Consumer Discretionary"]
```

**Affected Stocks (JSON):**
```json
["TSLA", "F", "GM", "TM", "STLA"]
```

**Trading Hint:**
```
Sell or reduce positions in traditional automakers. 
Price wars typically hurt profitability across the sector.
```

---

### Example 8: Cryptocurrency Regulation Announcement
**Title:** SEC Approves Major Cryptocurrency ETFs

**Content:**
```
The Securities and Exchange Commission has approved several Bitcoin and 
Ethereum ETFs, opening cryptocurrency investing to mainstream investors. 
Crypto-related stocks expected to benefit significantly.
```

**Impact Direction:** 📈 Positive (Bullish)

**Severity:** Critical Impact

**Affected Sectors (JSON):**
```json
["Technology", "Financials"]
```

**Affected Stocks (JSON):**
```json
["COIN", "MSTR", "RIOT", "MARA"]
```

**Trading Hint:**
```
Strong buy signal for crypto-related stocks. Major institutional 
money expected to flow into the sector.
```

---

## JSON Format Rules

### For Affected Sectors:
```json
["Sector Name 1", "Sector Name 2", "Sector Name 3"]
```

**Available Sectors in Your System:**
- Technology
- Healthcare
- Financials
- Energy
- Consumer Discretionary
- Consumer Staples
- Industrials
- Materials
- Real Estate
- Utilities
- Communication Services
- Oil & Gas
- Pharmaceuticals
- Biotechnology
- Consumer Electronics
- Automotive
- Retail

### For Affected Stocks:
```json
["SYMBOL1", "SYMBOL2", "SYMBOL3"]
```

**Example Stock Symbols:**
- Tech: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
- Finance: JPM, BAC, WFC, GS, MS
- Healthcare: JNJ, PFE, UNH, ABBV, TMO
- Energy: XOM, CVX, COP, SLB
- Retail: WMT, TGT, COST, HD, LOW

---

## Common Mistakes to Avoid

❌ **WRONG - Missing quotes around strings:**
```json
[Technology, Healthcare]
```

✅ **CORRECT:**
```json
["Technology", "Healthcare"]
```

---

❌ **WRONG - Single quotes instead of double quotes:**
```json
['AAPL', 'MSFT']
```

✅ **CORRECT:**
```json
["AAPL", "MSFT"]
```

---

❌ **WRONG - Trailing comma:**
```json
["AAPL", "MSFT",]
```

✅ **CORRECT:**
```json
["AAPL", "MSFT"]
```

---

❌ **WRONG - Missing brackets:**
```json
"AAPL", "MSFT"
```

✅ **CORRECT:**
```json
["AAPL", "MSFT"]
```

---

## Quick Copy-Paste Templates

### Empty (Market-Wide News):
```json
[]
```

### Single Item:
```json
["Technology"]
```
or
```json
["AAPL"]
```

### Multiple Items:
```json
["Technology", "Healthcare", "Financials"]
```
or
```json
["AAPL", "MSFT", "GOOGL", "AMZN"]
```

---

## Tips for Event Admins

1. **Timing:** Set "Expires at" to automatically hide news after a certain time
2. **Severity:** Use "Critical" sparingly for maximum impact
3. **Trading Hints:** Give students actionable advice to make the simulation educational
4. **Active Status:** Uncheck "Is active" to draft news before publishing
5. **Test First:** Add a test news item and view it on the team page before the event

---

## Checking Your News

After adding news in the admin:
1. Mark it as **Active** (✓ Is active checkbox)
2. Go to the team login page
3. Login with any team credentials
4. Click **News** in the navigation
5. Your news should appear with proper styling based on Impact and Severity

---

**Need Help?** If your JSON isn't working, copy-paste one of the examples above exactly, then modify it for your needs.
