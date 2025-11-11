# Quick Reference - Stock Price System

## 🚀 What Changed?

### Price Updates
- **Frequency**: Every 1 minute (was 5 minutes)
- **Neutrality**: 75% neutral updates (was 60%)
- **Volatility**: 0.3-1.5% per minute (was 0.5-2.0%)
- **Max Change**: ±8% per update (was ±15%)

### Custom Sector Changes
- **Random Variance**: Each stock gets ±0.5% offset
- **Example**: Set +5% → stocks actually change by 4.5%, 5.2%, 5.3%, etc.
- **Precision**: Accepts 1.2%, 0.9%, -2.37% (step: 0.01)

### Mean Reversion
- **Trigger**: >3% deviation (was >5%)
- **Correction**: 10-25% per update (was 5-15%)
- **Result**: Prices naturally return to realistic levels after manual changes

---

## 🎮 How to Use

### As Admin - Trigger Market Events

**Single Sector**:
1. Go to Admin > Stock Market Control
2. Select sector (e.g., "Technology")
3. Enter percentage (e.g., `1.25` or `-2.3`)
4. Click "Apply Custom %"
5. All Technology stocks change by ~1.25% (each with slight variance)

**All Sectors**:
1. Scroll to "Apply Change to ALL Sectors"
2. Enter percentage (e.g., `0.75` for mild bull market)
3. Click "Apply to All Sectors"
4. All stocks across all sectors change by ~0.75%

**Preset Buttons**:
- Quick buttons available: +3%, +5%, -3%, -5%
- Confirmation dialog prevents accidents

### As Student - Browse & Trade

**Browse Stocks**:
- Page auto-refreshes every 15 seconds
- "Last updated" shows real timestamp
- Prices change smoothly every minute
- Green/red flash shows price movements

**Trading**:
- Your buying creates upward pressure (+0-0.3%)
- High ownership makes stock more stable
- Actions affect market realistically

---

## 📊 Price Behavior Examples

### Normal Day:
```
10:00 AM - $225.00
10:01 AM - $225.45 (+0.20%)
10:02 AM - $225.12 (-0.15%)
10:03 AM - $225.98 (+0.38%)
```
*Small, natural movements*

### After +10% Event:
```
Immediate: $225.00 → $247.13 (+10%)
1 min later: $245.78 (-0.55%) [reversion]
5 mins later: $244.12 (-1.22%) [stabilizing]
20 mins later: $232.45 (+3.3%) [stable]
```
*Gradually returns to realistic level*

---

## ✅ Key Benefits

1. **Dynamic Markets**: Prices change every minute
2. **Natural Behavior**: 75% neutral, no wild swings
3. **Variance**: No two stocks move identically
4. **Self-Correcting**: Extreme changes revert naturally
5. **Precise Control**: Enter any decimal percentage

---

## 🐛 Troubleshooting

**"Prices aren't updating"**
- Check GitHub Actions: https://github.com/school11220/tradesim/actions
- Should see successful runs every minute
- Click on latest run to check logs

**"Last updated shows Never"**
- Clear browser cache
- Refresh page (Ctrl+F5)
- Wait 1-2 seconds for automatic update

**"Prices jumped too much"**
- Check if admin triggered manual event
- Prices will normalize over 5-10 minutes
- Mean reversion is working as intended

**"Custom % not working"**
- Ensure you selected a sector first
- Check if value is valid number
- Look for success message

---

## 📞 Quick Commands

**Manual Price Update**:
```bash
curl https://tradesim-lyart.vercel.app/api/update-prices-real
```

**Check GitHub Actions**:
https://github.com/school11220/tradesim/actions

**View Admin Panel**:
https://your-site.com/admin/

---

**Last Updated**: November 11, 2025  
**Status**: ✅ Production Ready
