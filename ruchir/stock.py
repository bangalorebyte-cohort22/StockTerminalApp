import sqlite3
import time
import os
import json
import pyfiglet
import pandas as pd
from urllib.request import urlopen
from create_db import *
import requests
from datetime import datetime
import tabulatehelper as th
import sys

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)

# con = sqlite3.connect("data.db")


def login():
    while True:
        current_user = ""
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        with sqlite3.connect('data.db') as db:
            cursor = db.cursor()
        find_user = ("SELECT * from users WHERE username = ? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        results = cursor.fetchall()

        if results:
            print("Welcome, " + username + "!\n")
            login.current_user = [username]
            loggedin_state = True
            if loggedin_state:
                return loggedin_menu()

        else:
            print(
                "Username and/or password not found. Taking you back to the main menu."
            )
            time.sleep(1)
            return main_menu()


def register():
    found = 0
    while found == 0:
        username = input("Enter a username: ")
        with sqlite3.connect("data.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM users WHERE username = ?")
        cursor.execute(findUser, [(username)])

        if cursor.fetchall():
            print("Username already taken. Please try again.")
        else:
            found = 1
        password = input("Please enter your password: ")
        password_re = input("Please re-enter your password: ")
        while password != password_re:
            print("Your password did not match. Please try again.")
            password = input("Please enter your password: ")
            password_re = input("Please re-enter your password: ")
        insertData = '''INSERT INTO users(username, password)
            VALUES(?,?)'''

        cursor.execute(insertData, [username, password])
        db.commit()


def heading():
    heading = pyfiglet.figlet_format("Welcome Stock Trader!", font="starwars")
    print(heading + '\n')
    sub_heading = pyfiglet.figlet_format("Select option:", font="bubble")
    print(sub_heading)


# //TODO: If users logs out as remove all elements in the current_user list.


def main_menu():
    while True:
        try:

            print('''
                 [1] -- > Login
                 [2] -- > Register
                 [3] -- > Search by Company Name or Symbol (w/o Logging-in)
                 [4] -- > Quit''')

            answer = int(input("[Enter]: "))

            if answer == 1:
                login()
            elif answer == 2:
                register()
            elif answer == 3:
                company_search()
            elif answer == 4:
                print("Quitting the program!")
                time.sleep(2)
                sys.exit()
            elif answer == 99:
                leaderboard()

            else:
                print("Command not recognized. ")

        except ValueError:
            print("Please enter a number. ")


def loggedin_menu():
    os.system("clear")
    loggedin_heading = pyfiglet.figlet_format("Welcome", font="starwars")
    print(loggedin_heading)
    loggedin_subheading = pyfiglet.figlet_format(str(login.current_user[0]),
                                                 font="bubble")
    print(loggedin_subheading)

    while True:
        try:

            print('''
                  [1] --- >> Search by Company Name or Symbol
                  [2] --- >> Get Latest Stock Quote
                  [3] --- >> View Your Portfolio
                  [4] --- >> Buy Stocks
                  [5] --- >> Sell Stocks
                  [6] --- >> Logout as: ''' + str(login.current_user[0]))

            choice = int(input("[Enter]: "))

            #maps the options to their respective function
            menu_funcs_loggedin = {
                1: company_search,
                2: get_quote,
                3: view_portfolio,
                4: buy_stock,
                5: sell_stock,
                6: logout
            }
            if choice in menu_funcs_loggedin:
                menu_funcs_loggedin[choice]()  #calls the function

            else:
                print("Command not recognized. ")

        except ValueError:
            print("Please enter a number. ")


def company_search():
    search = input("Enter company name or symbol to search: ")
    url = 'http://dev.markitondemand.com/Api/v2/Lookup/json?input=' + search
    data = pd.read_json(url)
    if data.empty:
        print('No results found')
    else:
        print("\nCompany Search Results:\n\n"+th.md_table(data, formats={-1: 'c'}))



def get_quote():
    pd.set_option('display.width', 200)
    search_quote = input("Enter stock symbol: ")
    try:
        url = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' + search_quote
        df = pd.DataFrame([requests.get(url).json()])
        print("\n")
        dropped_columns = ["MSDate", "Status", "Timestamp"]
        df1 = df.drop(dropped_columns, axis="columns")
        df1 = df.drop(dropped_columns, axis="columns")
        df2 = df1
        df1 = df1.reindex(
            ['Symbol', 'Name', 'Open', 'LastPrice', 'Change', 'ChangePercent'],
            axis=1)
        df2 = df2.reindex([
            'Symbol', 'Low', 'High', 'MarketCap', 'ChangePercentYTD',
            'ChangeYTD'
        ],
                          axis=1)

        print("Quote for " + search_quote.upper() + " as of " +
              datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " UTC:\n\n")
        
        print(th.md_table(df1, formats={-1: 'c'}))
        print("\n"+th.md_table(df2, formats={-1: 'c'}))

    except:
        print("Server not responding. Try again later. ")
        time.sleep(1)
        pass


def leaderboard():
    print("Leaderboard: \n\n")
    with sqlite3.connect('data.db') as db:
        df = pd.read_sql_query('SELECT * from stocks', db)
        df_1 = pd.read_sql_query('SELECT username , bankAccount from users', db)
        df_1.sort_values(by=['bankAccount'], inplace=True, ascending = False)
        df_1 = df_1.rename(columns={'username': "User:", 'bankAccount': "Money:"})
        try:
            df_1 = df_1.head(10)
            print(th.md_table(df_1, formats={-1: 'c'}))
        except AttributeError:
            print(th.md_table(df_1, formats={-1: 'c'}))
    
    
def buy_stock():
    buy_quote = input("Enter exact stock symbol you want to buy: ")
    buy_quote_upper = buy_quote.upper()
    num_shares = input("Number of shares you want to buy of " +
                       buy_quote.upper() + "? ")
    buy_stock.buy_quote = buy_quote
    buy_stock.num_shares = num_shares
    url = urlopen(
        'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' +
        buy_quote)
    obj = json.load(url)
    stock_price = obj["LastPrice"]
    buy_stock.stock_price = stock_price
    amount_deducted = float(stock_price) * float(num_shares)

    with sqlite3.connect('data.db') as db:
        cursor = db.cursor()
    find_bank_balance = ("SELECT bankAccount from users WHERE username = ?")
    cursor.execute(find_bank_balance, [(login.current_user[0])])
    results = list(cursor)
    results_list = [x[0] for x in results]

    new_balance = float(results_list[0]) - float(amount_deducted)
    with sqlite3.connect('data.db') as db:
        cursor = db.cursor()
        # update_bank_balance = (
        #     "UPDATE users SET bankAccount WHERE username = ?")
        cursor.execute(
            '''UPDATE users SET bankAccount = ? WHERE username = ?''',
            (new_balance, login.current_user[0]))
    print('''
          Your order was successfully executed. Your bank balance is: ''' +
          str(new_balance))
    # insertData_ = '''INSERT INTO stock(username, password)
    #     VALUES(?,?)'''
    # cursor.execute(insertData, [username, password])
    with sqlite3.connect('data.db') as db:
        cursor = db.cursor()
        cursor.execute('UPDATE stocks SET numShares = numShares + '+num_shares+' WHERE username = "'+login.current_user[0]+'" AND stockSymbol = "'+buy_quote_upper+'";')
        cursor.execute('INSERT INTO stocks(username, stockSymbol, numShares) SELECT "'+login.current_user[0]+'", "'+buy_quote_upper+'", "'+num_shares+'" WHERE (Select Changes() = 0);')


    # //TODO: Add import to database for buy_stock (UserID, stock_symbol, time_stamp, number_shares)


def sell_stock():
    sell_quote = input("Enter exact stock symbol you want to sell: ")
    sell_quote_upper = sell_quote.upper()
    num_shares_sold = int(input("Number of shares you want to sell of " +
                            sell_quote_upper + "? "))
    try:
        url = urlopen(
            'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' +
            sell_quote)
        obj = json.load(url)
        stock_price = obj["LastPrice"]
        amount_added = float(stock_price) * float(num_shares_sold)

        with sqlite3.connect('data.db') as db:
            df = pd.read_sql_query('SELECT stockSymbol, numShares FROM stocks WHERE username="'+login.current_user[0]+'";', db)
            df_1 = df[(df.stockSymbol.str.contains(sell_quote_upper))]
            shares_owned = int(df_1.iloc[0]['numShares'])
            stock_list = df_1.values.tolist()
            # df_1 = pd.read_sql_query('SELECT numshares from stocks ')
    # try:

        if num_shares_sold <= shares_owned and sell_quote_upper in stock_list[0]:
            with sqlite3.connect('data.db') as db:
                cursor = db.cursor()
                find_bank_balance = ("SELECT bankAccount from users WHERE username = ?")
                cursor.execute(find_bank_balance, [(login.current_user[0])])
                results = list(cursor)
                results_list = [x[0] for x in results]
                new_balance = float(results_list[0]) + float(amount_added)
                cursor.execute(
                        '''UPDATE users SET bankAccount = ? WHERE username = ?''',
                        (new_balance, login.current_user[0]))
                cursor.execute('UPDATE stocks SET numShares = numShares - '+str(num_shares_sold)+' WHERE username = "'+login.current_user[0]+'" AND stockSymbol = "'+sell_quote_upper+'";')
                print('''
                    Your order was successfully executed. Your bank balance is: ''' + str(new_balance))
        else:
            print("You don't own the stocks you are trying to sell! ")
    except KeyError:
        print("Invalid operation. Please try again. ")
    except ValueError:
        print("Invalid operation. Please try again. ")
    except AttributeError:
        print("Invalid operation. Please try again. ")


            
            

    # //TODO: Immediately add to bank account the moment the user sells a stock.
    # //TODO: Add import to database for sell_stock (UserID, stock_symbol, time_stamp, number_shares)


def stock_table_update():
    data = [
        login.current_user[0], buy_stock.buy_quote, buy_stock.stock_price,
        buy_stock.num_shares
    ]
    df = pd.DataFrame(
        [data], columns=["username", "stockSymbol", "price", "numShares"])

    # df = pd.DataFrame([[username]])
    print(data)
    # with sqlite3.connect("data.db") as db:
    #     c = db.cursor()
    #
    #     c.execute('''UPDATE stocks SET stockSymbol = ? WHERE username = ?''',
    #               (buy_stock.buy_quote, login.current_user[0]))


def view_portfolio():
    #//TO: Use pandas to easily display portfolio
    with sqlite3.connect('data.db') as db:
        # cursor = db.cursor() 
        df = pd.read_sql_query('SELECT * from stocks WHERE username="'+login.current_user[0]+'";', db)
        df = df.reindex(["stockSymbol","numShares"] ,axis=1)
        df = df.rename(columns={'stockSymbol': "Stocks Owned:", 'numShares': "# of Shares:"})
        print("\nYour Current Portfolio:\n\n"+th.md_table(df, formats={-1: 'c'}))

    # data = [
    #     login.current_user, buy_stock.buy_quote, buy_stock.stock_price,
    #     buy_stock.num_shares
    # ]
    # df = pd.DataFrame(
    #     [data], columns=["username", "stockSymbol", "price", "numShares"])

    # print(data)


def logout():
    login.current_user.clear()
    login.current_user = []
    print("You have successfully logged out! ")
    time.sleep(1)
    return main_menu()

if __name__ == "__main__":
    create_tables()
    seed_users()
    heading()
    main_menu()
