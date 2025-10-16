from django.urls import path
from .views import (
    home, signup, user_login, createuser, logout, dashboard, stockdetails, 
    removewatchlist, updatestocks, user_portfolio, errorpage, settings, health_check,
    team_signup, team_login, team_dashboard, team_logout,
    team_stocks, team_trade, team_portfolio, team_stock_prices_api
)

from .apis import search,watchlist,fetchdetails,graphdata,portfolio,portfoliochart,income,holdings,addtoWatchlist,trigger_price_update

urlpatterns = [
    path('health', health_check, name="health"),
    path('',dashboard,name="home"),
    
    # Individual user auth
    path('signup',signup,name="signup"),
    path('login',user_login,name="login"),
    path('createuser',createuser,name="createuser"),
    path('logout',logout,name="logout"),
    
    # Team Auth
    path("team/signup", team_signup, name="team_signup"),
    path("team/login", team_login, name="team_login"),
    path("team/dashboard", team_dashboard, name="team_dashboard"),
    path("team/logout", team_logout, name="team_logout"),
    
    # Team Trading
    path("team/stocks", team_stocks, name="team_stocks"),
    path("team/trade/<str:symbol>", team_trade, name="team_trade"),
    path("team/portfolio", team_portfolio, name="team_portfolio"),
    path("team/api/stock-prices", team_stock_prices_api, name="team_stock_prices_api"),
    
    # User dashboard
    path('dashboard',dashboard,name="dashboard"),
    path('details/<str:query>',stockdetails,name="stockdetails"),
    path('removewatchlist/<str:symbol>',removewatchlist,name="removewatchlist"),
    path('portfolio',user_portfolio,name="user_portfolio"),
    path('updatestocks',updatestocks,name="updatestocks"),
    path('errorpage',errorpage,name="errorpage"),
    path('settings',settings,name="settings"),
    
    # APIs
    path('api/search/<str:query>',search,name="search"),
    path('api/watchlist/<str:query>',watchlist,name="watchlist"),
    path('api/addtowatchlist/<str:query>',addtoWatchlist,name="addtoWatchlist"),
    path('api/fetchdetails/<str:query>',fetchdetails,name="fetchdetails"),
    path('api/graphdata/<str:query>/<str:start>/<str:end>',graphdata,name="graphdata"),
    path('api/portfolio',portfolio,name="portfolio"),
    path('api/portfoliochart',portfoliochart,name="portfoliochart"),
    path('api/incomecalculate',income,name="income"),
    path('api/update-prices',trigger_price_update,name="trigger_price_update"),
    path('api/holdings/<str:query>',holdings,name="holdings"),
]