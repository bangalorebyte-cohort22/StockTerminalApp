def homepage():
    return '''
##########################################################


    What would you like to do today?
        1 --- Login
        2 --- Register
        Please type q and press enter to quit


##########################################################

>>>  '''

def admin_page(username):
        return f'''
#########################################################


    What would you like to do today {username}?
        1 --- See Leaderboard
        Please type q and enter to logout


#########################################################

>>>  '''

def user_page(username):  
        return f'''
#########################################################


    What would you like to do today {username}?
        1 --- Search Tickers
        2 --- Stock Market Data
        3 --- View Portfolio
        4 --- Buy Stocks
        5 --- Sell Stocks
        Please type q and enter to logout


#########################################################

>>>  '''