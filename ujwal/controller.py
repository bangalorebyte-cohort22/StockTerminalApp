import pandas as pd
from re import findall
import model
import viewer

initial_money = 100000
markit = model.Markit()

def register(is_super):
    '''returns login() which returns (is_super,username) and asks for a unique username and
    a password with at least one upper case, one lower case, one number, one of 
    @#$ and at least 8 characters long as separate inputs then adds username, 
    password and initial_money to corresponding table determined by is_super'''
    while 1:
        username = viewer.ask_register_username()        
        if len(findall(r"\s",username))!=0:
            viewer.error_username_spaces()
        elif model.check_username(username):
            viewer.error_username_taken()
        else:
            break
    
    while 1:
        password = viewer.ask_register_password()
        if len(findall(r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$]).{8,}",
                       password))>0 and len(findall(r"\s",password)) == 0:
            break
        viewer.error_password()

    model.add_user(username,password,initial_money,is_super)
    viewer.done_register(is_super,username)
    return login()

def login():
    '''returns (is_super,username) determined by the correct pair
    of username and password that the user has entered
    user can go back to the menu then is_super wil be resetted'''
    viewer.show_login()
    is_back = None
    while 1:
        username = viewer.ask_login_username()
        logged_super = model.check_user(username,viewer.ask_login_password())
        if logged_super[0]:
            break
        viewer.error_login()
        is_back = viewer.ask_back()
        if is_back:
            break
    is_super = None if is_back==False else logged_super[1]
    viewer.done_login(is_super)
    return tuple([is_super,username])

def do_search(is_company_search):
    while 1:
        if is_company_search:
            stock_data = markit.company_search(viewer.ask_company_search())
        else:
            stock_data = markit.get_stock_info(viewer.ask_retrieve_market_data())
        if stock_data != False:
            viewer.show_table(stock_data)
            viewer.ask_continue()
            break
        viewer.error_no_results()
        if viewer.ask_back():
            break    

def do_company_search():
    do_search(True)

def do_retrieve_market_data():
    do_search(False)  

def leaderboard():
    pass

def view_total_value(username):
    pass

def view_stock_list(username):
    pass

def do_buy_stock(username,is_super):
    while 1:
        viewer.show_money(model.user_money(username,is_super))
        stock_data=markit.get_stock_info(viewer.ask_stock(is_buy=True))
        if stock_data==False:
            viewer.error_no_results()
            if viewer.ask_back():
                break            
        else:
            stock_name=stock_data[0]["Name"]
            stock_symbol=stock_data[0]["Symbol"]
            stock_price=stock_data[0]["LastPrice"]
            viewer.show_price_qty(stock_name,stock_price)
            qty=viewer.ask_qty(is_buy=True)
            if qty == False:
                break
            stock_price=markit.get_stock_info(stock_symbol)[0]["LastPrice"]
            if model.buy_stock(username,is_super,stock_symbol,stock_price,qty):
                viewer.done_stock(stock_name,stock_price,qty,is_buy=True)
                break
            viewer.error_no_money(model.user_money(username,is_super),stock_price*qty)
            if viewer.ask_back():
                break
                
def do_sell_stock(username,is_super):
    while 1:
        stock_symbol=viewer.ask_stock(is_buy=False)
        own_qty=model.get_user_stock(username,stock_symbol.upper())
        if own_qty == False:
            viewer.error_not_own_stock()
            if viewer.ask_back():
                break
        else:
            stock_data=markit.get_stock_info(stock_symbol)
            stock_name=stock_data[0]["Name"]
            stock_symbol=stock_data[0]["Symbol"]
            stock_price=stock_data[0]["LastPrice"]            
            viewer.show_price_qty(stock_name,stock_price,own_qty)        
            sell_qty=viewer.ask_qty(is_buy=False)
            if sell_qty == False:
                break
            stock_price=markit.get_stock_info(stock_symbol)[0]["LastPrice"]
            if model.sell_stock(username,is_super,stock_symbol,stock_price,sell_qty):
                viewer.done_stock(stock_name,stock_price,sell_qty,is_buy=False)
                break
            viewer.error_no_quantity(own_qty,sell_qty)
            if viewer.ask_back():
                break                

def do_choice(choice,username,is_super):
    if choice == "rsu" or choice == "ru":
        return register(choice == "rsu")
    elif choice == "li":
        return login()
    elif choice == "sc":
        return [do_company_search()]
    elif choice == "rmd":
        return [do_retrieve_market_data()]
    elif choice == "bs":
        do_buy_stock(username,is_super)
    elif choice == "ss":
        do_sell_stock(username,is_super)
    elif choice == "vtv":
        view_total_value(username,is_super)
    elif choice == "vls":
        view_stock_list(username)
    elif choice == "lb":
        leaderboard()
    elif choice == "lo":
        viewer.done_logout()
        return "lo"
    elif choice == "exit":
        viewer.show_exit()
        return ["exit"]

def b4_login():
    is_super = None
    while is_super == None and is_super != "exit":
        is_super_username = do_choice(viewer.begin_menu(),None,None)
        is_super = is_super_username[0]
        username = is_super_username[1] if is_super != None and is_super != "exit" else None
    return is_super,username
        
def after_login(is_super,username):
    while 1:
        is_logout = do_choice(viewer.logged_menu(is_super),username,is_super) == "lo"
        if is_logout:
            return None

def start():
    while 1:
        is_super_username = b4_login()
        is_super = is_super_username[0]
        username = is_super_username[1]
        if is_super == "exit":
            return None
        after_login(is_super,username)

viewer.show_welcome()
start()