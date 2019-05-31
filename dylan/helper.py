from dylan.queries import get_all_users, add_user
from dylan import con

def login():
    global con
    users = get_all_users(con)
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
        if password_input != users[users['username'] == username_input]['password'].value[0]:
            print("Invalid credentials.")
            return None
        elif password_input == users[users['username'] == username_input]['password'].value[0]:
            print("Correct credentials.")
            print(f"Logging you in now {username_input}.")
            print(users[users['username'] == username_input].to_dict())
            return users[users['username'] == username_input].to_dict() 


def register():
    global con
    users = get_all_users(con)
    response = input('''Welcome to the registration page. Please type q and hit enter now to go back to the main menu.
Otherwise, just hit enter.\n>>>   ''')
    if response == "q":
        return
    else:
        username = False
        password = False
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
Here are your details. You can always change them later:
    Username: {username_input}
    Password: {password_input}        
''')    
        print("Adding you to our system.")
        add_user(username,password,con)
        print("You were added. Feel free to log in at the main menu.")
        return