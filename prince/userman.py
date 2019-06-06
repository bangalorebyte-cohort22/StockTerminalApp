#!/usr/bin/env python3
''' This manages users, login and logout. '''

import getpass
import bcrypt
import sqlite3
import json
import requests

main_menu =  '''
 _______                  _             _   _______            _             __   ___  
|__   __|                (_)           | | |__   __|          | |           /_ | / _ \ 
   | | ___ _ __ _ __ ___  _ _ __   __ _| |    | |_ __ __ _  __| | ___ _ __   | || | | |
   | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | |    | | '__/ _` |/ _` |/ _ \ '__|  | || | | |
   | |  __/ |  | | | | | | | | | | (_| | |    | | | | (_| | (_| |  __/ |     | || |_| |
   |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|    |_|_|  \__,_|\__,_|\___|_|     |_(_)___/ 
                                                                                       
                1. Login
                2. Sign Up
                q: Quit
                '''

user_menu = '''
 _______                  _             _   _______            _             __   ___  
|__   __|                (_)           | | |__   __|          | |           /_ | / _ \ 
   | | ___ _ __ _ __ ___  _ _ __   __ _| |    | |_ __ __ _  __| | ___ _ __   | || | | |
   | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | |    | | '__/ _` |/ _` |/ _ \ '__|  | || | | |
   | |  __/ |  | | | | | | | | | | (_| | |    | | | | (_| | (_| |  __/ |     | || |_| |
   |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|    |_|_|  \__,_|\__,_|\___|_|     |_(_)___/ 

               1. Search by Company Name
               2. View Stock Ticker
               3. View Portfolio
               4. Buy Stocks
               5. Sell Stocks
               6. Logout
               '''

admin_menu = '''
 _______                  _             _   _______            _             __   ___  
|__   __|                (_)           | | |__   __|          | |           /_ | / _ \ 
   | | ___ _ __ _ __ ___  _ _ __   __ _| |    | |_ __ __ _  __| | ___ _ __   | || | | |
   | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | |    | | '__/ _` |/ _` |/ _ \ '__|  | || | | |
   | |  __/ |  | | | | | | | | | | (_| | |    | | | | (_| | (_| |  __/ |     | || |_| |
   |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|    |_|_|  \__,_|\__,_|\___|_|     |_(_)___/ 
                                                                                       
               1. View Leaderboard
               2. Logout                                                                      
               '''

'''
Accessing the db.
'''
conn = sqlite3.connect('nasdaq.db')
c = conn.cursor()

'''
user autheentication
'''
#Generating a bcrypt hash of the passowrd entered.
def gen_paswd(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

#Checking user password with the one that is in the db.
def check_user_pass(email, password):
    c.execute('SELECT password FROM users WHERE email=?', (email,))
    c_hash_pwd = c.fetchone()[0].encode('utf-8')

    if bcrypt.hashpw(password.encode('utf-8'), c_hash_pwd) == c_hash_pwd:
        return True
    else:
        return False

def search_company():
   company_name = input("Enter the company name: ")
   response = requests.get(f'http://dev.markitondemand.com/Api/v2/Lookup/json?count=3&input={company_name}')
   try:
      symbol = json.loads(response.content)[0]['Symbol']
      return symbol
   except:
      print("This company does not exist on NASDAQ. Try again")
      search_company()

def get_price():
   pass