"""
Management command to initialize 50+ stocks for trading competition
"""
from django.core.management.base import BaseCommand
from app1.models import Stock


class Command(BaseCommand):
    help = 'Initialize 50+ real company stocks for trading competition'

    def handle(self, *args, **options):
        self.stdout.write('Initializing 50+ stocks for competition...\n')

        stocks_data = [
            # Technology (15)
            ('AAPL', 'Apple Inc.', 175.50),
            ('MSFT', 'Microsoft Corporation', 378.90),
            ('GOOG', 'Alphabet Inc.', 142.30),
            ('META', 'Meta Platforms Inc.', 325.80),
            ('AMZN', 'Amazon.com Inc.', 145.60),
            ('TSLA', 'Tesla Inc.', 242.80),
            ('NVDA', 'NVIDIA Corporation', 495.20),
            ('ORCL', 'Oracle Corporation', 118.50),
            ('INTC', 'Intel Corporation', 43.20),
            ('AMD', 'Advanced Micro Devices', 138.90),
            ('CRM', 'Salesforce Inc.', 235.40),
            ('ADBE', 'Adobe Inc.', 558.70),
            ('CSCO', 'Cisco Systems Inc.', 49.80),
            ('IBM', 'International Business Machines', 152.30),
            ('NFLX', 'Netflix Inc.', 445.20),

            # Finance (10)
            ('JPM', 'JPMorgan Chase & Co.', 148.90),
            ('BAC', 'Bank of America Corp.', 32.45),
            ('WFC', 'Wells Fargo & Company', 52.30),
            ('GS', 'Goldman Sachs Group Inc.', 386.70),
            ('MS', 'Morgan Stanley', 85.60),
            ('V', 'Visa Inc.', 258.30),
            ('MA', 'Mastercard Inc.', 412.50),
            ('AXP', 'American Express Company', 185.40),
            ('BLK', 'BlackRock Inc.', 742.80),
            ('SCHW', 'Charles Schwab Corporation', 68.90),

            # Healthcare (10)
            ('JNJ', 'Johnson & Johnson', 158.90),
            ('PFE', 'Pfizer Inc.', 28.45),
            ('UNH', 'UnitedHealth Group Inc.', 478.30),
            ('ABBV', 'AbbVie Inc.', 168.70),
            ('TMO', 'Thermo Fisher Scientific Inc.', 528.40),
            ('MRK', 'Merck & Co. Inc.', 112.30),
            ('ABT', 'Abbott Laboratories', 108.90),
            ('BMY', 'Bristol-Myers Squibb Company', 54.60),
            ('LLY', 'Eli Lilly and Company', 585.90),
            ('AMGN', 'Amgen Inc.', 285.40),

            # Energy (7)
            ('XOM', 'Exxon Mobil Corporation', 108.70),
            ('CVX', 'Chevron Corporation', 152.30),
            ('COP', 'ConocoPhillips', 118.50),
            ('SLB', 'Schlumberger Limited', 48.90),
            ('EOG', 'EOG Resources Inc.', 128.40),
            ('MPC', 'Marathon Petroleum Corporation', 168.70),
            ('PSX', 'Phillips 66', 138.90),

            # Consumer Goods & Retail (10)
            ('WMT', 'Walmart Inc.', 168.40),
            ('HD', 'The Home Depot Inc.', 345.60),
            ('MCD', "McDonald's Corporation", 285.70),
            ('NKE', 'NIKE Inc.', 94.50),
            ('SBUX', 'Starbucks Corporation', 95.80),
            ('TGT', 'Target Corporation', 138.90),
            ('LOW', "Lowe's Companies Inc.", 228.40),
            ('TJX', 'The TJX Companies Inc.', 98.70),
            ('DG', 'Dollar General Corporation', 82.30),
            ('COST', 'Costco Wholesale Corporation', 658.90),

            # Industrial (5)
            ('BA', 'The Boeing Company', 178.90),
            ('CAT', 'Caterpillar Inc.', 298.40),
            ('GE', 'General Electric Company', 118.50),
            ('UPS', 'United Parcel Service Inc.', 145.30),
            ('HON', 'Honeywell International Inc.', 198.70),

            # Telecommunications (3)
            ('VZ', 'Verizon Communications Inc.', 42.30),
            ('T', 'AT&T Inc.', 18.90),
            ('TMUS', 'T-Mobile US Inc.', 178.40),

            # Entertainment & Media (3)
            ('DIS', 'The Walt Disney Company', 98.70),
            ('SONY', 'Sony Group Corporation', 92.40),
            ('CMCSA', 'Comcast Corporation', 43.20),
        ]

        created_count = 0
        updated_count = 0

        for symbol, name, price in stocks_data:
            stock, created = Stock.objects.update_or_create(
                symbol=symbol,
                defaults={
                    'name': name,
                    'current_price': price,
                    'previous_close': price * 0.98,  # Set previous close 2% lower
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created stock: {symbol} - {name} @ ${price}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated stock: {symbol} - {name} @ ${price}'))

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Stock initialization complete!'))
        self.stdout.write(f'  - Created: {created_count} new stocks')
        self.stdout.write(f'  - Updated: {updated_count} existing stocks')
        self.stdout.write(f'  - Total: {len(stocks_data)} stocks available for trading\n')
