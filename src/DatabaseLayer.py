import sqlite3
import uuid
import hashlib

def get_path():
    return "rentalDB.db"
    
PATH = "rentalDB.db"

"""
sends a vital error to me
"""
def send_error(message, *argv):
    pass

def get_sql_connection(path):
    return sqlite3.connect(path)


#region usermanagment

"""
Finds a user from the SQL database by their ID
returntype: User
"""
def find_user_in_database(id, path):
    connection = get_sql_connection(path)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE id={0}".format(id))
    rows = cursor.fetchall()
    if len(rows) > 1:
        send_error("DUPLICATE_ID", id)
        raise Exception(
            "DUPLICATE_ID_ERROR. FATAL ERROR. CONTACT US IMMEDIATELY")

    """
    User is not present in the database
    """
    if len(rows) == 0:
        return 1

    id = rows[0][0]

    return User.get_user_by_id(id)


"""
Short-term representation of user as an object
"""
class User:
    users = []


    def __init__(self, username, password, id=None, password_is_hashed=False):
        if (id):
            self.id = id
        else:
            self.id = uuid.uuid1()
        self.username = username
        # self.password_hash = hash(password)

        if (password_is_hashed):
            self.password_hash = password
        else:
            self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        """
        Logs User to registry and database
        """
        if (not self.user_in_database()):
            self.write_user()

        """
        Removes duplicates from the user registry
        These duplicates aren't a big deal, since it is not in the formal database
        """
        while User.find_user_in_registry(self.id) != None:
            User.users.remove(User.find_user_in_registry(self.id))
        User.users.append(self)

    """
    Checks if a User is in the database or not
    Checks by ID, so duplicate usernames and passwords are allowed
    returntype: bool, if User is in database
    """

    def user_in_database(self):
        connection = get_sql_connection(PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM users WHERE id = \"{0}\"".format(self.id))

        results = cursor.fetchall()

        return len(results) != 0

    """
    Writes a User to the SQL database
    returntype: int (error code)
        0: success
        1: User already present
        2: sql injection attempt
    """
    def write_user(self):
        # Ensure that no SQL injection is attempted
        if "--" in self.username or "--" in str(self.password_hash):
            print("SQL INJECTION ATTEMPT")
            return 2
        # Do not add User to the database if they are already present
        if self.user_in_database():
            print("User already in database.")
            return 1

        # establish connection to the SQL database
        connection = get_sql_connection(PATH)
        cursor = connection.cursor()

        # insert the new user into the database
        cursor.execute("INSERT INTO users VALUES(\"{0}\", \"{1}\", \"{2}\");".format(
            self.id, self.username, self.password_hash))


        # commit changes
        connection.commit()
        connection.close()

        return 0

    """
    Removes a User from the platform entirely
    Includes removal from the registry and database
    """
    def remove_user(self):
        connection = get_sql_connection(PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM users WHERE id = {0}".format(self.id))
        if self in User.users:
            User.users.remove(self)
        connection.commit()
        connection.close()


    """
    Removes user from the registry, if they are in it 
    """
    def remove_user_from_registry(self):
        if self in User.users:
            User.users.remove(self)


    """
    Updates a user in the SQL database so they are up to date with their information in the code
    """
    def update_user(self):
        self.remove_user()
        self.write_user()


    """
    Ovverride of the string method of the object
    """
    def __str__(self):
        return "ID: "+str(self.id)+"\nUsername: "+self.username+"\nPassword Hash: " + (self.password_hash[0:3] + "*" * (len(self.password_hash) -3))

    """
    Finds user in the registry by their id
    """
    @staticmethod
    def find_user_in_registry(id):
        for i in User.users:
            if i.id == id:
                return i
        return None


    """
    Verifies that a password is not too long, too short, or contains any disallowed characters
    """
    @staticmethod
    def is_valid_password(p):
        if len(p) > 40:
            return "LENGTH_EXCEEDS"
        elif len(p) < 8:
            return "LENGTH_TOO_LOW"
        elif "--" in p:
            return "SQL_INJECTION"
        return "VALID"


    """
    Verifies that a username is not too long, too short, containing any disallowed characters, or a duplicate username
    """
    @staticmethod
    def is_valid_username(s):
        if len(s) > 20:
            return "LENGTH_EXCEEDS"
        elif len(s) < 3:
            return "LENGTH_TOO_LOW"
        elif User.find_user_by_name(s) != None:
            return "DUPLICATE"
        elif "--" in s:
            return "SQL_INJECTION"
        elif not s.isalnum():
            return "INVALID_CHARACTER"
        return "VALID"

    @staticmethod
    def find_user_by_name(s):
        connection = get_sql_connection(PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT id, password_hash FROM users WHERE username = \"{0}\"".format(s))
        data = cursor.fetchall()
        
        if len(data) > 1:
            send_error("DUPLICATE_USERNAMES", s)
            raise Exception("Fatal error. Contact a network administrator immediately")
        
        if len(data) == 0:
            return None
        
        connection.commit()
        connection.close()
        tmp = User.find_user_in_registry(data[0][0])
        if tmp != None:
            return tmp
        return User(s, data[0][1], data[0][0], True)
        
    @staticmethod
    def execute_sql_select(command):
        connection = get_sql_connection(PATH)
        cursor = connection.cursor()

        cursor.execute(command)
        data = cursor.fetchall()
        
        return data

#endregion

#region balancemanagement

#endregion