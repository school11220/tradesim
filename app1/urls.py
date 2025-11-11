from django.urls import path
from django.shortcuts import redirect
from .views import (
    home, signup, user_login, createuser, logout, dashboard, stockdetails, 
    removewatchlist, updatestocks, user_portfolio, errorpage, settings, health_check,
    team_signup, team_login, team_dashboard, team_logout,
    team_stocks, team_trade, team_portfolio, team_stock_prices_api, team_news
)

from .apis import (
    search, watchlist, fetchdetails, graphdata, portfolio, portfoliochart, 
    income, holdings, addtoWatchlist, trigger_price_update,
    update_prices_real, update_prices_auto, toggle_price_mode,
    get_market_events
)

urlpatterns = [
    path('health', health_check, name="health"),
    
    # Redirect root to team login
    path('', lambda request: redirect('team_login'), name="home"),
    
    # Disable individual user auth - redirect to team system
    path('signup', lambda request: redirect('team_login'), name="signup"),
    path('login', lambda request: redirect('team_login'), name="login"),
    path('createuser', lambda request: redirect('team_login'), name="createuser"),
    path('logout', lambda request: redirect('team_logout'), name="logout"),
    path('dashboard', lambda request: redirect('team_dashboard'), name="dashboard"),
    path('details/<str:query>', lambda request, query: redirect('team_stocks'), name="stockdetails"),
    path('portfolio', lambda request: redirect('team_portfolio'), name="user_portfolio"),
    path('settings', lambda request: redirect('team_dashboard'), name="settings"),
    
    # Team Auth (PRIMARY SYSTEM)
    path("team/signup", team_signup, name="team_signup"),
    path("team/login", team_login, name="team_login"),
    path("team/dashboard", team_dashboard, name="team_dashboard"),
    path("team/logout", team_logout, name="team_logout"),
    
    # Team Trading
    path("team/stocks", team_stocks, name="team_stocks"),
    path("team/trade/<str:symbol>", team_trade, name="team_trade"),
    path("team/portfolio", team_portfolio, name="team_portfolio"),
    path("team/news", team_news, name="team_news"),
    path("team/api/stock-prices", team_stock_prices_api, name="team_stock_prices_api"),
    
    # Disable individual user pages - redirect to team system
    path('removewatchlist/<str:symbol>', lambda request, symbol: redirect('team_dashboard'), name="removewatchlist"),
    path('updatestocks', lambda request: redirect('team_dashboard'), name="updatestocks"),
    path('errorpage', lambda request: redirect('team_dashboard'), name="errorpage"),
    
    # APIs
    path('api/search/<str:query>',search,name="search"),
    path('api/watchlist/<str:query>',watchlist,name="watchlist"),
    path('api/addtowatchlist/<str:query>',addtoWatchlist,name="addtoWatchlist"),
    path('api/fetchdetails/<str:query>',fetchdetails,name="fetchdetails"),
    path('api/graphdata/<str:query>/<str:start>/<str:end>',graphdata,name="graphdata"),
    path('api/portfolio',portfolio,name="portfolio"),
    path('api/portfoliochart',portfoliochart,name="portfoliochart"),
    path('api/incomecalculate',income,name="income"),
    path('api/holdings/<str:query>',holdings,name="holdings"),
    
    # Stock Price Update APIs
    path('api/update-prices', trigger_price_update, name="trigger_price_update"),
    path('api/update-prices-real', update_prices_real, name="update_prices_real"),
    path('api/update-prices-auto', update_prices_auto, name="update_prices_auto"),
    path('api/toggle-price-mode', toggle_price_mode, name="toggle_price_mode"),
    path('api/market-events', get_market_events, name="get_market_events"),
]