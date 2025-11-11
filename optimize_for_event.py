"""
Optimize stock database for 8-10 hour events
Reduces to optimal number for Yahoo Finance rate limits
Keeps the most liquid and popular stocks
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
django.setup()

from app1.models import Stock

# Yahoo Finance Rate Limits:
# ~2,000 requests per hour (safe estimate: 1,800/hr to be conservative)
# 
# For 8-10 hour event with updates every 5 minutes:
# - 12 updates per hour
# - Max stocks = 1,800 / 12 = 150 stocks per hour
# 
# To be extra safe and account for overhead: 120 stocks

MAX_STOCKS = 120

# Select most important stocks (high liquidity, popular companies)
# Balanced across sectors for fair competition
KEEP_STOCKS = {
    # Technology (25 stocks - most active sector)
    'Technology': [
        'AAPL',   # Apple - Most valuable
        'MSFT',   # Microsoft
        'GOOGL',  # Alphabet/Google
        'AMZN',   # Amazon
        'NVDA',   # NVIDIA - AI leader
        'META',   # Meta/Facebook
        'TSLA',   # Tesla
        'AVGO',   # Broadcom
        'ORCL',   # Oracle
        'ADBE',   # Adobe
        'CRM',    # Salesforce
        'CSCO',   # Cisco
        'AMD',    # AMD
        'INTC',   # Intel
        'QCOM',   # Qualcomm
        'TXN',    # Texas Instruments
        'AMAT',   # Applied Materials
        'MU',     # Micron
        'LRCX',   # Lam Research
        'KLAC',   # KLA Corp
        'SNPS',   # Synopsys
        'NFLX',   # Netflix
        'UBER',   # Uber
        'SHOP',   # Shopify
        'SQ',     # Block/Square
    ],
    
    # Healthcare (20 stocks)
    'Healthcare': [
        'JNJ',    # Johnson & Johnson
        'UNH',    # UnitedHealth - largest
        'LLY',    # Eli Lilly
        'ABBV',   # AbbVie
        'MRK',    # Merck
        'TMO',    # Thermo Fisher
        'ABT',    # Abbott Labs
        'PFE',    # Pfizer
        'DHR',    # Danaher
        'BMY',    # Bristol Myers
        'AMGN',   # Amgen
        'GILD',   # Gilead
        'CVS',    # CVS Health
        'VRTX',   # Vertex Pharma
        'REGN',   # Regeneron
        'ISRG',   # Intuitive Surgical
        'CI',     # Cigna
        'ZTS',    # Zoetis
        'SYK',    # Stryker
        'BDX',    # Becton Dickinson
    ],
    
    # Financial (20 stocks)
    'Financial': [
        'JPM',    # JPMorgan - largest bank
        'BAC',    # Bank of America
        'WFC',    # Wells Fargo
        'GS',     # Goldman Sachs
        'MS',     # Morgan Stanley
        'BLK',    # BlackRock - largest asset manager
        'C',      # Citigroup
        'SCHW',   # Charles Schwab
        'AXP',    # American Express
        'USB',    # US Bancorp
        'PNC',    # PNC Financial
        'TFC',    # Truist Financial
        'COF',    # Capital One
        'BK',     # Bank of NY Mellon
        'AIG',    # AIG
        'MET',    # MetLife
        'PRU',    # Prudential
        'AFL',    # Aflac
        'ALL',    # Allstate
        'TRV',    # Travelers
    ],
    
    # Consumer (15 stocks)
    'Consumer': [
        'WMT',    # Walmart - largest retailer
        'HD',     # Home Depot
        'MCD',    # McDonald's
        'COST',   # Costco
        'NKE',    # Nike
        'SBUX',   # Starbucks
        'TGT',    # Target
        'LOW',    # Lowe's
        'KO',     # Coca-Cola
        'PEP',    # PepsiCo
        'PG',     # Procter & Gamble
        'WMT',    # Walmart
        'DIS',    # Disney
        'CMCSA',  # Comcast
        'NFLX',   # Netflix
    ],
    
    # Energy (12 stocks)
    'Energy': [
        'XOM',    # Exxon Mobil - largest
        'CVX',    # Chevron
        'COP',    # ConocoPhillips
        'SLB',    # Schlumberger
        'EOG',    # EOG Resources
        'MPC',    # Marathon Petroleum
        'PSX',    # Phillips 66
        'VLO',    # Valero Energy
        'OXY',    # Occidental
        'HAL',    # Halliburton
        'DVN',    # Devon Energy
        'FANG',   # Diamondback Energy
    ],
    
    # Industrial (12 stocks)
    'Industrial': [
        'BA',     # Boeing
        'HON',    # Honeywell
        'UPS',    # UPS
        'CAT',    # Caterpillar
        'GE',     # General Electric
        'RTX',    # Raytheon
        'LMT',    # Lockheed Martin
        'DE',     # Deere
        'MMM',    # 3M
        'FDX',    # FedEx
        'UNP',    # Union Pacific
        'WM',     # Waste Management
    ],
    
    # Telecommunications (8 stocks)
    'Telecommunications': [
        'T',      # AT&T
        'VZ',     # Verizon
        'TMUS',   # T-Mobile
        'CHTR',   # Charter Comm
        'DIS',    # Disney (media)
        'NFLX',   # Netflix
        'CMCSA',  # Comcast
        'PARA',   # Paramount
    ],
    
    # Real Estate (5 stocks - REITs)
    'Real Estate': [
        'AMT',    # American Tower
        'PLD',    # Prologis
        'EQIX',   # Equinix
        'PSA',    # Public Storage
        'SPG',    # Simon Property
    ],
    
    # Materials (5 stocks)
    'Materials': [
        'LIN',    # Linde
        'APD',    # Air Products
        'ECL',    # Ecolab
        'FCX',    # Freeport-McMoRan
        'NEM',    # Newmont
    ],
    
    # Utilities (3 stocks)
    'Utilities': [
        'NEE',    # NextEra Energy
        'DUK',    # Duke Energy
        'SO',     # Southern Company
    ],
}

def optimize_stocks():
    """Remove excess stocks, keep only the most liquid and popular ones"""
    
    print("="*70)
    print("OPTIMIZING STOCK DATABASE FOR 8-10 HOUR EVENTS")
    print("="*70)
    print(f"\nTarget: {MAX_STOCKS} stocks (safe for Yahoo Finance rate limits)")
    print(f"Current: {Stock.objects.count()} stocks\n")
    
    # Flatten the keep list
    keep_symbols = set()
    for sector, symbols in KEEP_STOCKS.items():
        keep_symbols.update(symbols)
    
    # Remove duplicates and count
    keep_symbols = list(set(keep_symbols))
    print(f"Selected: {len(keep_symbols)} most liquid stocks\n")
    
    if len(keep_symbols) > MAX_STOCKS:
        print(f"⚠️  Warning: Selected {len(keep_symbols)} stocks, trimming to {MAX_STOCKS}")
        keep_symbols = keep_symbols[:MAX_STOCKS]
    
    # Get stocks to delete
    stocks_to_delete = Stock.objects.exclude(symbol__in=keep_symbols)
    delete_count = stocks_to_delete.count()
    
    if delete_count > 0:
        print(f"🗑️  Removing {delete_count} less liquid stocks...\n")
        
        # Show what's being removed
        removed_by_sector = {}
        for stock in stocks_to_delete:
            sector = stock.sector
            if sector not in removed_by_sector:
                removed_by_sector[sector] = []
            removed_by_sector[sector].append(stock.symbol)
        
        print("Stocks being removed:")
        for sector, symbols in sorted(removed_by_sector.items()):
            print(f"  {sector}: {', '.join(symbols[:5])}{'...' if len(symbols) > 5 else ''} ({len(symbols)} total)")
        
        # Delete them
        stocks_to_delete.delete()
        print(f"\n✅ Deleted {delete_count} stocks")
    else:
        print("✅ No stocks need to be removed")
    
    # Final count by sector
    print(f"\n{'='*70}")
    print("FINAL STOCK DISTRIBUTION")
    print(f"{'='*70}\n")
    
    total = 0
    for sector in sorted(KEEP_STOCKS.keys()):
        count = Stock.objects.filter(sector=sector).count()
        total += count
        print(f"  {sector:20s}: {count:3d} stocks")
    
    print(f"\n  {'Total':20s}: {total:3d} stocks")
    
    # Calculate rate limits
    print(f"\n{'='*70}")
    print("RATE LIMIT ANALYSIS")
    print(f"{'='*70}\n")
    
    updates_per_hour = 12  # Every 5 minutes
    requests_per_hour = total * updates_per_hour
    
    print(f"  Updates per hour: {updates_per_hour}")
    print(f"  Stocks: {total}")
    print(f"  Requests per hour: {requests_per_hour}")
    print(f"  Yahoo limit: ~1,800/hour")
    print(f"  Safety margin: {1800 - requests_per_hour} requests/hour")
    
    if requests_per_hour <= 1800:
        print(f"\n  ✅ SAFE: Can run for 10+ hours without issues!")
    else:
        print(f"\n  ⚠️  WARNING: May hit rate limits!")
    
    # Event duration calculations
    print(f"\n{'='*70}")
    print("EVENT DURATION CALCULATIONS")
    print(f"{'='*70}\n")
    
    for hours in [8, 10, 12]:
        total_requests = requests_per_hour * hours
        print(f"  {hours}-hour event: {total_requests:,} total requests")
    
    max_hours = 48000 // requests_per_hour  # Daily limit
    print(f"\n  Maximum sustainable duration: {max_hours} hours")
    
    print(f"\n{'='*70}")
    print("✅ OPTIMIZATION COMPLETE!")
    print(f"{'='*70}\n")
    
    return total

if __name__ == '__main__':
    try:
        final_count = optimize_stocks()
        print(f"Your system is now optimized with {final_count} stocks.")
        print("Safe for 8-10 hour events with 5-minute updates! 🚀")
    except Exception as e:
        print(f"❌ Error: {e}")
