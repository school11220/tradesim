#import matplotlib.pyplot as plt
#import numpy as np

import requests
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from .models import users
from .mdate import getdate,today

from json import dumps

def search(request,query):
    query=query.replace(" ","%20")
    url="https://query2.finance.yahoo.com/v1/finance/search?q="+query
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}

    response = requests.get(url,headers=headers)
    data = response.json()

    #print(type(data))
    store={"stocks":[]}

    # print(data.keys())

    # print(data["quotes"])

    for i in data["quotes"]:
        store["stocks"].append(i)

    return JsonResponse(store)

# print(search("apple"))

def watchlist(request, query):

    response_step1 = requests.get("https://fc.yahoo.com")
    cookie = response_step1.headers.get('Set-Cookie')

    url_step2 = "https://query2.finance.yahoo.com/v1/test/getcrumb"
    headers_step2 = headers = {
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Cookie": cookie
        }  # Include obtained cookie in request headers

    response_step2 = requests.get(url_step2, headers=headers_step2)
    crumb = response_step2.text

    # url = f"https://query2.finance.yahoo.com/v7/finance/quote?symbols=TSLA&crumb={crumb}"

    # Construct the URL with the crumb value
    url = "https://query1.finance.yahoo.com/v7/finance/quote?&symbols=" + query + "&fields=currency,fromCurrency,toCurrency,exchangeTimezoneName,exchangeTimezoneShortName,gmtOffSetMilliseconds,regularMarketChange,regularMarketChangePercent,regularMarketPrice,regularMarketTime,preMarketTime,postMarketTime,extendedMarketTime&crumb="+crumb+"&formatted=false&region=US&lang=en-US"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Cookie": cookie
    }

    response_step3 = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",'Cookie': cookie})

    cache = {'cookie': cookie, 'crumb': crumb}

    data=response_step3.json()
    store={"stocks":[]}
    
    for i in range(0,len(data["quoteResponse"]["result"])):
        symbol=data["quoteResponse"]["result"][i]["symbol"]
        link="/removewatchlist/"+symbol
        store["stocks"].append([symbol,round(data["quoteResponse"]["result"][i]["regularMarketPrice"],2),round(data["quoteResponse"]["result"][i]["regularMarketChangePercent"],5),link,data["quoteResponse"]["result"][i]["marketState"]])
        # print(store)
    
    # print(store)
    return JsonResponse(store)

    

# Example usage:
# watchlist("e", "aapl,goog,meta,msft,sony")

def fetchdetails(request, query):
    url="https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/"+query+"?merge=false&padTimeSeries=true&period1=1698240600&period2=1714055399&type=quarterlyMarketCap%2CtrailingMarketCap%2CquarterlyEnterpriseValue%2CtrailingEnterpriseValue%2CquarterlyPeRatio%2CtrailingPeRatio%2CquarterlyForwardPeRatio%2CtrailingForwardPeRatio%2CquarterlyPegRatio%2CtrailingPegRatio%2CquarterlyPsRatio%2CtrailingPsRatio%2CquarterlyPbRatio%2CtrailingPbRatio%2CquarterlyEnterprisesValueRevenueRatio%2CtrailingEnterprisesValueRevenueRatio%2CquarterlyEnterprisesValueEBITDARatio%2CtrailingEnterprisesValueEBITDARatio&lang=en-US&region=US"
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    response = requests.get(url,headers=headers)
    data = response.json()

    #print(data["chart"]["result"][0]["meta"])

    store={}

    for i in (data["timeseries"]["result"]):
        typ=i["meta"]["type"][0]
        store[typ]=i[typ][0]["reportedValue"]["fmt"]
    
    return JsonResponse(store)

def graphdata(request,query,start,end):
    # print("--------------------------------")
    # print(query,start,end)
    # print("--------------------------------")
    url="https://query2.finance.yahoo.com/v8/finance/chart/"+query+"?period1="+str(start)+"&period2="+str(end)+"&interval=5m&includePrePost=true&events=div%7Csplit%7Cearn&&lang=en-US&region=US"
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    print(url)
    response = requests.get(url,headers=headers)
    data = response.json()

    store={"date":[],"close":[]}

    for i in range(0,len(data["chart"]["result"][0]["timestamp"])):
        store["date"].append(getdate(data["chart"]["result"][0]["timestamp"][i]))
        try:
            store["close"].append(round(data["chart"]["result"][0]["indicators"]["quote"][0]["close"][i],2))
        except:
            continue
    
    store["currency"]=data["chart"]["result"][0]["meta"]["currency"]
    return JsonResponse(store)

def portfolio(request):
    user=request.user
    stocks=user.stockbuy
    name=list(stocks.keys())
    print(name[0])
    print(name)
    stocksname=""
    for i in range(len(name)-1,-1,-1):
        print(i)
        stocksname=name[i]+","+stocksname
    print(stocksname)
    store=[]
    i=0
    url="http://127.0.0.1:8000/api/watchlist/"+stocksname
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    response = requests.get(url,headers=headers)
    data = response.json()
    for i in range(0,len(name)):
        store.append({"symbol":[name[i]],"quantity":[stocks[name[i]]["quantity"]],"boughtat":[stocks[name[i]]["boughtat"]],"averageprice":[stocks[name[i]]["averageprice"]],"currentprice":data["stocks"][i][1],"percentchange":data["stocks"][i][2]})

    print(data["stocks"])
    print(store)
    
    return JsonResponse(store,safe=False)

def portfoliochart(request):
    user=request.user
    stocks=user.stockbuy
    price=[]
    name=list(stocks.keys())
    for i in name:
        price.append(user.stockbuy[i]["boughtat"]*user.stockbuy[i]["quantity"])

    store={"name":name,"price":price}
    return JsonResponse(store)

def income(request):
    user=request.user
    stocks=user.stockbuy
    price=[]
    name=list(stocks.keys())
    stocksname=""
    for i in range(len(name)-1,-1,-1):
        # print(i)
        stocksname=name[i]+","+stocksname
    print(stocksname)
    print(name)
    url="http://127.0.0.1:8000/api/watchlist/"+stocksname
    headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    response = requests.get(url,headers=headers)
    data = response.json()
    storepl=0
    print(data["stocks"][0])
    for i in range(0,len(name)):
        investedamount=user.stockbuy[name[i]]["averageprice"]*user.stockbuy[name[i]]["quantity"]
        currentamount=data["stocks"][i][1]*user.stockbuy[name[i]]["quantity"]
        # print("investedamount",investedamount)
        # print("Current Amount",currentamount)
        pl=currentamount-investedamount
        storepl=storepl+round(pl,2)
    return HttpResponse(round(storepl,2))

def holdings(request,query):
    # print("---------------Holdings-----------------")
    # print(query)
    # print("---------------Holdings-----------------")
    logedInUser=request.user
    stocks=logedInUser.stockbuy.keys()
    print(logedInUser)
    print(stocks)
    if(query in list(stocks)):
        # url="http://127.0.0.1:8000/api/watchlist/"+query
        # headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
        # response = requests.get(url,headers=headers)
        # data = response.json()
        return HttpResponse(logedInUser.stockbuy[query]["quantity"])
    else:
        return HttpResponse(0)
    
def addtoWatchlist(request,query):
    logedInUser=request.user
    
    # Ensure watchlist is properly structured
    if not isinstance(logedInUser.watchlist, dict):
        logedInUser.watchlist = {"symbol": []}
    
    if "symbol" not in logedInUser.watchlist:
        logedInUser.watchlist["symbol"] = []
    
    watchlist=logedInUser.watchlist
    print(watchlist)
    print(query)
    
    if(query in watchlist["symbol"]):
        print("Already Exists")
        return JsonResponse({"response":"Already Exists"})
    else:
        watchlist["symbol"].append(query)
        logedInUser.save()
        return JsonResponse({"response":"Added "+query})


def trigger_price_update(request):
    """
    API endpoint to trigger stock price updates (simulated)
    Can be called by cron jobs or manually to update all stock prices
    """
    from app1.models import Stock
    import random
    
    try:
        # Get volatility from query param, default 2%
        volatility = float(request.GET.get('volatility', 0.02))
        
        # Get all active stocks
        stocks = Stock.objects.filter(is_active=True)
        
        if not stocks.exists():
            return JsonResponse({
                'success': False,
                'error': 'No active stocks found'
            })
        
        updated_count = 0
        updates = []
        
        # Update each stock
        for stock in stocks:
            old_price = float(stock.current_price)
            new_price = float(stock.update_price_random(volatility))
            change = new_price - old_price
            change_percent = (change / old_price * 100) if old_price > 0 else 0
            
            updates.append({
                'symbol': stock.symbol,
                'old_price': round(old_price, 2),
                'new_price': round(float(new_price), 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2)
            })
            
            updated_count += 1
        
        return JsonResponse({
            'success': True,
            'mode': 'simulated',
            'updated_count': updated_count,
            'volatility': volatility,
            'updates': updates
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def update_prices_real(request):
    """
    API endpoint to update stock prices from REAL market data via Yahoo Finance
    Optimized with 3-tier fallback and batch processing
    """
    from app1.models import Stock
    from datetime import datetime
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        import yfinance as yf
    except ImportError:
        return JsonResponse({
            'success': False,
            'error': 'yfinance not installed. Run: pip install yfinance'
        }, status=500)
    
    try:
        stocks = Stock.objects.filter(is_active=True)
        
        if not stocks.exists():
            return JsonResponse({
                'success': False,
                'error': 'No active stocks found'
            })
        
        updated_count = 0
        failed = []
        updates = []
        errors = []
        
        logger.info(f"Starting real price update for {stocks.count()} stocks")
        
        # Try batch download first (much faster!)
        symbols = [stock.symbol for stock in stocks]
        batch_data = {}
        
        try:
            # Download all tickers at once - MUCH faster than individual calls
            logger.info(f"Attempting batch download for {len(symbols)} symbols")
            tickers = yf.Tickers(' '.join(symbols))
            
            for stock in stocks:
                try:
                    ticker = tickers.tickers[stock.symbol]
                    
                    # Try fast_info first
                    try:
                        batch_data[stock.symbol] = float(ticker.fast_info.last_price)
                    except:
                        # Fallback to history
                        try:
                            hist = ticker.history(period="1d")
                            if not hist.empty:
                                batch_data[stock.symbol] = float(hist['Close'].iloc[-1])
                        except:
                            pass
                except Exception as e:
                    logger.warning(f"Batch fetch failed for {stock.symbol}: {str(e)[:50]}")
        except Exception as e:
            logger.warning(f"Batch download failed, falling back to individual: {str(e)[:100]}")
        
        # Process all stocks
        for stock in stocks:
            try:
                current_price = batch_data.get(stock.symbol)
                
                # If batch failed, try individual fetch
                if not current_price:
                    ticker = yf.Ticker(stock.symbol)
                    
                    # Method 1: fast_info
                    try:
                        current_price = float(ticker.fast_info.last_price)
                    except Exception:
                        # Method 2: history
                        try:
                            hist = ticker.history(period="1d")
                            if not hist.empty:
                                current_price = float(hist['Close'].iloc[-1])
                        except Exception:
                            # Method 3: info dict
                            try:
                                info = ticker.info
                                for field in ['currentPrice', 'regularMarketPrice', 'previousClose']:
                                    if field in info and info[field]:
                                        current_price = float(info[field])
                                        break
                            except Exception:
                                pass
                
                if current_price and current_price > 0:
                    old_price = float(stock.current_price)
                    stock.previous_close = old_price
                    stock.current_price = round(current_price, 2)
                    stock.last_updated = datetime.now()
                    stock.save()
                    
                    change = current_price - old_price
                    change_pct = (change / old_price) * 100 if old_price > 0 else 0
                    
                    updates.append({
                        'symbol': stock.symbol,
                        'old_price': round(old_price, 2),
                        'new_price': round(current_price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_pct, 2)
                    })
                    updated_count += 1
                else:
                    failed.append(stock.symbol)
                    logger.warning(f"No valid price data for {stock.symbol}")
            except Exception as e:
                failed.append(stock.symbol)
                error_msg = f"{stock.symbol}: {str(e)[:100]}"
                errors.append(error_msg)
                logger.error(f"Error fetching {stock.symbol}: {str(e)}")
        
        success_rate = (updated_count / len(stocks) * 100) if stocks else 0
        logger.info(f"Price update complete: {updated_count}/{len(stocks)} stocks ({success_rate:.1f}%)")
        
        return JsonResponse({
            'success': True,
            'mode': 'real_market',
            'updated_count': updated_count,
            'total_stocks': len(stocks),
            'success_rate': round(success_rate, 1),
            'failed_count': len(failed),
            'failed': failed[:20] if len(failed) > 20 else failed,  # Limit to first 20
            'errors': errors[:5] if len(errors) > 5 else errors,  # Limit to first 5 errors
            'timestamp': datetime.now().isoformat(),
            'updates': updates[:10] if len(updates) > 10 else updates  # Sample of updates
        })
        
    except Exception as e:
        logger.error(f"Fatal error in update_prices_real: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def update_prices_auto(request):
    """
    API endpoint that checks simulator setting and uses appropriate update method
    """
    from app1.models import SimulatorSettings
    
    try:
        setting = SimulatorSettings.objects.get(setting_name='use_real_prices')
        use_real = setting.setting_value.lower() == 'true'
    except SimulatorSettings.DoesNotExist:
        use_real = False
    
    if use_real:
        return update_prices_real(request)
    else:
        return trigger_price_update(request)


def toggle_price_mode(request):
    """
    API endpoint to toggle between real and simulated price updates
    """
    from app1.models import SimulatorSettings
    from django.views.decorators.http import require_http_methods
    
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Admin access required'
        }, status=403)
    
    try:
        setting, created = SimulatorSettings.objects.get_or_create(
            setting_name='use_real_prices',
            defaults={
                'setting_value': 'false',
                'description': 'Use real stock market prices from Yahoo Finance'
            }
        )
        
        # Toggle the value
        current = setting.setting_value.lower() == 'true'
        new_value = not current
        setting.setting_value = str(new_value).lower()
        setting.save()
        
        return JsonResponse({
            'success': True,
            'use_real_prices': new_value,
            'message': f'Switched to {"REAL market data" if new_value else "SIMULATED prices"}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def adjust_sector(request):
    """
    API endpoint to adjust prices for an entire sector by custom percentage
    """
    from app1.models import Stock
    import json
    
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Admin access required'
        }, status=403)
    
    try:
        data = json.loads(request.body)
        sector = data.get('sector')
        percentage = float(data.get('percentage', 0))
        
        if not sector:
            return JsonResponse({
                'success': False,
                'error': 'Sector is required'
            }, status=400)
        
        stocks = Stock.objects.filter(sector=sector, is_active=True)
        
        if not stocks.exists():
            return JsonResponse({
                'success': False,
                'error': f'No active stocks found in {sector} sector'
            }, status=404)
        
        multiplier = 1 + (percentage / 100)
        
        for stock in stocks:
            stock.previous_close = float(stock.current_price)
            stock.current_price = round(float(stock.current_price) * multiplier, 2)
            stock.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Adjusted {stocks.count()} stocks in {sector} sector by {percentage:+.2f}%',
            'sector': sector,
            'percentage': percentage,
            'stocks_affected': stocks.count()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_market_events(request):
    """
    API endpoint to get recent market events for teams
    Returns active events from the last 24 hours
    """
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        # Try to import MarketEvent (may not exist until migrations run)
        try:
            from app1.models import MarketEvent
        except ImportError:
            return JsonResponse({
                'success': True,
                'events': [],
                'count': 0,
                'message': 'MarketEvent feature not yet available. Run migrations.'
            })
        
        # Get events from last 24 hours
        cutoff_time = timezone.now() - timedelta(hours=24)
        
        events = MarketEvent.objects.filter(
            is_active=True,
            is_triggered=True,
            triggered_at__gte=cutoff_time
        ).order_by('-triggered_at')[:10]  # Latest 10 events
        
        events_data = []
        for event in events:
            events_data.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'event_type': event.get_event_type_display(),
                'affected_sector': event.affected_sector,
                'percentage': event.get_percentage_change(),
                'is_positive': event.is_positive,
                'stocks_affected': event.stocks_affected,
                'triggered_at': event.triggered_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'events': events_data,
            'count': len(events_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'events': []
        }, status=500)