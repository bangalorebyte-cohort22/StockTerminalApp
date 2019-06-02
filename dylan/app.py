import sqlite3
from helper import register,login, user_app, admin_app
from menus import homepage

def run_app(run, user):
    while run == True:
        if user is None:
            try:
                ask = input(homepage()).strip().lower()
                if ask == str(1):
                    user = login()
                elif ask == str(2):
                    print("regitration")
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
            if user['admin'] == 1:
                user = admin_app(user)
            elif user['admin'] == 0:
                user = user_app(user)

            

if __name__ == '__main__':
    run = True
    user = None
    run_app(run, user)