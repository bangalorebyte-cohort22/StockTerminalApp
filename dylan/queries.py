import sqlite3
import pandas as pd

def get_all_users():
    con = sqlite3.connect("stock_trading.db")
    data = pd.read_sql("SELECT * FROM users", con)
    con.close()
    return data

def get_all_buys():
    con = sqlite3.connect("stock_trading.db")
    data = pd.read_sql("SELECT * FROM orders WHERE order_type = 'buy'", con)
    con.close()
    return data

def get_all_sells():
    con = sqlite3.connect("stock_trading.db")
    data = pd.read_sql("SELECT * FROM orders WHERE order_type = 'sell", con)
    con.close()
    return data

def get_user_info(username):
    con = sqlite3.connect("stock_trading.db")
    data = pd.read_sql(f"SELECT * FROM users WHERE username = {username}", con)
    con.close()
    return data

def add_user(username,password):
    con = sqlite3.connect("stock_trading.db")
    con.execute(
        '''
        INSERT INTO users (username,password)
        VALUES (?,?)
        ''', (username,password)
    )
    con.commit()
    con.close()