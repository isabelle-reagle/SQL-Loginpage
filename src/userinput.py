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
        if (not response):
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
    print(s)
    if s[0] == "help":
        return ("""Commands:
        \tregister [username]: registers an account
        \tlogin [username]: logs into an existing account
        \thelp: brings up this menu
        \texit / stop: stops the program
        \tadminmenu {requires admin verification}: debug statistics""", None)
    elif s[0] == "exit" or s[0] == "stop":
        return None, None
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
    else:
        return "Invalid command. Type help fogr a list of commands.", None


def register_username():
    while True:
        username = raw_input("Username: ")
        validity = User.is_valid_username(username)
        if validity == "LENGTH_EXCEEDS":
            print("Username is invalid. Maximum length is 20 characters")
            continue
        elif validity == "LENGTH_TOO_LOW":
            print("Username is invalid. Minimum length is 3 characters")
            continue
        elif validity == "SQL_INJECTION":
            print("Invalid character in username")
            continue
        elif validitiy == "INVALID_CHARACTER":
            print("Invalid character in username")
            continue
        elif validity == "DUPLICATE":
            print("Sorry. That username is already taken")
            continue
        break

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
            print("Password is invalid. Maximum length is 40 characters")
            continue
        elif validity == "LENGTH_TOO_LOW":
            print("Password is too short. Must be a minimum of 8 characters")
            continue
        elif validity == "SQL_INJECTION":
            print("Invalid character in password")
            continue
        break
    while True:
        password2 = getpass("Verify Password: ")
        if password != password2:
            print("Passwords do not match. Try again")       
            continue
        break

    return User(s, password)

def login():
    pass

def login_password(s):
    pass

if __name__ == "__main__":
    main()