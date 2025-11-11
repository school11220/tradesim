from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import users, Stock, SimulatorSettings, Event, Team, MarketNews
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import path

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
        balance_str = f'₹{obj.balance:,.2f}'
        return format_html(
            '<strong style="color: {};">{}</strong>',
            color,
            balance_str
        )
    balance_display.short_description = 'Balance'
    balance_display.admin_order_field = 'balance'

    actions = ['reset_balance', 'add_bonus_1000', 'add_bonus_5000']

    def reset_balance(self, request, queryset):
        """Reset selected users' balance to default"""
        default_balance = SimulatorSettings.get_default_balance()
        count = queryset.update(balance=default_balance)
        self.message_user(request, f'Reset balance to ₹{default_balance:,.2f} for {count} user(s).')
    reset_balance.short_description = "Reset balance to default"

    def add_bonus_1000(self, request, queryset):
        """Add ₹1000 bonus to selected users"""
        for user in queryset:
            user.balance += 1000
            user.save()
        self.message_user(request, f'Added ₹1,000 bonus to {queryset.count()} user(s).')
    add_bonus_1000.short_description = "Add 1000 dollar bonus"

    def add_bonus_5000(self, request, queryset):
        """Add ₹5000 bonus to selected users"""
        for user in queryset:
            user.balance += 5000
            user.save()
        self.message_user(request, f'Added ₹5,000 bonus to {queryset.count()} user(s).')
    add_bonus_5000.short_description = "Add 5000 dollar bonus"


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """Admin interface for managing stock prices with custom controls"""
    list_display = ('symbol', 'name', 'sector', 'current_price_display', 'price_change_display', 'is_active')
    list_filter = ('is_active', 'sector')
    search_fields = ('symbol', 'name')
    ordering = ('symbol',)
    actions = ['apply_custom_percentage', 'adjust_sector_prices']
    
    readonly_fields = ('last_updated', 'created_at')
    
    fieldsets = (
        ('Stock Information', {
            'fields': ('symbol', 'name', 'sector', 'is_active')
        }),
        ('Price Settings', {
            'fields': ('current_price', 'previous_close', 'last_updated'),
            'description': 'Manually set stock prices or use bulk actions below'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom-price-control/', self.admin_site.admin_view(self.custom_price_control), name='stock_custom_price_control'),
            path('sector-control/', self.admin_site.admin_view(self.sector_control), name='stock_sector_control'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_controls'] = True
        return super().changelist_view(request, extra_context)
    
    def current_price_display(self, obj):
        """Display current price formatted"""
        return format_html('<strong style="color: #1e40af;">₹{}</strong>', f'{float(obj.current_price):.2f}')
    current_price_display.short_description = 'Current Price'
    
    def price_change_display(self, obj):
        """Display price change with color"""
        change = float(obj.price_change)
        change_pct = float(obj.price_change_percent)
        if change > 0:
            return format_html(
                '<span style="color: green;">▲ +₹{} (+{}%)</span>',
                f'{change:.2f}', f'{change_pct:.2f}'
            )
        elif change < 0:
            return format_html(
                '<span style="color: red;">▼ ₹{} ({}%)</span>',
                f'{change:.2f}', f'{change_pct:.2f}'
            )
        return format_html('<span style="color: gray;">—</span>')
    price_change_display.short_description = 'Change'
    
    def apply_custom_percentage(self, request, queryset):
        """Apply custom percentage change to selected stocks"""
        if 'apply' in request.POST:
            percentage = float(request.POST.get('percentage', 0))
            count = 0
            for stock in queryset:
                stock.previous_close = float(stock.current_price)
                stock.current_price = float(stock.current_price) * (1 + percentage / 100)
                stock.save()
                count += 1
            self.message_user(request, f'Applied {percentage:+.2f}% change to {count} stock(s).')
            return redirect('admin:app1_stock_changelist')
        
        context = {
            'stocks': queryset,
            'action_name': 'apply_custom_percentage',
            'title': 'Apply Custom Percentage Change'
        }
        return render(request, 'admin/stock_custom_percentage.html', context)
    
    apply_custom_percentage.short_description = "Apply custom percentage change"
    
    def adjust_sector_prices(self, request, queryset):
        """Redirect to sector-based control panel"""
        return redirect('admin:stock_sector_control')
    
    adjust_sector_prices.short_description = "Adjust prices by sector"
    
    def custom_price_control(self, request):
        """Custom price control interface"""
        stocks = Stock.objects.all()
        
        if request.method == 'POST':
            action_type = request.POST.get('action_type')
            
            if action_type == 'individual':
                for stock in stocks:
                    new_price = request.POST.get(f'price_{stock.symbol}')
                    if new_price:
                        try:
                            stock.previous_close = float(stock.current_price)
                            stock.current_price = float(new_price)
                            stock.save()
                        except ValueError:
                            pass
                self.message_user(request, 'Individual stock prices updated successfully.')
                
            elif action_type == 'percentage':
                percentage = float(request.POST.get('percentage', 0))
                selected = request.POST.getlist('stocks')
                count = 0
                for symbol in selected:
                    try:
                        stock = Stock.objects.get(symbol=symbol)
                        stock.previous_close = float(stock.current_price)
                        stock.current_price = float(stock.current_price) * (1 + percentage / 100)
                        stock.save()
                        count += 1
                    except Stock.DoesNotExist:
                        pass
                self.message_user(request, f'Applied {percentage:+.2f}% to {count} stock(s).')
            
            return redirect('admin:app1_stock_changelist')
        
        context = {
            'stocks': stocks,
            'sectors': Stock.objects.values_list('sector', flat=True).distinct(),
            'title': 'Custom Stock Price Control',
            'site_title': 'Stock Administration',
            'has_permission': True,
        }
        return render(request, 'admin/stock_price_control.html', context)
    
    def sector_control(self, request):
        """Sector-based price adjustment interface"""
        sectors = Stock.objects.values_list('sector', flat=True).distinct().order_by('sector')
        
        if request.method == 'POST':
            for sector in sectors:
                percentage_key = f'percentage_{sector}'
                percentage = request.POST.get(percentage_key)
                
                if percentage:
                    try:
                        percentage = float(percentage)
                        stocks = Stock.objects.filter(sector=sector)
                        for stock in stocks:
                            stock.previous_close = float(stock.current_price)
                            stock.current_price = float(stock.current_price) * (1 + percentage / 100)
                            stock.save()
                    except ValueError:
                        pass
            
            self.message_user(request, 'Sector prices updated successfully.')
            return redirect('admin:app1_stock_changelist')
        
        # Get stock counts by sector
        sector_data = []
        for sector in sectors:
            stock_count = Stock.objects.filter(sector=sector).count()
            sector_data.append({
                'name': sector,
                'count': stock_count,
                'stocks': Stock.objects.filter(sector=sector)
            })
        
        context = {
            'sector_data': sector_data,
            'title': 'Sector-Based Price Control',
            'site_title': 'Stock Administration',
            'has_permission': True,
        }
        return render(request, 'admin/stock_sector_control.html', context)


@admin.register(SimulatorSettings)
class SimulatorSettingsAdmin(admin.ModelAdmin):
    """Admin interface for global simulator settings"""
    list_display = ('setting_name', 'setting_value', 'description', 'last_updated')
    search_fields = ('setting_name', 'description')
    ordering = ('setting_name',)
    
    fieldsets = (
        ('Setting', {
            'fields': ('setting_name', 'setting_value', 'description')
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
            return mark_safe('<span style="color: green;">✓ Active</span>')
        return mark_safe('<span style="color: gray;">○ Inactive</span>')
    is_active_display.short_description = 'Active'
    
    def registration_status(self, obj):
        """Display registration status"""
        if obj.registration_open:
            return mark_safe('<span style="color: green;">✓ Open</span>')
        return mark_safe('<span style="color: red;">✗ Closed</span>')
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
    start_event.short_description = "START selected events"
    
    def stop_event(self, request, queryset):
        """Stop selected events"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} event(s) stopped successfully!')
    stop_event.short_description = "STOP selected events"
    
    def open_registration(self, request, queryset):
        """Open registration for selected events"""
        updated = queryset.update(registration_open=True)
        self.message_user(request, f'Registration opened for {updated} event(s)!')
    open_registration.short_description = "Open registration"
    
    def close_registration(self, request, queryset):
        """Close registration for selected events"""
        updated = queryset.update(registration_open=False)
        self.message_user(request, f'Registration closed for {updated} event(s)!')
    close_registration.short_description = "Close registration"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for monitoring teams (ADMIN ONLY - Teams can't see each other)"""
    list_display = ('team_code', 'team_name', 'event', 'leader_name', 'portfolio_value_display', 'profit_loss_display', 'total_trades', 'is_active_display', 'last_trade_time')
    list_filter = ('event', 'is_active', 'is_disqualified', 'registration_time')
    search_fields = ('team_code', 'team_name', 'leader_name', 'leader_email')
    ordering = ('-registration_time',)
    readonly_fields = ('team_code', 'registration_time', 'portfolio_value_display', 'profit_loss_display', 'profit_loss_percent_display', 'rank_display', 'trade_history_display')
    change_list_template = 'admin/team_leaderboard.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('leaderboard/', self.admin_site.admin_view(self.leaderboard_view), name='team_leaderboard'),
        ]
        return custom_urls + urls
    
    def leaderboard_view(self, request):
        """Display team leaderboard with sorting"""
        from django.db.models import F, FloatField, ExpressionWrapper
        from app1.models import Stock
        
        # Get filter parameters
        event_id = request.GET.get('event', None)
        sort_by = request.GET.get('sort', 'portfolio_value')
        order = request.GET.get('order', 'desc')
        
        # Base queryset
        teams = Team.objects.filter(is_active=True)
        
        # Filter by event if specified
        if event_id:
            teams = teams.filter(event_id=event_id)
        
        # Calculate portfolio values for each team
        team_data = []
        for team in teams:
            # Calculate portfolio value
            portfolio_value = float(team.balance)
            holdings_value = 0
            
            for symbol, holding in team.portfolio.items():
                try:
                    stock = Stock.objects.get(symbol=symbol, is_active=True)
                    holdings_value += holding['quantity'] * float(stock.current_price)
                except Stock.DoesNotExist:
                    pass
            
            portfolio_value += holdings_value
            
            # Calculate P/L
            initial_capital = float(team.event.initial_capital)
            profit_loss = portfolio_value - initial_capital
            profit_loss_percent = (profit_loss / initial_capital * 100) if initial_capital > 0 else 0
            
            team_data.append({
                'team': team,
                'portfolio_value': portfolio_value,
                'balance': float(team.balance),
                'holdings_value': holdings_value,
                'profit_loss': profit_loss,
                'profit_loss_percent': profit_loss_percent,
                'total_trades': team.total_trades,
                'initial_capital': initial_capital,
            })
        
        # Sort teams
        reverse = (order == 'desc')
        if sort_by == 'portfolio_value':
            team_data.sort(key=lambda x: x['portfolio_value'], reverse=reverse)
        elif sort_by == 'profit_loss':
            team_data.sort(key=lambda x: x['profit_loss'], reverse=reverse)
        elif sort_by == 'profit_loss_percent':
            team_data.sort(key=lambda x: x['profit_loss_percent'], reverse=reverse)
        elif sort_by == 'total_trades':
            team_data.sort(key=lambda x: x['total_trades'], reverse=reverse)
        elif sort_by == 'balance':
            team_data.sort(key=lambda x: x['balance'], reverse=reverse)
        elif sort_by == 'holdings_value':
            team_data.sort(key=lambda x: x['holdings_value'], reverse=reverse)
        
        # Add rank to each team
        for idx, team_info in enumerate(team_data, 1):
            team_info['rank'] = idx
        
        # Get all events for filter dropdown
        events = Event.objects.all().order_by('-start_time')
        
        context = {
            'team_data': team_data,
            'events': events,
            'selected_event': event_id,
            'sort_by': sort_by,
            'order': order,
            'title': 'Team Leaderboard',
            'site_title': 'TradeWars Admin',
            'has_permission': True,
        }
        
        return render(request, 'admin/team_leaderboard_full.html', context)
    
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
        try:
            value = obj.portfolio_value
            color = 'green' if value >= float(obj.event.initial_capital) else 'red'
            return format_html(
                '<strong style="color: {}; font-size: 1.1em;">₹{:,.2f}</strong>',
                color,
                float(value)
            )
        except (ValueError, TypeError, AttributeError):
            return format_html('<strong>₹0.00</strong>')
    portfolio_value_display.short_description = 'Portfolio Value'
    
    def profit_loss_display(self, obj):
        """Display profit/loss amount"""
        pl = obj.profit_loss
        color = 'green' if pl >= 0 else 'red'
        symbol = '+' if pl >= 0 else ''
        pl_str = f'{symbol}{pl:,.2f}'
        return format_html(
            '<strong style="color: {};">{}</strong>',
            color,
            pl_str
        )
    profit_loss_display.short_description = 'Profit/Loss'
    
    def profit_loss_percent_display(self, obj):
        """Display profit/loss percentage"""
        percent = obj.profit_loss_percent
        color = 'green' if percent >= 0 else 'red'
        symbol = '+' if percent >= 0 else ''
        return format_html(
            '<strong style="color: {};">{}{:.2f}%%</strong>',
            color,
            symbol,
            percent
        )
    profit_loss_percent_display.short_description = 'P/L Percent'
    
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
            return mark_safe('<span style="color: red;">✗ Disqualified</span>')
        if obj.is_active:
            return mark_safe('<span style="color: green;">✓ Active</span>')
        return mark_safe('<span style="color: gray;">○ Inactive</span>')
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
                <td>₹{trade.get("price", 0):.2f}</td>
                <td>₹{trade.get("total", 0):.2f}</td>
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
    reset_balance.short_description = "Reset to initial capital"
    
    def disqualify_team(self, request, queryset):
        """Disqualify selected teams"""
        updated = queryset.update(is_disqualified=True, is_active=False)
        self.message_user(request, f'{updated} team(s) disqualified!')
    disqualify_team.short_description = "Disqualify teams"
    
    def activate_team(self, request, queryset):
        """Activate selected teams"""
        updated = queryset.update(is_disqualified=False, is_active=True)
        self.message_user(request, f'{updated} team(s) activated!')
    activate_team.short_description = "Activate teams"


@admin.register(MarketNews)
class MarketNewsAdmin(admin.ModelAdmin):
    """Admin interface for managing market news and events"""
    list_display = ('title', 'impact_badge', 'severity_badge', 'affected_display', 'published_at', 'is_active')
    list_filter = ('is_active', 'impact_direction', 'severity', 'published_at')
    search_fields = ('title', 'content', 'trading_hint')
    ordering = ('-published_at',)
    
    fieldsets = (
        ('News Content', {
            'fields': ('title', 'content', 'trading_hint')
        }),
        ('Market Impact', {
            'fields': ('impact_direction', 'severity'),
            'description': 'Define how this news affects the market'
        }),
        ('Affected Entities', {
            'fields': ('affected_sectors', 'affected_stocks'),
            'description': 'Select which sectors/stocks are affected. Leave empty for market-wide news.'
        }),
        ('Visibility', {
            'fields': ('is_active', 'expires_at'),
            'description': 'Control when and if this news is visible to teams'
        }),
    )
    
    readonly_fields = ('published_at',)
    
    def impact_badge(self, obj):
        """Display impact with emoji and color"""
        colors = {
            'positive': '#10b981',
            'negative': '#ef4444',
            'neutral': '#6b7280',
            'mixed': '#f59e0b',
        }
        color = colors.get(obj.impact_direction, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold;">{} {}</span>',
            color,
            obj.impact_emoji,
            obj.get_impact_direction_display()
        )
    impact_badge.short_description = 'Impact'
    
    def severity_badge(self, obj):
        """Display severity with color coding"""
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold;">{}</span>',
            obj.severity_color,
            obj.get_severity_display()
        )
    severity_badge.short_description = 'Severity'
    
    def affected_display(self, obj):
        """Display what's affected in a readable format"""
        parts = []
        if obj.affected_sectors:
            parts.append(f"{len(obj.affected_sectors)} sector(s)")
        if obj.affected_stocks:
            parts.append(f"{len(obj.affected_stocks)} stock(s)")
        if not parts:
            return format_html('<span style="color: #6b7280;">Market-wide</span>')
        return format_html('<span style="color: #6366f1;">{}</span>', ', '.join(parts))
    affected_display.short_description = 'Affects'
    
    actions = ['activate_news', 'deactivate_news', 'extend_expiry']
    
    def activate_news(self, request, queryset):
        """Activate selected news items"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} news item(s) activated!')
    activate_news.short_description = "✅ Activate news"
    
    def deactivate_news(self, request, queryset):
        """Deactivate selected news items"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} news item(s) deactivated!')
    deactivate_news.short_description = "❌ Deactivate news"
    
    def extend_expiry(self, request, queryset):
        """Extend expiry by 24 hours"""
        from datetime import timedelta
        for news in queryset:
            if news.expires_at:
                news.expires_at += timedelta(hours=24)
            else:
                news.expires_at = timezone.now() + timedelta(hours=24)
            news.save()
        self.message_user(request, f'Extended expiry for {queryset.count()} news item(s) by 24 hours!')
    extend_expiry.short_description = "⏰ Extend expiry +24h"


# Customize admin site headers
admin.site.site_header = "TradeWars Market Control Center"
admin.site.site_title = "TradeWars Admin"
admin.site.index_title = "Market Control Dashboard"