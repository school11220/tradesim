from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import users, Stock, SimulatorSettings, Event, Team
from django.utils.html import format_html
from django.utils import timezone

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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for managing trading events"""
    list_display = ('name', 'status_display', 'start_time', 'end_time', 'initial_capital', 'team_count', 'is_active_display', 'registration_status')
    list_filter = ('is_active', 'registration_open', 'start_time')
    search_fields = ('name', 'description')
    ordering = ('-start_time',)
    
    fieldsets = (
        ('Event Details', {
            'fields': ('name', 'description')
        }),
        ('Schedule', {
            'fields': ('start_time', 'end_time')
        }),
        ('Trading Configuration', {
            'fields': ('initial_capital', 'allow_short_selling', 'max_trades_per_team', 'trading_fee_percentage')
        }),
        ('Status', {
            'fields': ('is_active', 'registration_open'),
            'description': 'Control event and registration status'
        }),
    )
    
    actions = ['start_event', 'stop_event', 'open_registration', 'close_registration']
    
    def status_display(self, obj):
        """Display event status with color"""
        status = obj.status
        colors = {
            'LIVE': 'green',
            'UPCOMING': 'blue',
            'ENDED': 'gray',
            'SCHEDULED': 'orange'
        }
        return format_html(
            '<strong style="color: {};">{}</strong>',
            colors.get(status, 'black'),
            status
        )
    status_display.short_description = 'Status'
    
    def is_active_display(self, obj):
        """Display active status"""
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: gray;">○ Inactive</span>')
    is_active_display.short_description = 'Active'
    
    def registration_status(self, obj):
        """Display registration status"""
        if obj.registration_open:
            return format_html('<span style="color: green;">✓ Open</span>')
        return format_html('<span style="color: red;">✗ Closed</span>')
    registration_status.short_description = 'Registration'
    
    def team_count(self, obj):
        """Display number of registered teams"""
        count = obj.teams.count()
        return format_html('<strong>{}</strong> teams', count)
    team_count.short_description = 'Teams'
    
    def start_event(self, request, queryset):
        """Start selected events"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} event(s) started successfully!')
    start_event.short_description = "▶️ START selected events"
    
    def stop_event(self, request, queryset):
        """Stop selected events"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} event(s) stopped successfully!')
    stop_event.short_description = "⏸️ STOP selected events"
    
    def open_registration(self, request, queryset):
        """Open registration for selected events"""
        updated = queryset.update(registration_open=True)
        self.message_user(request, f'Registration opened for {updated} event(s)!')
    open_registration.short_description = "🔓 Open registration"
    
    def close_registration(self, request, queryset):
        """Close registration for selected events"""
        updated = queryset.update(registration_open=False)
        self.message_user(request, f'Registration closed for {updated} event(s)!')
    close_registration.short_description = "🔒 Close registration"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for monitoring teams (ADMIN ONLY - Teams can't see each other)"""
    list_display = ('team_code', 'team_name', 'event', 'leader_name', 'portfolio_value_display', 'profit_loss_display', 'total_trades', 'is_active_display', 'last_trade_time')
    list_filter = ('event', 'is_active', 'is_disqualified', 'registration_time')
    search_fields = ('team_code', 'team_name', 'leader_name', 'leader_email')
    ordering = ('-registration_time',)
    readonly_fields = ('team_code', 'registration_time', 'portfolio_value_display', 'profit_loss_display', 'profit_loss_percent_display', 'rank_display', 'trade_history_display')
    
    fieldsets = (
        ('Team Information', {
            'fields': ('event', 'team_code', 'team_name', 'password')
        }),
        ('Team Leader', {
            'fields': ('leader_name', 'leader_email')
        }),
        ('Team Members', {
            'fields': ('members',)
        }),
        ('Portfolio Overview', {
            'fields': ('portfolio_value_display', 'balance', 'profit_loss_display', 'profit_loss_percent_display', 'rank_display'),
            'description': 'Real-time portfolio metrics'
        }),
        ('Holdings & Trades', {
            'fields': ('portfolio', 'total_trades', 'last_trade_time', 'trade_history_display'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_disqualified', 'disqualification_reason')
        }),
        ('Timestamps', {
            'fields': ('registration_time',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['reset_balance', 'disqualify_team', 'activate_team', 'view_detailed_portfolio']
    
    def portfolio_value_display(self, obj):
        """Display total portfolio value"""
        value = obj.portfolio_value
        color = 'green' if value >= float(obj.event.initial_capital) else 'red'
        return format_html(
            '<strong style="color: {}; font-size: 1.1em;">${:,.2f}</strong>',
            color,
            value
        )
    portfolio_value_display.short_description = 'Portfolio Value'
    
    def profit_loss_display(self, obj):
        """Display profit/loss amount"""
        pl = obj.profit_loss
        color = 'green' if pl >= 0 else 'red'
        symbol = '+' if pl >= 0 else ''
        return format_html(
            '<strong style="color: {};">{}{:,.2f}</strong>',
            color,
            symbol,
            pl
        )
    profit_loss_display.short_description = 'Profit/Loss'
    
    def profit_loss_percent_display(self, obj):
        """Display profit/loss percentage"""
        percent = obj.profit_loss_percent
        color = 'green' if percent >= 0 else 'red'
        symbol = '+' if percent >= 0 else ''
        return format_html(
            '<strong style="color: {};">{}{:.2f}%</strong>',
            color,
            symbol,
            percent
        )
    profit_loss_percent_display.short_description = 'P/L %'
    
    def rank_display(self, obj):
        """Display team rank"""
        rank = obj.rank
        if rank:
            medal = '🥇' if rank == 1 else '🥈' if rank == 2 else '🥉' if rank == 3 else f'#{rank}'
            return format_html('<strong style="font-size: 1.2em;">{}</strong>', medal)
        return '-'
    rank_display.short_description = 'Rank'
    
    def is_active_display(self, obj):
        """Display active status"""
        if obj.is_disqualified:
            return format_html('<span style="color: red;">❌ Disqualified</span>')
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: gray;">○ Inactive</span>')
    is_active_display.short_description = 'Status'
    
    def trade_history_display(self, obj):
        """Display formatted trade history"""
        if not obj.trade_history:
            return "No trades yet"
        
        html = '<table style="width:100%; border-collapse: collapse;">'
        html += '<tr style="background: #f0f0f0;"><th>Time</th><th>Type</th><th>Stock</th><th>Qty</th><th>Price</th><th>Total</th></tr>'
        
        for trade in obj.trade_history[-20:]:  # Last 20 trades
            html += f'''
            <tr>
                <td>{trade.get("time", "")}</td>
                <td style="color: {'green' if trade.get('type') == 'BUY' else 'red'};">{trade.get("type", "")}</td>
                <td><strong>{trade.get("symbol", "")}</strong></td>
                <td>{trade.get("quantity", 0)}</td>
                <td>${trade.get("price", 0):.2f}</td>
                <td>${trade.get("total", 0):.2f}</td>
            </tr>
            '''
        html += '</table>'
        return format_html(html)
    trade_history_display.short_description = 'Recent Trades'
    
    def reset_balance(self, request, queryset):
        """Reset teams to initial capital"""
        for team in queryset:
            team.balance = team.event.initial_capital
            team.portfolio = {}
            team.trade_history = []
            team.total_trades = 0
            team.save()
        self.message_user(request, f'{queryset.count()} team(s) reset to initial capital!')
    reset_balance.short_description = "🔄 Reset to initial capital"
    
    def disqualify_team(self, request, queryset):
        """Disqualify selected teams"""
        updated = queryset.update(is_disqualified=True, is_active=False)
        self.message_user(request, f'{updated} team(s) disqualified!')
    disqualify_team.short_description = "❌ Disqualify teams"
    
    def activate_team(self, request, queryset):
        """Activate selected teams"""
        updated = queryset.update(is_disqualified=False, is_active=True)
        self.message_user(request, f'{updated} team(s) activated!')
    activate_team.short_description = "✓ Activate teams"


# Customize admin site headers
admin.site.site_header = "TradeSim Event Control Center"
admin.site.site_title = "TradeSim Admin"
admin.site.index_title = "Trading Competition Management"
admin.site.index_title = "Market Control Dashboard"