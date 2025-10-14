from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import users, Stock, SimulatorSettings
from django.utils.html import format_html

# Register your models here.
# ₹

@admin.register(users)
class CustomUserAdmin(UserAdmin):
    """Enhanced admin for user accounts with balance control"""
    list_display = ('username', 'email', 'firstname', 'lastname', 'balance_display', 'datajoined', 'is_active')
    list_filter = ('is_active', 'is_staff', 'datajoined')
    search_fields = ('username', 'email', 'firstname', 'lastname')
    ordering = ('-datajoined',)
    
    fieldsets = (
        ('Login Info', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('firstname', 'lastname', 'email')
        }),
        ('Trading Account', {
            'fields': ('balance', 'stockbuy', 'stocksold', 'watchlist', 'cache'),
            'description': 'Control user balance and view trading history'
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'datajoined'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('datajoined', 'last_login')
    
    def balance_display(self, obj):
        """Display balance with color coding"""
        color = 'green' if obj.balance >= 10000 else 'orange' if obj.balance >= 5000 else 'red'
        return format_html(
            '<strong style="color: {};">${:,.2f}</strong>',
            color,
            obj.balance
        )
    balance_display.short_description = 'Balance'
    balance_display.admin_order_field = 'balance'

    actions = ['reset_balance', 'add_bonus_1000', 'add_bonus_5000']

    def reset_balance(self, request, queryset):
        """Reset selected users' balance to default"""
        default_balance = SimulatorSettings.get_default_balance()
        count = queryset.update(balance=default_balance)
        self.message_user(request, f'Reset balance to ${default_balance:,.2f} for {count} user(s).')
    reset_balance.short_description = "Reset balance to default"

    def add_bonus_1000(self, request, queryset):
        """Add $1000 bonus to selected users"""
        for user in queryset:
            user.balance += 1000
            user.save()
        self.message_user(request, f'Added $1,000 bonus to {queryset.count()} user(s).')
    add_bonus_1000.short_description = "Add $1,000 bonus"

    def add_bonus_5000(self, request, queryset):
        """Add $5000 bonus to selected users"""
        for user in queryset:
            user.balance += 5000
            user.save()
        self.message_user(request, f'Added $5,000 bonus to {queryset.count()} user(s).')
    add_bonus_5000.short_description = "Add $5,000 bonus"


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """Admin interface for controlling stock prices"""
    list_display = ('symbol', 'name', 'current_price_display', 'previous_close', 'change_display', 'is_active', 'last_updated')
    list_filter = ('is_active', 'last_updated')
    search_fields = ('symbol', 'name')
    ordering = ('symbol',)
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Stock Information', {
            'fields': ('symbol', 'name', 'is_active')
        }),
        ('Price Control', {
            'fields': ('current_price', 'previous_close'),
            'description': 'Set stock prices directly here. Changes take effect immediately.'
        }),
        ('Timestamps', {
            'fields': ('last_updated', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('last_updated', 'created_at')
    
    def current_price_display(self, obj):
        """Display current price formatted"""
        return format_html('<strong>${:,.2f}</strong>', obj.current_price)
    current_price_display.short_description = 'Current Price'
    current_price_display.admin_order_field = 'current_price'
    
    def change_display(self, obj):
        """Display price change with color coding"""
        change = obj.price_change
        percent = obj.price_change_percent
        color = 'green' if change >= 0 else 'red'
        arrow = '↑' if change >= 0 else '↓'
        return format_html(
            '<span style="color: {};">{} ${:,.2f} ({:+.2f}%)</span>',
            color, arrow, abs(change), percent
        )
    change_display.short_description = 'Change'
    
    actions = ['increase_price_10', 'decrease_price_10', 'set_previous_to_current', 'activate_stocks', 'deactivate_stocks']
    
    def increase_price_10(self, request, queryset):
        """Increase price by 10%"""
        for stock in queryset:
            stock.current_price *= 1.10
            stock.save()
        self.message_user(request, f'Increased price by 10% for {queryset.count()} stock(s).')
    increase_price_10.short_description = "Increase price by 10%"
    
    def decrease_price_10(self, request, queryset):
        """Decrease price by 10%"""
        for stock in queryset:
            stock.current_price *= 0.90
            stock.save()
        self.message_user(request, f'Decreased price by 10% for {queryset.count()} stock(s).')
    decrease_price_10.short_description = "Decrease price by 10%"
    
    def set_previous_to_current(self, request, queryset):
        """Set previous close to current price (reset change to 0)"""
        for stock in queryset:
            stock.previous_close = stock.current_price
            stock.save()
        self.message_user(request, f'Reset previous close for {queryset.count()} stock(s).')
    set_previous_to_current.short_description = "Set previous close = current price"
    
    def activate_stocks(self, request, queryset):
        """Activate selected stocks"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'Activated {count} stock(s).')
    activate_stocks.short_description = "Activate stocks"
    
    def deactivate_stocks(self, request, queryset):
        """Deactivate selected stocks"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'Deactivated {count} stock(s).')
    deactivate_stocks.short_description = "Deactivate stocks"


@admin.register(SimulatorSettings)
class SimulatorSettingsAdmin(admin.ModelAdmin):
    """Admin interface for global simulator settings"""
    list_display = ('setting_key', 'setting_value', 'description', 'last_updated')
    search_fields = ('setting_key', 'description')
    ordering = ('setting_key',)
    
    fieldsets = (
        ('Setting', {
            'fields': ('setting_key', 'setting_value', 'description')
        }),
        ('Metadata', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('last_updated',)


# Customize admin site headers
admin.site.site_header = "TradeSim Admin Panel"
admin.site.site_title = "TradeSim Control Center"
admin.site.index_title = "Market Control Dashboard"