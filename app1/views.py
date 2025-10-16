from django.shortcuts import render,HttpResponse,redirect
from .models import users, Team, Event
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import requests as req
from .mdate import today
import secrets
import string

# Create your views here.
def home(requests):
    return HttpResponse("Hello World!!")

def health_check(request):
    """Simple health check endpoint for debugging"""
    import sys
    return HttpResponse(f"OK - Django {sys.version} - Database: {request.META.get('HTTP_HOST', 'unknown')}")

def signup(requests):
    data={"isusername":"hidden","isemail":"hidden"}
    return render(requests,"login/signup.html",data)

def user_login(requests):
    def checkusername(text):
        try:
            uname=users.objects.get(username=text)
            checkpword=uname.password
            return checkpword
        except:
            return 0
        
    if requests.method == "POST":
        uname=requests.POST.get("username")
        pword=requests.POST.get("password")

        iscorrectpword=checkusername(uname)
    
        if(iscorrectpword==0):
            data={"isusername":"visible","ispasswordcorrect":"hidden"}
            return render(requests,"login/login.html",data)
        else:
            if(iscorrectpword==pword):
                # existing_user = users.objects.get(username=uname)
                # existing_user.make_password(pword)
                # user=authenticate(requests,username=uname,password=pword)
                # print(user)
                auth_login(requests,users.objects.get(username=uname))
                return redirect("dashboard")
            else:
                data={"isusername":"hidden","ispasswordcorrect":"visible"}
                return render(requests,"login/login.html",data)
    
    data={"isusername":"hidden","ispasswordcorrect":"hidden"}
    return render(requests,"login/login.html",data)

def createuser(requests):
    if requests.method=="POST":
        uname=requests.POST.get("username")
        fname=requests.POST.get("first_name")
        lname=requests.POST.get("last_name")
        mail=requests.POST.get("email")
        pword=requests.POST.get("password")

        # print(uname,fname,lname,mail,pword)

        def checkusername(text):
            user_count=users.objects.filter(username=text).count()
            return user_count
        
        def checkemail(text):
            email_count=users.objects.filter(email=text).count()
            return email_count
        
        ucount=checkusername(uname)
        ecount=checkemail(mail)
        
        if(ucount==1 and ecount==1):
            data={"isusername":"visible","isemail":"visible"}
            return render(requests,"login/signup.html",data)

        if(ucount==1):
            data={"isusername":"visible","isemail":"hidden"}
            return render(requests,"login/signup.html",data)
        elif(ecount==1):
            data={"isusername":"hidden","isemail":"visible"}
            return render(requests,"login/signup.html",data)
        
        if(ucount==0 and ecount==0):
            adduser=users(username=uname,firstname=fname,lastname=lname,email=mail,password=pword,watchlist={"symbol":["SONY","MSFT","META","GOOG","AAPL"]})
            adduser.save()
            return redirect("login")
    else:
        return redirect("login")

# def logout(requests):
#     auth_logout(requests)
#     return HttpResponse("Logout!!")

def logout(requests):
    auth_logout(requests)
    return HttpResponse("Logout!!")

def user_a(requests):
    if requests.user.is_authenticated:
        user = requests.user
        print("--------User--------")
        print(user)
        
        # Ensure stockbuy is a dict
        if not isinstance(user.stockbuy, dict):
            user.stockbuy = {}
        
        stockname=user.stockbuy.keys()
        print(stockname)
        stock=[]
        price=[]
        for i in stockname:
            stock.append(i)
            price.append(user.stockbuy[i]["boughtat"]*user.stockbuy[i]["quantity"])
        print("Yes")
        user=requests.user
        print(user)
        print(user.watchlist)
        
        # Ensure watchlist exists and has symbol key
        if not isinstance(user.watchlist, dict):
            user.watchlist = {"symbol": ["SONY","MSFT","META","GOOG","AAPL"]}
        if "symbol" not in user.watchlist:
            user.watchlist["symbol"] = ["SONY","MSFT","META","GOOG","AAPL"]
        
        watchlistsymbols=""
        for i in user.watchlist["symbol"]:
            watchlistsymbols=i+","+watchlistsymbols
        # print(watchlistsymbols)
        data={
            "username":user.username,
            "name":user.firstname,
            "email":user.email,
            "totalbalance":round(user.balance,2),
            "watchlist":watchlistsymbols,
            "stocklist":user.watchlist["symbol"],
            "stock":list(stockname),
            "price":price,
            "start":today()-200000,
            "end":today(),
            "currentlyholding":"hidden",
        }
        return data

def dashboard(requests):
    try:
        if requests.user.is_authenticated:
            data = user_a(requests)

            data["title"]="Dashboard"
            print("---------------Data-----------------")
            print(data)
            print("---------------Data-----------------")
            return render(requests,"main/dashboard.html",data)
        else:
            return redirect("login")
    except Exception as e:
        print(f"Dashboard error: {e}")
        return redirect("login")

def stockdetails(requests,query):
    try:
        if requests.user.is_authenticated:
            todayepoch=int(today())
            start=str(todayepoch-457199)
            end=str(todayepoch)
            url="https://query2.finance.yahoo.com/v8/finance/chart/"+query+"?period1="+str(todayepoch-457199)+"&period2="+str(todayepoch)+"&interval=5m&includePrePost=true&events=div%7Csplit%7Cearn&&lang=en-US&region=US"
            headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
            response = req.get(url,headers=headers)
            data = response.json()

            store={}
            data=data["chart"]["result"][0]["meta"]
            previousclose=data["previousClose"]

            for i in data.keys():
                if i == ("firstTradeDate") or i == ("regularMarketTime") or i == ("hasPrePostMarketData") or i == ("gmtoffset") or i == ("timezone") or i == ("instrumentType") or i == ("fullExchangeName") or i == ("regularMarketVolume") or i == ("previousClose") or i == ("regularMarketPrice"):
                    continue
                if i == "scale":
                    break
                store[i.capitalize()]=data[i]
                
            
            print("Yes")
            user=requests.user
            
            # Ensure watchlist exists
            if not isinstance(user.watchlist, dict) or "symbol" not in user.watchlist:
                user.watchlist = {"symbol": ["SONY","MSFT","META","GOOG","AAPL"]}
            
            watchlistsymbols=""
            for i in user.watchlist["symbol"]:
                watchlistsymbols=i+","+watchlistsymbols
            # print(watchlistsymbols)
            data={
                "username":user.username,
                "name":user.firstname,
                "email":user.email,
                "totalbalance":round(user.balance,2),
                "watchlist":watchlistsymbols,
                "data":store,
                "query":query,
                "previousclose":previousclose,
                "start":start,
                "end":end,
                "title":query,
            }
            return render(requests,"main/details.html",data)
        else:
            return redirect("login")
    except Exception as e:
        print(f"Stockdetails error: {e}")
        return redirect("dashboard")

def removewatchlist(requests,symbol):
    # print(symbol)
    user = requests.user
    user.watchlist["symbol"].remove(symbol)

    # user.watchlist=wlist

    # remove=users(watchlist=wlist)
    user.save()
    return redirect("dashboard")


def updatestocks(requests):
    if requests.method == "POST":
        quantity=int(requests.POST.get("quantity-input"))
        print(quantity)
        name=requests.POST.get("symbolname")
        print(name)
        currentprice=float(requests.POST.get("currentprice"))
        print(currentprice)
        if "buy" in requests.POST:
            user = requests.user
            if(quantity==0):
                return render(requests,"main/error.html")
                # return redirect("Quantity Can not be 0")
            if(currentprice*quantity)>user.balance:
                return render(requests,"main/error.html")
                # return HttpResponse("Not Sufficient Balance")
            if (name in user.stockbuy.keys()):
                previousprice=user.stockbuy[name]["quantity"]*user.stockbuy[name]["boughtat"]
                currentshareprice=quantity*currentprice
                totalquantity=int(user.stockbuy[name]["quantity"])+int(quantity)
                averageprice=(previousprice+currentshareprice)/totalquantity
                user.stockbuy[name]={"quantity":totalquantity, "boughtat":currentprice, "averageprice":averageprice,"purchaseat":"date" }
                user.balance=user.balance-float(quantity*currentprice)
            else:
            # user.stockbuy={}
                user.stockbuy[name]={"quantity": quantity ,"boughtat": currentprice, "averageprice": currentprice,"purchaseat":"date" }
                user.balance=user.balance-float(quantity*currentprice)
            user.save()
            print("Buy")
        if "sell" in requests.POST:
            user=requests.user
            if (name in user.stockbuy.keys()):
                if quantity > user.stockbuy[name]["quantity"]:
                    return render(requests,"main/error.html")
                    # print("Not Enough Shares Holding")
                if user.stockbuy[name]["quantity"] == quantity:
                    print("Here")
                    user.stockbuy.pop(name)
                    user.balance=user.balance+(currentprice*quantity)
                    user.save()
                else:
                    user.stockbuy[name].update({"quantity":user.stockbuy[name]["quantity"]-quantity})
                    user.balance=user.balance+(currentprice*quantity)
                    user.save()
                    print("Sell")
            else:
                print("Quantity is 0")
            print("Sell")
    
        return(redirect('dashboard'))
    else:
        return render(requests,"login/login.html")

def user_portfolio(requests):
    try:
        if requests.user.is_authenticated:
            user = requests.user
            
            # Ensure stockbuy is a dict
            if not isinstance(user.stockbuy, dict):
                user.stockbuy = {}
            
            stockname=user.stockbuy.keys()
            stock=[]
            price=[]
            for i in stockname:
                stock.append(i)
                price.append(user.stockbuy[i]["boughtat"]*user.stockbuy[i]["quantity"])
            print("Yes")
            user=requests.user
            print(user)
            print(user.watchlist)
            
            # Ensure watchlist exists
            if not isinstance(user.watchlist, dict) or "symbol" not in user.watchlist:
                user.watchlist = {"symbol": ["SONY","MSFT","META","GOOG","AAPL"]}
            
            watchlistsymbols=""
            for i in user.watchlist["symbol"]:
                watchlistsymbols=i+","+watchlistsymbols
            
            # print(watchlistsymbols)
            data={
                "username":user.username,
                "name":user.firstname,
                "email":user.email,
                "totalbalance":round(user.balance,2),
                "watchlist":watchlistsymbols,
                "stock":stock,
                "price":price,
                "start":today()-70000,
                "end":today(),
                "currentlyholding":"hidden",
            }
            return render(requests,"main/portfolio.html",data)
        else:
            return redirect("login")
    except Exception as e:
        print(f"Portfolio error: {e}")
        return redirect("login")

def errorpage(requests):
    try:
        if requests.user.is_authenticated:
            user = requests.user
            
            # Ensure stockbuy is a dict
            if not isinstance(user.stockbuy, dict):
                user.stockbuy = {}
            
            stockname=user.stockbuy.keys()
            stock=[]
            price=[]
            for i in stockname:
                stock.append(i)
                price.append(user.stockbuy[i]["boughtat"]*user.stockbuy[i]["quantity"])
            print("Yes")
            user=requests.user
            print(user)
            print(user.watchlist)
            
            # Ensure watchlist exists
            if not isinstance(user.watchlist, dict) or "symbol" not in user.watchlist:
                user.watchlist = {"symbol": ["SONY","MSFT","META","GOOG","AAPL"]}
            
            watchlistsymbols=""
            for i in user.watchlist["symbol"]:
                watchlistsymbols=i+","+watchlistsymbols
            
            # print(watchlistsymbols)
            data={
                "username":user.username,
                "name":user.firstname,
                "email":user.email,
                "totalbalance":round(user.balance,2),
                "watchlist":watchlistsymbols,
                "stock":stock,
                "price":price,
            }
            return render(requests,"main/error.html",data)
        else:
            return redirect("login")
    except Exception as e:
        print(f"Errorpage error: {e}")
        return redirect("login")

def settings(requests):
    try:
        if requests.user.is_authenticated:
            data = user_a(requests)
            data["currentcheck"]="hidden"
            data["matchcheck"]="hidden"
            data["title"]="Settings"
            if requests.method == "POST":
                currentPass=requests.POST.get("currentpassword")
                newpass=requests.POST.get("newpassword")
                repeatpass=requests.POST.get("repeat-password")
                user = requests.user
                print("---------------------------------------")
                print(user.password)
                if (user.password == currentPass):
                    data["currentcheck"]="hidden"
                    if(newpass == repeatpass):
                        data["matchcheck"]="hidden"
                        user.password = newpass
                        user.save()
                    else:
                        print("Password Doesn't Match")
                        data["matchcheck"]="visible"
                else:
                    data["currentcheck"]="visible"
                    print("Password is Not Correct")
                print(currentPass)
                print(newpass)
                print(repeatpass)
            return render(requests,"main/settings.html",data)
        else:
            return redirect("login")
    except Exception as e:
        print(f"Settings error: {e}")
        return redirect("login")


# ============ TEAM REGISTRATION & LOGIN ============

def team_signup(request):
    """Team registration page"""
    data = {
        "error": None,
        "success": None,
        "events": Event.objects.filter(registration_open=True).order_by('-start_time')
    }
    
    if request.method == "POST":
        try:
            event_id = request.POST.get("event_id")
            team_name = request.POST.get("team_name")
            leader_name = request.POST.get("leader_name")
            leader_email = request.POST.get("leader_email")
            password = request.POST.get("password")
            members_str = request.POST.get("members", "")
            
            # Validation
            if not all([event_id, team_name, leader_name, leader_email, password]):
                data["error"] = "All fields are required"
                return render(request, "login/team_signup.html", data)
            
            # Check event exists and registration is open
            try:
                event = Event.objects.get(id=event_id)
                if not event.registration_open:
                    data["error"] = "Registration is closed for this event"
                    return render(request, "login/team_signup.html", data)
            except Event.DoesNotExist:
                data["error"] = "Event not found"
                return render(request, "login/team_signup.html", data)
            
            # Check if team name is already taken for this event
            if Team.objects.filter(event=event, team_name=team_name).exists():
                data["error"] = f"Team name '{team_name}' is already taken for this event"
                return render(request, "login/team_signup.html", data)
            
            # Generate unique team code
            team_code = generate_team_code()
            while Team.objects.filter(team_code=team_code).exists():
                team_code = generate_team_code()
            
            # Parse members list
            members = [m.strip() for m in members_str.split(",") if m.strip()]
            
            # Hash password
            hashed_password = make_password(password)
            
            # Create team
            team = Team.objects.create(
                event=event,
                team_name=team_name,
                team_code=team_code,
                password=hashed_password,
                leader_name=leader_name,
                leader_email=leader_email,
                members=members,
                balance=event.initial_capital,
                portfolio={},
                trade_history=[],
                total_trades=0,
                is_active=True,
                is_disqualified=False
            )
            
            # Store team code in session for display
            data["success"] = True
            data["team_code"] = team_code
            data["team_name"] = team_name
            
            return render(request, "login/team_signup.html", data)
            
        except Exception as e:
            data["error"] = f"Registration failed: {str(e)}"
            return render(request, "login/team_signup.html", data)
    
    return render(request, "login/team_signup.html", data)


def team_login(request):
    """Team login page"""
    data = {"error": None}
    
    if request.method == "POST":
        team_code = request.POST.get("team_code")
        password = request.POST.get("password")
        
        if not team_code or not password:
            data["error"] = "Team code and password are required"
            return render(request, "login/team_login.html", data)
        
        try:
            team = Team.objects.get(team_code=team_code.upper())
            
            # Check if team is active
            if not team.is_active:
                data["error"] = "This team is not active"
                return render(request, "login/team_login.html", data)
            
            if team.is_disqualified:
                data["error"] = "This team has been disqualified"
                return render(request, "login/team_login.html", data)
            
            # Verify password
            if check_password(password, team.password):
                # Store team info in session
                request.session['team_id'] = team.id
                request.session['team_code'] = team.team_code
                request.session['team_name'] = team.team_name
                request.session['is_team'] = True
                return redirect('team_dashboard')
            else:
                data["error"] = "Invalid team code or password"
                return render(request, "login/team_login.html", data)
                
        except Team.DoesNotExist:
            data["error"] = "Invalid team code or password"
            return render(request, "login/team_login.html", data)
    
    return render(request, "login/team_login.html", data)


def team_dashboard(request):
    """Team dashboard - isolated view showing only team's own data"""
    if not request.session.get('is_team'):
        return redirect('team_login')
    
    try:
        team_id = request.session.get('team_id')
        team = Team.objects.get(id=team_id)
        
        # Check if event is active
        if not team.event.is_active:
            data = {
                "error": "The event is not currently active",
                "team": team,
                "event_status": team.event.status
            }
            return render(request, "main/team_dashboard.html", data)
        
        # Prepare team data
        data = {
            "team": team,
            "team_code": team.team_code,
            "team_name": team.team_name,
            "balance": float(team.balance),
            "portfolio_value": team.portfolio_value,
            "profit_loss": team.profit_loss,
            "profit_loss_percent": team.profit_loss_percent,
            "portfolio": team.portfolio,
            "total_trades": team.total_trades,
            "recent_trades": team.trade_history[-10:] if team.trade_history else [],
            "event": team.event,
            "initial_capital": float(team.event.initial_capital),
            "title": f"Team {team.team_name} Dashboard"
        }
        
        return render(request, "main/team_dashboard.html", data)
        
    except Team.DoesNotExist:
        request.session.flush()
        return redirect('team_login')


def team_logout(request):
    """Logout team"""
    request.session.flush()
    return redirect('team_login')


def generate_team_code():
    """Generate a unique team code (e.g., TEAM-X7K2)"""
    chars = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(chars) for _ in range(4))
    return f"TEAM-{code}"


# ============ TEAM TRADING FUNCTIONS ============

def team_stocks(request):
    """Browse all available stocks for trading"""
    if not request.session.get('is_team'):
        return redirect('team_login')
    
    try:
        team_id = request.session.get('team_id')
        team = Team.objects.get(id=team_id)
        
        # Check if event is active
        if not team.event.is_active:
            from django.contrib import messages
            messages.warning(request, "Trading is currently paused. Event is not active.")
            return redirect('team_dashboard')
        
        # Get all active stocks
        from app1.models import Stock
        stocks = Stock.objects.filter(is_active=True).order_by('symbol')
        
        # Calculate additional info for each stock
        stock_data = []
        for stock in stocks:
            # Check if team owns this stock
            portfolio = team.portfolio if isinstance(team.portfolio, dict) else {}
            holding = portfolio.get(stock.symbol, {})
            owns = holding.get('quantity', 0) > 0
            
            stock_info = {
                'symbol': stock.symbol,
                'name': stock.name,
                'sector': stock.sector if hasattr(stock, 'sector') else 'N/A',
                'current_price': float(stock.current_price),
                'previous_close': float(stock.previous_close),
                'price_change': float(stock.price_change),
                'price_change_percent': float(stock.price_change_percent),
                'owns': owns,
                'quantity': holding.get('quantity', 0) if owns else 0,
                'avg_price': holding.get('avg_price', 0) if owns else 0,
            }
            stock_data.append(stock_info)
        
        data = {
            'team': team,
            'team_code': team.team_code,
            'team_name': team.team_name,
            'balance': float(team.balance),
            'stocks': stock_data,
            'stock_count': len(stock_data),
            'event': team.event,
            'title': 'Browse Stocks'
        }
        
        return render(request, "main/team_stocks.html", data)
        
    except Team.DoesNotExist:
        request.session.flush()
        return redirect('team_login')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f"Error loading stocks: {str(e)}")
        return redirect('team_dashboard')


def team_trade(request, symbol):
    """Buy or sell a specific stock"""
    if not request.session.get('is_team'):
        return redirect('team_login')
    
    try:
        team_id = request.session.get('team_id')
        team = Team.objects.get(id=team_id)
        
        # Check if event is active
        if not team.event.is_active:
            return redirect('team_dashboard')
        
        # Get the stock
        from app1.models import Stock
        stock = Stock.objects.get(symbol=symbol, is_active=True)
        
        # Get team's current holding
        holding = team.portfolio.get(symbol, {'quantity': 0, 'avg_price': 0})
        
        error = None
        success = None
        
        if request.method == "POST":
            action = request.POST.get("action")  # 'buy' or 'sell'
            quantity = int(request.POST.get("quantity", 0))
            
            if quantity <= 0:
                error = "Quantity must be greater than 0"
            elif action == "buy":
                # Calculate cost
                total_cost = float(stock.current_price) * quantity
                
                # Check if team has enough balance
                if total_cost > float(team.balance):
                    error = f"Insufficient balance. Need ${total_cost:,.2f}, have ${float(team.balance):,.2f}"
                else:
                    # Execute buy
                    current_quantity = holding.get('quantity', 0)
                    current_avg = holding.get('avg_price', 0)
                    
                    # Calculate new average price
                    total_shares = current_quantity + quantity
                    new_avg_price = ((current_quantity * current_avg) + (quantity * float(stock.current_price))) / total_shares
                    
                    # Update portfolio
                    team.portfolio[symbol] = {
                        'quantity': total_shares,
                        'avg_price': new_avg_price
                    }
                    
                    # Deduct balance
                    team.balance = float(team.balance) - total_cost
                    
                    # Record trade
                    from django.utils import timezone
                    trade_record = {
                        'time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'BUY',
                        'symbol': symbol,
                        'quantity': quantity,
                        'price': float(stock.current_price),
                        'total': total_cost
                    }
                    team.trade_history.append(trade_record)
                    team.total_trades += 1
                    team.last_trade_time = timezone.now()
                    
                    team.save()
                    
                    success = f"Successfully bought {quantity} shares of {symbol} for ${total_cost:,.2f}"
                    
            elif action == "sell":
                # Check if team owns enough shares
                if holding.get('quantity', 0) < quantity:
                    error = f"Insufficient shares. You own {holding.get('quantity', 0)} shares"
                else:
                    # Execute sell
                    total_revenue = float(stock.current_price) * quantity
                    remaining_shares = holding['quantity'] - quantity
                    
                    if remaining_shares == 0:
                        # Sold all shares, remove from portfolio
                        team.portfolio.pop(symbol, None)
                    else:
                        # Update quantity
                        team.portfolio[symbol]['quantity'] = remaining_shares
                    
                    # Add balance
                    team.balance = float(team.balance) + total_revenue
                    
                    # Record trade
                    from django.utils import timezone
                    trade_record = {
                        'time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'SELL',
                        'symbol': symbol,
                        'quantity': quantity,
                        'price': float(stock.current_price),
                        'total': total_revenue
                    }
                    team.trade_history.append(trade_record)
                    team.total_trades += 1
                    team.last_trade_time = timezone.now()
                    
                    team.save()
                    
                    success = f"Successfully sold {quantity} shares of {symbol} for ${total_revenue:,.2f}"
            
            # Refresh holding data after trade
            holding = team.portfolio.get(symbol, {'quantity': 0, 'avg_price': 0})
        
        # Calculate profit/loss if team owns the stock
        current_value = 0
        invested_value = 0
        profit_loss = 0
        profit_loss_percent = 0
        
        if holding.get('quantity', 0) > 0:
            current_value = float(stock.current_price) * holding['quantity']
            invested_value = holding['avg_price'] * holding['quantity']
            profit_loss = current_value - invested_value
            if invested_value > 0:
                profit_loss_percent = (profit_loss / invested_value) * 100
        
        data = {
            'team': team,
            'team_code': team.team_code,
            'team_name': team.team_name,
            'balance': float(team.balance),
            'stock': stock,
            'holding': holding,
            'current_value': current_value,
            'invested_value': invested_value,
            'profit_loss': profit_loss,
            'profit_loss_percent': profit_loss_percent,
            'error': error,
            'success': success,
            'title': f'Trade {symbol}'
        }
        
        return render(request, "main/team_trade.html", data)
        
    except Stock.DoesNotExist:
        return redirect('team_stocks')
    except Team.DoesNotExist:
        request.session.flush()
        return redirect('team_login')


def team_portfolio(request):
    """View team's complete portfolio with profit/loss"""
    if not request.session.get('is_team'):
        return redirect('team_login')
    
    try:
        team_id = request.session.get('team_id')
        team = Team.objects.get(id=team_id)
        
        # Get current prices for all holdings
        from app1.models import Stock
        portfolio_data = []
        total_invested = 0
        total_current_value = 0
        
        # Ensure portfolio is a dict
        portfolio = team.portfolio if isinstance(team.portfolio, dict) else {}
        
        for symbol, holding in portfolio.items():
            try:
                stock = Stock.objects.get(symbol=symbol, is_active=True)
                quantity = holding.get('quantity', 0)
                avg_price = holding.get('avg_price', 0)
                
                invested = avg_price * quantity
                current_value = float(stock.current_price) * quantity
                profit_loss = current_value - invested
                profit_loss_percent = (profit_loss / invested * 100) if invested > 0 else 0
                
                portfolio_data.append({
                    'symbol': symbol,
                    'name': stock.name,
                    'sector': stock.sector if hasattr(stock, 'sector') else 'N/A',
                    'quantity': quantity,
                    'avg_price': avg_price,
                    'current_price': float(stock.current_price),
                    'invested': invested,
                    'current_value': current_value,
                    'profit_loss': profit_loss,
                    'profit_loss_percent': profit_loss_percent
                })
                
                total_invested += invested
                total_current_value += current_value
                
            except Stock.DoesNotExist:
                # Stock might have been deactivated
                continue
        
        total_profit_loss = total_current_value - total_invested
        total_profit_loss_percent = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        data = {
            'team': team,
            'team_code': team.team_code,
            'team_name': team.team_name,
            'balance': float(team.balance),
            'portfolio': portfolio_data,
            'holdings_count': len(portfolio_data),
            'total_invested': total_invested,
            'total_current_value': total_current_value,
            'total_profit_loss': total_profit_loss,
            'total_profit_loss_percent': total_profit_loss_percent,
            'portfolio_value': team.portfolio_value,
            'event': team.event,
            'title': 'Portfolio'
        }
        
        return render(request, "main/team_portfolio.html", data)
        
    except Team.DoesNotExist:
        request.session.flush()
        return redirect('team_login')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f"Error loading portfolio: {str(e)}")
        return redirect('team_dashboard')


def team_stock_prices_api(request):
    """API endpoint to fetch current stock prices for AJAX updates"""
    from django.http import JsonResponse
    from app1.models import Stock
    
    if not request.session.get('is_team'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        stocks = Stock.objects.filter(is_active=True).values(
            'symbol', 'current_price', 'previous_close'
        )
        
        stock_data = {}
        for stock in stocks:
            change = float(stock['current_price']) - float(stock['previous_close'])
            change_percent = (change / float(stock['previous_close']) * 100) if stock['previous_close'] > 0 else 0
            
            stock_data[stock['symbol']] = {
                'price': float(stock['current_price']),
                'change': change,
                'change_percent': change_percent
            }
        
        return JsonResponse({'success': True, 'stocks': stock_data})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)