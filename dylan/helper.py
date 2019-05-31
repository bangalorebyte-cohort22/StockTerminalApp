from queries import get_all_users, add_user
from menus import admin_page, user_page
from wrapper import Markit

def login():
    users = get_all_users()
    response = input('''Welcome to the login page. Please type q and hit enter now to go back to the main menu.
Otherwise, just hit enter.\n>>>   ''')
    if response == "q":
        return None
    username_input = input("What's your username?")
    password_input = input("What's your password?")
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
Otherwise, just hit enter.\n>>>   ''')
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
            print("Here's a list of companies that might match your search with some basic info:")
            print(companies)

        elif ask == str(2):
            ticker_input = input("Which stock would you like current market data for? Please type the ticker!")
            quote = markit.get_quote(ticker_input)
            print(f"Here's the quote for {ticker_input}:")
            print(quote)

        elif ask == str(3):
            pass

        elif ask == str(4):
            pass

        elif ask == str(5):
            pass

        elif ask == "q":
            print(f"Logging you out {user['username']}")
            user = None
            return user

        else:
            print("Please enter one of the options.")



def admin_app(user):
    while user is not None:
        ask = input(user_page(user['username'])).strip().lower()
        if ask == str(1):
            pass
        elif ask == "q":
            print(f"Logging you out {user['username']}")
            user = None
            return user
        else:
            print("Please enter one of the options.")