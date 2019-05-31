import sqlite3
from .app import run_app


if __name__ == '__main__':
    con = sqlite3.connect("stock_trading.db")
    run = True
    user = None
    run_app(run, user)