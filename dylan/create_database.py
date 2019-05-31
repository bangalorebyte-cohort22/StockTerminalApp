# Importing modules
import sqlite3

# Connecting to the database
con = sqlite3.connect('stock_trading.db')

# Creating users and orders tables
con.execute(
    '''
    CREATE TABLE IF NOT EXISTS users(
    username UNIQUE NOT NULL PRIMARY KEY,
    password NOT NULL,
    bank_account NOT NULL DEFAULT 1000000.0,
    admin BOOLEAN NOT NULL DEFAULT 0
    );
    '''
)

con.execute(
    '''
    CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_type NOT NULL,
    order_made_by NOT NULL,
    order_timestamp DATETIME NOT NULL,
    stock_ticker NOT NULL,
    strike_price NOT NULL
    );
    '''
)

try:
    con.execute(
        '''
        INSERT INTO users (username,password,admin)
        VALUES ("admin","admin2",1)
        '''
    )
    con.execute(
        '''
        INSERT INTO users (username,password,admin)
        VALUES ("dillkillbill","1234",0)
        '''
    )
except:
    print("Didn't add admin and test user")

con.commit()
con.close()