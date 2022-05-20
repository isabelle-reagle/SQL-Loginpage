from DatabaseLayer import *
from getpass import getpass

def main():
    print("Welcome to the testing phase of the SQL integration test.")
    print("Type help for a list of commands.")


    account = None
    
    # login / register loop
    while True:
        message = raw_input("/$ ")  
        response, account = verify_loginpage_input(message)
        if (response == "EXIT"):
            return
        print(response)
        if response == "Logged in successfully":
            break
    
    # account loop
    while True:
        message = raw_input("/{0}$ ")

        response = verify_accountpage_input(message)


"""
Checks the user's input on the account page and makes a decision according to it
"""
def verify_accountpage_input(s):
    s = s.split(" ")
    return


"""
Checks the user's input on the login screen and makes a decision according to it
Commands:
    register: register an account
    login: log in with an account
    help: get command list
"""
def verify_loginpage_input(s):
    print(s)
    s = str(s).split(" ")
    if s[0] == "help":
        return ("""Commands:
        \tregister [username]: registers an account
        \tlogin [username]: logs into an existing account
        \thelp: brings up this menu
        \texit / stop: stops the program
        \tadminmenu {requires admin verification}: debug statistics""", None)
    elif s[0] == "exit" or s[0] == "stop":
        return "EXIT", None
    elif s[0] == "register" and len(s) > 1:
        tmp = register_password(s[1])
        if tmp:
            return "Account created successfully. Please log in", tmp
        else:
            return None, None
    elif s[0] == "register":
        tmp = register()
        if tmp:
            return "Account created sucessfully. Please log in", tmp
        else:
            return None, None
    elif s[0] == "login" and len(s) > 1:
        tmp = login_password(s[1])
        if tmp:
            return "Logged in sucessfully", tmp
        else:
            return None, None
    elif s[0] == "login":
        tmp = login()
        if tmp:
            return "Logged in successfully", tmp    
        else:
            return None, None
    elif s[0] == "admin":
        return User.execute_sql_select("SELECT * FROM users"), None
    else:
        return "Invalid command. Type help fogr a list of commands.", None


"""
Prompts a user to register their username
"""
def register_username(username = None):
    while True:
        if not username:
            username = raw_input("Username: ")
        if username == "back":
            return None
        validity = User.is_valid_username(username)
        if validity == "LENGTH_EXCEEDS":
            print("Username is invalid. Maximum length is 20 characters\nType 'back' to return to home page")
            username = None
            continue
        elif validity == "LENGTH_TOO_LOW":
            print("Username is invalid. Minimum length is 3 characters\nType 'back' to return to home page")
            username = None
            continue
        elif validity == "SQL_INJECTION":
            print("Invalid character in username\nType 'back' to return to home page")
            username = None
            continue
        elif validitiy == "INVALID_CHARACTER":
            print("Invalid character in username\nType 'back' to return to home page")
            username = None
            continue    
        elif validity == "DUPLICATE":
            print("Sorry. That username is already taken\nType 'back' to return to home page")
            username = None
            continue
        break

    return register_password(username)


def register(s = None):
    while True:
        if (not s):
            username = raw_input("Username: ")
        if username == "back":
            return None
        validity = User.is_valid_username(username)

        if validity == "LENGTH_EXCEEDS":
            print("Username is too long. Maximum length is 20 characters.\nType 'back' to return to home page")
            s = None
            continue
        elif validity == "LENGTH_TOO_LOW":
            print("Username is too short. Minimum length is 3 characters.\nType 'back' to return to home page")
            s = None
            continue
        elif validity == "DUPLICATE":
            print("Username already taken.\nType 'back' to return to home page")
            s = None
            continue
        elif validity == "SQL_INJECTION":
            print("Invalid character in username.\nType 'back' to return to home page")
            s = None
            continue
        elif validity == "INVALID_CHARACTER":
            print("Invalid character in username.\nType 'back' to return to home page")
            s = None
            continue

        return register_password(username)


"""
Prompts a user to enter their account password,
Then sends a request to the SQL integration layer to register the account
"""
def register_password(s):
    
    while True:
        password = getpass()
        validity = User.is_valid_password(password)
        if validity ==  "LENGTH_EXCEEDS":
            print("Password is invalid. Maximum length is 40 characters\nType 'back' to return to home page")
            continue
        elif validity == "LENGTH_TOO_LOW":
            print("Password is too short. Must be a minimum of 8 characters\nType 'back' to return to home page")
            continue
        elif validity == "SQL_INJECTION":
            print("Invalid character in password\nType 'back' to return to home page")
            continue
        break
    while True:
        password2 = getpass("  Password: ")
        if password != password2:
            print("Passwords do not match. Try again\nType 'back' to return to home page")       
            continue
        break

    return User(s, password)


"""
Prompts a user to enter their login username
"""
def login():
    while True:
        username = raw_input("Username: ")
        if username == "back":
            return None
        tmp = User.find_user_by_name(username)
        if tmp:
            return login_password(tmp)
        print("Invalid username.\nType back to return to the home page.") 
        continue
        

"""
Prompts a user to enter their login password
"""
def login_password(user):
    while True:
        password = raw_input("Password: ")
        if password == "back":
            return None
        if user.password_hash == hash(password):
            return user
        print("Incorrect password\nType back to return to the home page")
        continue

if __name__ == "__main__":
    main()