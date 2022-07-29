from flask import Blueprint, request, jsonify, make_response,abort
from app import db
from app.models.price import Price
from app.models.stock import Stock
import os
import requests
from dotenv import load_dotenv
load_dotenv()
API_key = os.environ.get("API_KEY")

#--------request "GET" from external stock API--------------
def get_stock_price(ticker):  # for one datapoint == one price
    params = {"function":"GLOBAL_QUOTE", "symbol":ticker,'apikey': API_key}
    url = 'https://www.alphavantage.co/query'
    data = requests.get(url,params)
    return data.json()

def time_series_monthly_adjusted(ticker):
    params = {"function":"TIME_SERIES_MONTHLY_ADJUSTED", "symbol":ticker,'apikey': API_key}
    url = 'https://www.alphavantage.co/query'
    data = requests.get(url,params)
    return data.json()
#----------------------STOCK------------------
stocks_bp = Blueprint("stocks_bp", __name__, url_prefix="/stocks")

#post a stock-----------------------------
@stocks_bp.route("", methods = ["POST"])
def post_stock():
    
    post_dict = request.get_json()

    if 'ticker' not in post_dict or 'shares' not in post_dict:
        abort (make_response({"details":"Invalid data: Need stock ticker and number of shares"},400))
    
    shares = post_dict['shares']
    ticker = post_dict['ticker']

    stock = Stock.query.filter_by(ticker=ticker).first()  #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    if stock:
        abort (make_response({"detail": "Invalid data: This stock already in the database. You only can modify or delete"},400))

    stock = Stock(ticker=ticker, shares=shares)
    db.session.add(stock)
    db.session.commit()
    
    data_dict = get_stock_price(ticker)
    closed_price = data_dict['Global Quote']['05. price'] # not save to database
    trade_date = data_dict['Global Quote']['07. latest trading day'] # not save to database
    
    data = time_series_monthly_adjusted(ticker)
    monthly_data = data['Monthly Adjusted Time Series']
    for date in monthly_data:
        print(date)
        if date <= "2022-06-30" and date > "2021-06-30":
            monthly_price = monthly_data[date]['5. adjusted close']
            price = Price(date=date,closed_price=monthly_price,stock=stock) 
            db.session.add(price)
            db.session.commit()

    stock_dict = {}
    stock_dict['id'] = stock.id
    stock_dict['ticker'] = stock.ticker
    stock_dict['shares'] = stock.shares
    stock_dict['price'] = closed_price  # because not save to database
    stock_dict['trade_date']= trade_date # because not save to database
    response_dict = {"stock": stock_dict}
    return jsonify(response_dict), 201

# get all prices for one stock by stock_id--------------------
@stocks_bp.route("/<stock_id>/prices",methods = ['GET'])
def get_prices_for_one_stock(stock_id):
    
    stock = Stock.query.get(stock_id)
    if (stock == None):
        abort (make_response({"message":f"stock {stock_id} not found"},404))
    
    prices_db = stock.prices # list of all price instances associated with this stock
    print (prices_db)

    for i in range(len(prices_db)-1):  # sorted price instances by oldest date first and later date last
        oldest_date = prices_db[i].date
        oldest_idx = i
        for j in range(i+1, len(prices_db)):
            if prices_db[j].date < oldest_date:
                oldest_date = prices_db[j].date
                oldest_idx = j
        # exchange instances with corresponding dates, so the instance with the oldest date is the first date in the list
        price_instance_with_oldest_date = prices_db[oldest_idx]
        price_instance_with_current_date_iteration = prices_db[i]
        prices_db[oldest_idx] = price_instance_with_current_date_iteration
        prices_db[i] = price_instance_with_oldest_date
    
    for instance in prices_db:
        print(instance.date) 

    dates = []
    prices = []
    for instance in prices_db:
        dates.append(instance.date)
        prices.append(instance.closed_price)
    
    percent_gains_list = [0]
    for i in range(len(prices)-1):
        percent_gain = round(100 * ((prices[i+1] - prices[i])/prices[i]))
        percent_gains_list.append(percent_gain)
    
    response = {}
    for i in range(len(prices)):
        date_str = f'{dates[i]}'
        new_entry = {'price':prices[i], 'percentage_gain':f'{percent_gains_list[i]}%'}
        response[date_str] = new_entry
    return jsonify(response),201

# update stock by id (PUT method)--------------------   
@stocks_bp.route("/<id>", methods =["PUT"]) 
def update_stock_by_id(id):

    stock = Stock.query.get(id)
    if (stock == None):
        abort(make_response({"message":f"stock {id} not found"}, 404))

    update_dict = request.get_json()
    if 'ticker' not in update_dict or 'shares' not in update_dict:
        return make_response({"details":"Invalid data"},400)
    
    ticker = update_dict['ticker']
    shares = update_dict['shares']

    if ticker != stock.ticker: 
        abort (make_response({"detail": "Invalid data: This stock ticker is not in the database.  Hence, you need to post a stock first"},400))

    stock.shares = shares
    db.session.commit()

    data_dict = get_stock_price(ticker)
    closed_price = data_dict['Global Quote']['05. price']
    trade_date = data_dict['Global Quote']['07. latest trading day']
    
    stock_dict = {}
    stock_dict['id'] = stock.id
    stock_dict['ticker'] = stock.ticker
    stock_dict['shares'] = stock.shares
    stock_dict['price'] = closed_price
    stock_dict['trade_date']= trade_date
    return_dict = {"stock": stock_dict}
    return jsonify(return_dict), 201

# remove stock by id---------------
@stocks_bp.route("/<id>",methods=['DELETE'])
def remove_stock_by_id(id):
    stock = Stock.query.get(id)
    if (stock==None):
        abort(make_response({"message":f"stock {id} not found"},404))

    update_dict = request.get_json()
    if 'ticker' not in update_dict:
        return make_response({"details":"Invalid data"},400)
    
    ticker = update_dict['ticker']
    
    if ticker != stock.ticker: 
        abort (make_response({"detail": "Invalid data: This ticker does not correspond to the stock_id.  Please check your ticker and stock_id"},400))

    for price in stock.prices:
        db.session.delete(price)
    db.session.delete(stock)
    db.session.commit()
    
    return make_response({"details":f"stock with {id} successfully deleted"},200)

'''
# get all prices for one stock by stock_id--------------------
@stocks_bp.route("/portfolio",methods = ['GET'])
def get_prices_for_one_stock(stock_id):

'''

'''







'''
#----------PRICE------------------
prices_bp = Blueprint("prices_bp", __name__, url_prefix="/prices")
@stocks_bp.route("/prices", methods=["POST"])
def post_price():
    pass
# #get historical monthly prices associated with stock
# @stocks_bp.route("/<stock_id>/prices", methods=["GET"])
# def get_historical_prices(stock_id):
#     stock = Stock.query.get(stock_id)
#     if stock==None:
#         abort(make_response({"message":f"stock {stock_id} not found"},400))
    
#     prices = stock.prices
#     price_list = []
#     for price in prices:
#         price_dict = {
#         'id': price.id,
#         'date' : price.date,
#         'closed_price' : price.closed_price,
#         }
#         price_list.append(price_dict)
    
#     response_dict = {
#         'id': stock.id,
#         'ticker': stock.ticker,
#         'prices': price_list
#     }
#     return jsonify(response_dict),200

