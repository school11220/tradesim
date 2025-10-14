from django.db import models
from django.contrib.auth.models import AbstractUser

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


class SimulatorSettings(models.Model):
    """Global settings for the stock market simulator"""
    setting_key = models.CharField(max_length=50, unique=True, primary_key=True)
    setting_value = models.TextField()
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Simulator Setting"
        verbose_name_plural = "Simulator Settings"

    def __str__(self):
        return f"{self.setting_key}: {self.setting_value}"

    @classmethod
    def get_default_balance(cls):
        """Get the default starting balance for new users"""
        try:
            setting = cls.objects.get(setting_key='default_user_balance')
            return float(setting.setting_value)
        except (cls.DoesNotExist, ValueError):
            return 10000.0

    @classmethod
    def set_default_balance(cls, amount):
        """Set the default starting balance for new users"""
        setting, created = cls.objects.update_or_create(
            setting_key='default_user_balance',
            defaults={
                'setting_value': str(amount),
                'description': 'Default starting balance for new user accounts'
            }
        )
        return setting