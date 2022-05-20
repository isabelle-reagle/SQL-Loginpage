from DatabaseLayer import *
from getpass import getpass

def main():
    print("Welcome to the testing phase of the SQL integration test.")
    print("Type help for a list of commands.")
    # print("$", end=" ")

    while True:
        message = input(" $ ")  

        response = verify_loginpage_input(message)
        print(response)
"""
Checks the user's input and makes a decision according to it
Commands:
    register: register an account
    login: log in with an account
    help: get command list
"""
def verify_loginpage_input(s):
    s = s.split(" ")
    if s[0] == "help":
        return """Commands:
        \tregister [username]: registers an account
        \tlogin [username]: logs into an existing account
        \thelp: brings up this menu"""
    elif s[0] == "register" and len(s) > 1:
        register_password(s[1])
        return "Account created successfully. Please log in"
    elif s[0] == "register":
        register()
        return "Account create sucessfully. Please log in"
    elif s[0] == "login":
        login_password(s[1])
    else:
        return "Invalid command. Type help for a list of commands."


def register_username(s):
    while True:
        username = input("Username: ")
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

"""
Prompts a user to enter their account password,
Then sends a request to the SQL integration layer to register the account
"""
def register_password(s):
    while True:
        password = getpass()
        validity = User.is_valid_username(password)
        if validity == "LENGTH_EXCEEDS":
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

    return User(s, password )


if __name__ == "__main__":
    main()