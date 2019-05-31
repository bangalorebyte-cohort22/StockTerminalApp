import sqlite3
from .helper import login, register
from .menus import login_page, homepage

def run_app(run, user):
    while run == True:
        if user is None:
            try:
                ask = input(homepage()).strip().lower()
                if ask == str(1):
                    user = login()
                elif ask == str(2):
                    register()
                elif ask == "q":
                    print("Now exiting the program...")
                    print("Goodbye!")
                    run = False
                else:
                    print("Please enter either 1 or 2.")
                    input("Press enter to go back to main menu.")
            except:
                print("Please enter either 1 or 2.") 
                input("Press enter to go back to the main menu.")
        else:
            ask = login_page(user['username'],user['admin'])