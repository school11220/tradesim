from django.db import models
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.
class users(AbstractUser):
    username=models.CharField(max_length=52,primary_key=True)
    firstname=models.CharField(max_length=52)
    lastname=models.CharField(max_length=52)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128,default=0000)
    datajoined=models.DateTimeField(auto_now_add=True)
    balance=models.FloatField(default=10000.0)
    stockbuy=models.JSONField(default=dict)
    stocksold=models.JSONField(default=dict)
    watchlist=models.JSONField(default=dict)
    cache=models.JSONField(default=dict)

    def __str__(self):
        return self.username


class Stock(models.Model):
    """Model for controlling stock prices in the simulator"""
    symbol = models.CharField(max_length=10, unique=True, primary_key=True, help_text="Stock ticker symbol (e.g., AAPL)")
    name = models.CharField(max_length=100, help_text="Company name")
    sector = models.CharField(max_length=50, default="Technology", help_text="Industry sector")
    current_price = models.FloatField(default=100.0, help_text="Current price per share")
    previous_close = models.FloatField(default=100.0, help_text="Previous closing price")
    is_active = models.BooleanField(default=True, help_text="Whether this stock is available for trading")
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['symbol']
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.symbol} - ${self.current_price}"

    @property
    def price_change(self):
        """Calculate price change from previous close"""
        return self.current_price - self.previous_close

    @property
    def price_change_percent(self):
        """Calculate percentage change"""
        if self.previous_close > 0:
            return ((self.current_price - self.previous_close) / self.previous_close) * 100
        return 0
    
    def update_price_random(self, volatility=0.02):
        """
        Update stock price with random fluctuation
        volatility: percentage (0.02 = ±2% change)
        """
        # Generate random percentage change between -volatility and +volatility
        change_percent = random.uniform(-volatility, volatility)
        
        # Ensure current_price is float
        current = float(self.current_price)
        
        # Calculate new price
        new_price = current * (1 + change_percent)
        
        # Ensure price doesn't go below $0.01
        new_price = max(0.01, new_price)
        
        # Update prices
        self.previous_close = current
        self.current_price = round(new_price, 2)
        self.save()
        
        return self.current_price


class SimulatorSettings(models.Model):
    """Global settings for the stock market simulator"""
    setting_name = models.CharField(max_length=50, unique=True, primary_key=True, db_column='setting_name')
    setting_value = models.TextField()
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Simulator Setting"
        verbose_name_plural = "Simulator Settings"
        db_table = 'app1_simulatorsettings'

    def __str__(self):
        return f"{self.setting_name}: {self.setting_value}"

    @classmethod
    def get_default_balance(cls):
        """Get the default starting balance for new users"""
        try:
            setting = cls.objects.get(setting_name='default_user_balance')
            return float(setting.setting_value)
        except (cls.DoesNotExist, ValueError):
            return 10000.0

    @classmethod
    def set_default_balance(cls, amount):
        """Set the default starting balance for new users"""
        setting, created = cls.objects.update_or_create(
            setting_name='default_user_balance',
            defaults={
                'setting_value': str(amount),
                'description': 'Default starting balance for new user accounts'
            }
        )
        return setting


class Event(models.Model):
    """Trading competition event"""
    name = models.CharField(max_length=200, help_text="Event name (e.g., 'Spring Trading Challenge 2025')")
    description = models.TextField(blank=True, help_text="Event description and rules")
    start_time = models.DateTimeField(help_text="Event start date and time")
    end_time = models.DateTimeField(help_text="Event end date and time")
    initial_capital = models.DecimalField(max_digits=12, decimal_places=2, default=100000.00, help_text="Starting balance for each team")
    is_active = models.BooleanField(default=False, help_text="Is event currently active?")
    registration_open = models.BooleanField(default=True, help_text="Can teams register?")
    allow_short_selling = models.BooleanField(default=False, help_text="Allow teams to short sell?")
    max_trades_per_team = models.IntegerField(null=True, blank=True, help_text="Maximum trades per team (leave empty for unlimited)")
    trading_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Trading fee as percentage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"

    @property
    def is_registration_open(self):
        """Check if registration is still open"""
        return self.registration_open

    @property
    def status(self):
        """Get event status"""
        from django.utils import timezone
        now = timezone.now()
        if self.is_active:
            return "LIVE"
        elif now < self.start_time:
            return "UPCOMING"
        elif now > self.end_time:
            return "ENDED"
        else:
            return "SCHEDULED"


class Team(models.Model):
    """Trading team for competition"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams')
    team_name = models.CharField(max_length=100, help_text="Team name")
    team_code = models.CharField(max_length=20, unique=True, help_text="Unique team code (e.g., TEAM-X7K2)")
    password = models.CharField(max_length=128, help_text="Team password for login")
    
    # Team info
    leader_name = models.CharField(max_length=100, help_text="Team leader name")
    leader_email = models.EmailField(help_text="Team leader email")
    members = models.JSONField(default=list, help_text="List of team member names")
    
    # Trading data
    balance = models.DecimalField(max_digits=15, decimal_places=2, help_text="Current available cash")
    portfolio = models.JSONField(default=dict, help_text="Stock holdings: {symbol: {quantity: int, avg_price: float}}")
    trade_history = models.JSONField(default=list, help_text="List of all trades")
    total_trades = models.IntegerField(default=0, help_text="Total number of trades made")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Is team active in competition?")
    is_disqualified = models.BooleanField(default=False, help_text="Has team been disqualified?")
    disqualification_reason = models.TextField(blank=True)
    
    # Timestamps
    registration_time = models.DateTimeField(auto_now_add=True)
    last_trade_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['team_name']
        unique_together = ['event', 'team_name']
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"{self.team_code} - {self.team_name}"

    @property
    def portfolio_value(self):
        """Calculate total portfolio value (cash + holdings)"""
        holdings_value = 0
        for symbol, data in self.portfolio.items():
            try:
                stock = Stock.objects.get(symbol=symbol)
                holdings_value += float(stock.current_price) * data.get('quantity', 0)
            except Stock.DoesNotExist:
                pass
        return float(self.balance) + holdings_value

    @property
    def profit_loss(self):
        """Calculate profit/loss from initial capital"""
        return self.portfolio_value - float(self.event.initial_capital)

    @property
    def profit_loss_percent(self):
        """Calculate profit/loss percentage"""
        initial = float(self.event.initial_capital)
        if initial > 0:
            return (self.profit_loss / initial) * 100
        return 0

    @property
    def rank(self):
        """Get team's rank in the event"""
        # Get all active teams and sort by portfolio value in Python
        teams = self.event.teams.filter(is_active=True, is_disqualified=False)
        ranked_teams = sorted(teams, key=lambda t: t.portfolio_value, reverse=True)
        try:
            return ranked_teams.index(self) + 1
        except ValueError:
            return None


# MarketEvent model temporarily disabled
# Will be added after site is working properly
# See STOCK_API_GUIDE.md for instructions