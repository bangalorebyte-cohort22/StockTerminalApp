#!/usr/bin/env python3

from userman import *
# from dbman import *

'''
Login
'''
def login():
    email = input("Enter your email address: ")
    password = getpass.getpass(prompt='Enter your password: ')
    #Authentication
    c.execute('SELECT EXISTS(SELECT 1 FROM users WHERE email=? LIMIT 1)', (email,))
    x = c.fetchone()[0]
    if x:
        if check_user_pass(email, password):
           global username
           global user_type
           username = email
           c.execute('SELECT user_type FROM users WHERE email=?',(username,))
           user_type = str(c.fetchone()[0])
            
    else:
        print("\nPlease check the credentials! \nTry again!>> ")
        login()

'''
Logout
'''
def logout(user_name):
    user_name = "null"
    user_type = "null"

'''
Global variables for login.
'''
user_name = "null"
user_type = "null"
system = "run"


if __name__ == "__main__":
    while system == 'run':
        # print(main_menu)
        first_input = input(main_menu)
        if first_input == '1':
            login()
            if user_type == 'admin':
                print(admin_menu)
                admin_input = input(">>> ")
            else:
                print(user_menu)
                user_input = input(">>> ")
        elif first_input == '2':
            pass
        elif first_input == 'q' or first_input == 'Q':
            print(quit)
            system = "end"

