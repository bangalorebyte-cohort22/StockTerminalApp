import sqlite3
import pandas as pd

def connect():
    return sqlite3.connect("stock_trading.db")

def get_all_users():
    con = connect()
    data = pd.read_sql("SELECT * FROM users", con)
    con.close()
    return data

def get_all_buys():
    con = connect()
    data = pd.read_sql("SELECT * FROM orders WHERE order_type = 'buy'", con)
    con.close()
    return data

def get_all_sells():
    con = connect()
    data = pd.read_sql("SELECT * FROM orders WHERE order_type = 'sell", con)
    con.close()
    return data

def get_user_info(username):
    con = connect()
    data = pd.read_sql(f"SELECT * FROM users WHERE username = {username}", con)
    con.close()
    return data

def add_user(username,password):
    con = connect()
    con.execute(
        '''
        INSERT INTO users (username,password)
        VALUES (?,?)
        ''', (username,password)
    )
    con.commit()
    con.close()

def get_bank_balance(username):
    con = connect()
    current_account = pd.read_sql("SELECT bank_account FROM users WHERE username = '{0}'".format(username),con)
    con.close()
    return current_account.iloc[0,0]


def check_funds(username,stock_price,number_of_shares):
    bank_account = get_bank_balance(username)
    if stock_price*number_of_shares > bank_account:
        return False
    else:
        return True

def buy_stock(username,ticker,price,number_of_shares,datetime):
    con = connect()
    con.execute(
        '''
        INSERT INTO orders (order_type,order_made_by,order_timestamp,stock_ticker,strike_price,number_of_shares)
        VALUES (?,?,?,?,?,?)
        ''', ("buy",username,datetime,ticker,price,number_of_shares)
    )
    con.commit()
    con.close()

def deduct_account(username,price,number_of_shares):
    current_account = get_bank_balance(username)   
    new_balance = current_account - (price*number_of_shares)
    con = connect()
    con.execute(
        '''
        UPDATE users
        SET bank_account = ?
        WHERE username = ?
        ''', (new_balance,username)
    )
    con.commit()
    con.close()
    return new_balance


def check_stocks(username,stock_ticker,number_of_shares):
    net_stocks = stock_portfolio(username)
    print(stock_ticker)
    print(net_stocks[net_stocks['stock_ticker']==stock_ticker])
    num_stocks_ticker = net_stocks[net_stocks['stock_ticker'] == stock_ticker]['number_of_shares_owned'].values[0]
    if number_of_shares > num_stocks_ticker:
        return False
    else:
        return True


def sell_stock(username,ticker,price,number_of_shares,datetime):
    con = connect()
    con.execute(
        '''
        INSERT INTO orders (order_type,order_made_by,order_timestamp,stock_ticker,strike_price,number_of_shares)
        VALUES (?,?,?,?,?,?)
        ''', ("sell",username,datetime,ticker,price,-number_of_shares)
    )
    con.commit()
    con.close()

def credit_account(username,price,number_of_shares):
    current_account = get_bank_balance(username)
    new_balance = current_account + (price*number_of_shares)
    con = connect()
    con.execute(
        '''
        UPDATE users
        SET bank_account = ?
        WHERE username = ?
        ''', (new_balance,username)
    )
    con.commit()
    con.close()
    return new_balance


def stock_portfolio(username):
    query = f'''
SELECT stock_ticker, SUM(number_of_shares) AS number_of_shares_owned
FROM orders 
WHERE order_made_by = "{username}"
GROUP BY stock_ticker
'''
    con = connect()
    portfolio = pd.read_sql(query,con)
    con.close()
    return portfolio

def get_all_portfolios():
    query = '''
SELECT order_made_by AS username, stock_ticker, SUM(number_of_shares) AS number_of_shares_owned
FROM orders 
GROUP BY stock_ticker, order_made_by
ORDER BY order_made_by ASC
'''
    con = connect()
    all_p = pd.read_sql(query,con)
    con.close()
    return all_p

def get_all_banks():
    query = '''
    SELECT username, bank_account FROM users
    '''
    con = connect()
    data = pd.read_sql(query,con)
    con.close()
    return data

def leaderboard(markit):
    all_p = get_all_portfolios()
    all_p['current_price'] = all_p.apply(lambda x: markit.get_price(x['stock_ticker']), axis = 1)
    all_p['worth'] = all_p['number_of_shares_owned']*all_p['current_price']
    all_p = all_p[['username','worth']].groupby('username').sum().reset_index()
    banks = get_all_banks()
    final = pd.merge(all_p,banks,how = 'inner',on = ['username','username'])
    final['net_worth'] = final['worth'] + final['bank_account']
    return final.sort_values(['net_worth','username'],ascending = [1,1])[['username','net_worth']]

