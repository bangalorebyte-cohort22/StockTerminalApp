from datetime import datetime

from queries import get_all_users, add_user, buy_stock, check_funds, deduct_account, stock_portfolio, check_stocks, sell_stock, credit_account, leaderboard
from menus import admin_page, user_page
from wrapper import Markit


def login():
    users = get_all_users()
    response = input('''Welcome to the login page. Please type q and hit enter now to go back to the main menu.
Otherwise, just hit enter.''')
    if response == "q":
        return None
    username_input = input("What's your username?\n>>>   ")
    password_input = input("What's your password?\n>>>   ")
    if username_input not in users['username'].values:
        print("Invalid credentials.")
        return None
    elif username_input in users['username'].values:
        if password_input != users[users['username'] == username_input]['password'].values[0]:
            print("Invalid credentials.")
            return None
        elif password_input == users[users['username'] == username_input]['password'].values[0]:
            print("Correct credentials.")
            print(f"Logging you in now {username_input}.")
            return users[users['username'] == username_input].to_dict('records')[0] 


def register():
    users = get_all_users()
    response = input('''Welcome to the registration page. Please type q and hit enter now to go back to the main menu.
Otherwise, just hit enter.''')
    print(response)
    if response == "q":
        return
    else:
        username = False
        while not username:
            username_input = input("What username would you like? Your username isn't case sensitive.\n>>>   ").strip().lower()
            if username_input == "":
                print("Please don't enter just spaces.")
                continue
            elif username_input in users['username'].values:
                print("That username is already taken.")
                continue
            elif username_input not in users['username'].values:
                username = username_input
        password_input = input("What password would you like? Your password is case-sensitive.\n>>>   ")
        print(f'''
Here are your details. Please note them down somewhere:
    Username: {username}
    Password: {password_input}        
''')    
        add_user(username,password_input)
        print("You were successfully added to the system.")
        

def user_app(user):
    while user is not None:
        markit = Markit()
        ask = input(user_page(user['username'])).strip().lower()
        if ask == str(1):
            company_input = input("What company would you like to search for? Please enter just one company or the search engine won't work.\n>>>   ")
            companies = markit.company_search(company_input)
            if companies.empty:
                print("Cannot find any data for that company name.")
            else:
                print("Here's a list of companies that might match your search with some basic info:")
                print(companies)

        elif ask == str(2):
            ticker_input = input("Which stock would you like current market data for? Please type the ticker.\n>>>   ").strip().upper()
            quote = markit.get_quote(ticker_input, 'Name','Symbol','LastPrice','Open','Timestamp')
            if quote.empty:
                print("Cannot find data for that ticker.")
            else:
                print(f"Here's the quote for {ticker_input}:")
                print(quote)

        elif ask == str(3):
            portfolio = stock_portfolio(user['username'])
            if portfolio.empty:
                print("You don't have any stocks.")
            else:
                print("Here's a list of the stocks you own:")
                print(portfolio)

            
        elif ask == str(4):
            buy = False
            while not buy:
                purchase_req = input("Enter the ticker and number of shares you'd like to purchase separated by spaces? Eg: AAPL 5 or NFLX 2.\n>>>   ").split()
                if len(purchase_req) != 2:
                    print("Please input the order in the correct format.")
                    continue
                try:
                    number_of_shares = int(purchase_req[1].strip())
                except:
                    print("Please enter an integer for number of shares.")
                    continue
                if int(number_of_shares) != float(number_of_shares):
                    print("You can't sell fractions of shares.")
                    continue
                ticker_input = purchase_req[0].strip().upper()
                quote = markit.get_quote(ticker_input,"LastPrice",'Timestamp')
                if quote.empty:
                    print("Could not get data for that ticker.")
                    continue
                print(f"Here's the quote for {ticker_input}, along with the price timestamp:")
                print(quote)
                stock_price = quote.loc['LastPrice',0]
                if not check_funds(user['username'],stock_price,number_of_shares):
                    print("You don't have enough money in your bank account to complete this transaction. Consider buying a lower amount of shares or another stock.")
                    continue

                confirm = False
                while not confirm:
                    ask = input("Would you like to execute this buy order? Yes or No?").strip().lower()
                    if ask not in ["yes","no"]:
                        print("Please enter yes or no.")
                        continue
                    elif ask == "yes":
                        now = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                        buy_stock(user['username'],ticker_input,stock_price,number_of_shares,now)
                        new_balance = deduct_account(user['username'],stock_price,number_of_shares)
                        confirm = True
                        buy = True
                        print(f"Bought {number_of_shares} shares of {ticker_input} for you at {now}. Your new account balance is {new_balance}.")
                    elif ask == "no":
                        print("Taking you back to the main menu.")
                        confirm = True
                        buy = True

        elif ask == str(5):
            sell = False
            while not sell:
                sell_req = input("Enter the ticker and number of shares you'd like to sell separated by spaces? Eg: AAPL 5 or NFLX 2.\n>>>   ").split()
                if len(sell_req) != 2:
                    print("Please input the order in the correct format.")
                    continue
                try:
                    number_of_shares = int(sell_req[1].strip())
                except:
                    print("Please enter an integer for number of shares.")
                    continue
                if int(number_of_shares) != float(number_of_shares):
                    print("You can't sell fractions of shares.")
                    continue
                ticker_input = sell_req[0].strip().upper()
                quote = markit.get_quote(ticker_input,"LastPrice",'Timestamp')
                if quote.empty:
                    print("Could not get data for that ticker.")
                    continue
                if not check_stocks(user['username'],ticker_input,number_of_shares):
                    print(f"You don't have that many shares of {ticker_input} to sell.")
                    continue
                print(f"Here's the quote for {ticker_input}, along with the price timestamp:")
                print(quote)
                stock_price = quote.loc['LastPrice',0]
                confirm = False
                while not confirm:
                    ask = input("Would you like to execute this sell order? Yes or No?\n>>>   ").strip().lower()
                    if ask not in ["yes","no"]:
                        print("Please enter yes or no.")
                        continue
                    elif ask == "yes":
                        now = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                        sell_stock(user['username'],ticker_input,stock_price,number_of_shares,now)
                        new_balance = credit_account(user['username'],stock_price,number_of_shares)
                        confirm = True
                        sell = True
                        print(f"Sold {number_of_shares} shares of {ticker_input} for you at {now}. Your new account balance is {new_balance}.")
                    elif ask == "no":
                        print("Taking you back to the main menu.")
                        confirm = True
                        sell = True

        elif ask == "q":
            print(f"Logging you out {user['username']}")
            user = None
            return user

        else:
            print("Please enter one of the options.")
        input(f"Please press enter to go back to your main menu {user['username']}")


def admin_app(user):
    while user is not None:
        markit = Markit()
        ask = input(admin_page(user['username'])).strip().lower()
        if ask == str(1):
            print("Fetching current market data...")
            data = leaderboard(markit)
            print("Here's the leaderboard in terms of net worth:")
            print(data)
        elif ask == "q":
            print(f"Logging you out {user['username']}")
            user = None
            return user
        else:
            print("Please enter one of the options.")
        input(f"Please press enter to go back to your main menu {user['username']}")


