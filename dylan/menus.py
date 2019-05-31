def homepage():
    return '''
##########################################################


    What would you like to do today?
        1 --- Login
        2 --- Register
        Please type q and press enter to quit


##########################################################

>>>  '''

def login_page(username, admin):
    if admin == 1:
        return f'''
#########################################################


    What would you like to do today {username}?
        1 --- Check Account Details
        2 --- Update Password
        3 --- 
        4 --- 
        Please type any key and press enter to log out


#########################################################

>>>  '''
    else:    
        return f'''
#########################################################


    What would you like to do today {username}?
        1 --- Check Account Details
        2 --- Update Password
        3 --- 
        4 --- 
        Please type any key and press enter to log out


#########################################################

>>>  '''