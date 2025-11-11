"""
Script to populate database with 150+ stocks across various sectors
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demostocks.settings')
django.setup()

from app1.models import Stock

# Define comprehensive stock list across multiple sectors
STOCK_DATA = {
    "Technology": [
        ("AAPL", "Apple Inc.", 175.50),
        ("MSFT", "Microsoft Corporation", 378.90),
        ("GOOGL", "Alphabet Inc. Class A", 142.30),
        ("META", "Meta Platforms Inc.", 485.20),
        ("NVDA", "NVIDIA Corporation", 495.60),
        ("TSLA", "Tesla Inc.", 242.80),
        ("ORCL", "Oracle Corporation", 123.45),
        ("ADBE", "Adobe Inc.", 546.78),
        ("CRM", "Salesforce Inc.", 234.56),
        ("INTC", "Intel Corporation", 42.33),
        ("AMD", "Advanced Micro Devices", 154.76),
        ("CSCO", "Cisco Systems Inc.", 51.25),
        ("AVGO", "Broadcom Inc.", 876.50),
        ("TXN", "Texas Instruments", 167.80),
        ("QCOM", "Qualcomm Inc.", 142.90),
        ("AMAT", "Applied Materials", 158.30),
        ("MU", "Micron Technology", 88.40),
        ("LRCX", "Lam Research", 945.60),
        ("KLAC", "KLA Corporation", 587.20),
        ("SNPS", "Synopsys Inc.", 543.10),
    ],
    
    "Healthcare": [
        ("JNJ", "Johnson & Johnson", 156.80),
        ("UNH", "UnitedHealth Group", 524.30),
        ("PFE", "Pfizer Inc.", 28.50),
        ("ABBV", "AbbVie Inc.", 154.70),
        ("TMO", "Thermo Fisher Scientific", 541.20),
        ("ABT", "Abbott Laboratories", 110.45),
        ("DHR", "Danaher Corporation", 252.80),
        ("BMY", "Bristol-Myers Squibb", 51.60),
        ("LLY", "Eli Lilly and Company", 598.70),
        ("AMGN", "Amgen Inc.", 281.40),
        ("GILD", "Gilead Sciences", 78.90),
        ("CVS", "CVS Health Corporation", 82.30),
        ("CI", "Cigna Corporation", 312.50),
        ("REGN", "Regeneron Pharmaceuticals", 875.60),
        ("VRTX", "Vertex Pharmaceuticals", 398.20),
        ("ISRG", "Intuitive Surgical", 367.80),
        ("ZTS", "Zoetis Inc.", 178.90),
        ("SYK", "Stryker Corporation", 324.50),
        ("BDX", "Becton Dickinson", 245.70),
        ("EW", "Edwards Lifesciences", 87.40),
    ],
    
    "Financial": [
        ("JPM", "JPMorgan Chase & Co.", 178.40),
        ("BAC", "Bank of America Corp", 34.50),
        ("WFC", "Wells Fargo & Company", 52.30),
        ("GS", "Goldman Sachs Group", 398.70),
        ("MS", "Morgan Stanley", 98.60),
        ("C", "Citigroup Inc.", 56.80),
        ("BLK", "BlackRock Inc.", 785.90),
        ("SCHW", "Charles Schwab Corp", 68.40),
        ("AXP", "American Express Company", 189.50),
        ("USB", "U.S. Bancorp", 43.20),
        ("PNC", "PNC Financial Services", 156.70),
        ("TFC", "Truist Financial Corp", 38.90),
        ("COF", "Capital One Financial", 132.40),
        ("BK", "Bank of New York Mellon", 54.80),
        ("STT", "State Street Corporation", 78.30),
        ("AIG", "American International Group", 68.50),
        ("MET", "MetLife Inc.", 67.90),
        ("PRU", "Prudential Financial", 98.70),
        ("AFL", "Aflac Incorporated", 78.60),
        ("ALL", "Allstate Corporation", 154.80),
    ],
    
    "Consumer": [
        ("AMZN", "Amazon.com Inc.", 178.35),
        ("WMT", "Walmart Inc.", 165.80),
        ("HD", "Home Depot Inc.", 365.40),
        ("MCD", "McDonald's Corporation", 287.90),
        ("NKE", "Nike Inc.", 98.50),
        ("SBUX", "Starbucks Corporation", 94.30),
        ("TGT", "Target Corporation", 148.60),
        ("LOW", "Lowe's Companies", 234.70),
        ("COST", "Costco Wholesale", 658.90),
        ("KO", "Coca-Cola Company", 58.40),
        ("PEP", "PepsiCo Inc.", 168.50),
        ("PG", "Procter & Gamble", 156.70),
        ("CL", "Colgate-Palmolive", 88.30),
        ("KMB", "Kimberly-Clark", 134.50),
        ("GIS", "General Mills", 67.80),
        ("K", "Kellogg Company", 58.90),
        ("HSY", "Hershey Company", 198.40),
        ("MDLZ", "Mondelez International", 71.20),
        ("KHC", "Kraft Heinz Company", 35.60),
        ("STZ", "Constellation Brands", 245.80),
    ],
    
    "Energy": [
        ("XOM", "Exxon Mobil Corporation", 112.40),
        ("CVX", "Chevron Corporation", 156.80),
        ("COP", "ConocoPhillips", 118.50),
        ("SLB", "Schlumberger Limited", 48.70),
        ("EOG", "EOG Resources", 124.30),
        ("MPC", "Marathon Petroleum", 168.90),
        ("PSX", "Phillips 66", 138.40),
        ("VLO", "Valero Energy", 145.60),
        ("OXY", "Occidental Petroleum", 58.90),
        ("HAL", "Halliburton Company", 34.20),
        ("DVN", "Devon Energy", 42.80),
        ("FANG", "Diamondback Energy", 156.70),
        ("HES", "Hess Corporation", 148.30),
        ("MRO", "Marathon Oil", 26.50),
        ("APA", "APA Corporation", 32.40),
        ("BKR", "Baker Hughes", 34.80),
        ("NOV", "NOV Inc.", 17.50),
        ("CHRD", "Chord Energy", 168.90),
        ("CTRA", "Coterra Energy", 26.70),
        ("OVV", "Ovintiv Inc.", 48.90),
    ],
    
    "Industrial": [
        ("BA", "Boeing Company", 178.60),
        ("HON", "Honeywell International", 198.40),
        ("UPS", "United Parcel Service", 148.90),
        ("CAT", "Caterpillar Inc.", 312.50),
        ("GE", "General Electric", 134.60),
        ("RTX", "Raytheon Technologies", 98.70),
        ("LMT", "Lockheed Martin", 468.90),
        ("DE", "Deere & Company", 398.50),
        ("MMM", "3M Company", 98.60),
        ("EMR", "Emerson Electric", 108.40),
        ("ITW", "Illinois Tool Works", 256.70),
        ("PH", "Parker-Hannifin", 487.30),
        ("ETN", "Eaton Corporation", 278.90),
        ("PCAR", "PACCAR Inc.", 98.50),
        ("ROK", "Rockwell Automation", 298.60),
        ("FDX", "FedEx Corporation", 256.40),
        ("NSC", "Norfolk Southern", 234.80),
        ("CSX", "CSX Corporation", 34.60),
        ("UNP", "Union Pacific", 248.70),
        ("WM", "Waste Management", 189.50),
    ],
    
    "Telecommunications": [
        ("T", "AT&T Inc.", 18.45),
        ("VZ", "Verizon Communications", 40.30),
        ("TMUS", "T-Mobile US", 162.80),
        ("CMCSA", "Comcast Corporation", 42.50),
        ("CHTR", "Charter Communications", 378.90),
        ("DIS", "Walt Disney Company", 96.40),
        ("NFLX", "Netflix Inc.", 485.60),
        ("PARA", "Paramount Global", 14.30),
        ("WBD", "Warner Bros Discovery", 9.80),
        ("FOX", "Fox Corporation", 34.60),
        ("FOXA", "Fox Corporation Class A", 35.20),
        ("DISH", "DISH Network", 6.40),
        ("SIRI", "Sirius XM Holdings", 3.80),
        ("LUMN", "Lumen Technologies", 1.90),
        ("VIV", "Telefonica Brasil", 9.50),
    ],
    
    "Real Estate": [
        ("AMT", "American Tower Corp", 198.70),
        ("PLD", "Prologis Inc.", 134.50),
        ("CCI", "Crown Castle Inc.", 98.30),
        ("EQIX", "Equinix Inc.", 823.40),
        ("PSA", "Public Storage", 298.60),
        ("WELL", "Welltower Inc.", 98.70),
        ("DLR", "Digital Realty Trust", 145.80),
        ("SPG", "Simon Property Group", 148.90),
        ("O", "Realty Income Corp", 56.40),
        ("AVB", "AvalonBay Communities", 198.30),
        ("EQR", "Equity Residential", 67.80),
        ("VTR", "Ventas Inc.", 48.90),
        ("ESS", "Essex Property Trust", 256.70),
        ("MAA", "Mid-America Apartment", 145.60),
        ("UDR", "UDR Inc.", 38.90),
    ],
    
    "Materials": [
        ("LIN", "Linde plc", 445.60),
        ("APD", "Air Products & Chemicals", 298.70),
        ("ECL", "Ecolab Inc.", 198.40),
        ("SHW", "Sherwin-Williams", 312.50),
        ("FCX", "Freeport-McMoRan", 42.80),
        ("NEM", "Newmont Corporation", 42.30),
        ("DOW", "Dow Inc.", 54.60),
        ("DD", "DuPont de Nemours", 78.90),
        ("PPG", "PPG Industries", 134.70),
        ("NUE", "Nucor Corporation", 178.40),
        ("BALL", "Ball Corporation", 56.80),
        ("ALB", "Albemarle Corporation", 112.50),
        ("CE", "Celanese Corporation", 134.60),
        ("IFF", "International Flavors", 87.90),
        ("VMC", "Vulcan Materials", 234.50),
    ],
    
    "Utilities": [
        ("NEE", "NextEra Energy", 67.80),
        ("DUK", "Duke Energy", 98.40),
        ("SO", "Southern Company", 78.90),
        ("D", "Dominion Energy", 54.30),
        ("AEP", "American Electric Power", 89.60),
        ("EXC", "Exelon Corporation", 39.80),
        ("XEL", "Xcel Energy", 56.70),
        ("SRE", "Sempra Energy", 78.90),
        ("WEC", "WEC Energy Group", 89.40),
        ("ED", "Consolidated Edison", 98.60),
        ("PEG", "Public Service Enterprise", 67.80),
        ("ES", "Eversource Energy", 64.50),
        ("AWK", "American Water Works", 145.80),
        ("FE", "FirstEnergy Corp", 38.90),
        ("CNP", "CenterPoint Energy", 29.70),
    ],
}

def populate_stocks():
    """Populate the database with stock data"""
    created_count = 0
    updated_count = 0
    
    for sector, stocks in STOCK_DATA.items():
        print(f"\nProcessing {sector} sector...")
        for symbol, name, price in stocks:
            stock, created = Stock.objects.update_or_create(
                symbol=symbol,
                defaults={
                    'name': name,
                    'sector': sector,
                    'current_price': price,
                    'previous_close': price,
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                print(f"  ✓ Created: {symbol} - {name}")
            else:
                updated_count += 1
                print(f"  ↻ Updated: {symbol} - {name}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"Total stocks created: {created_count}")
    print(f"Total stocks updated: {updated_count}")
    print(f"Total stocks in database: {Stock.objects.count()}")
    
    # Print sector distribution
    print(f"\nSector Distribution:")
    for sector in STOCK_DATA.keys():
        count = Stock.objects.filter(sector=sector).count()
        print(f"  {sector}: {count} stocks")

if __name__ == '__main__':
    print("="*60)
    print("STOCK DATABASE POPULATION SCRIPT")
    print("="*60)
    populate_stocks()
    print(f"\n{'='*60}")
    print("DONE! Database populated successfully.")
    print("="*60)
