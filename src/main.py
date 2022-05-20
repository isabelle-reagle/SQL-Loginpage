import sqlite3

PATH = "rentalDB.db"


def get_sql_connection(path):
    return sqlite3.connect(path)


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
sends a vital error to me
"""


def send_error(message, *argv):
    pass


"""
A hash function of password
"""


def hash(s):
    return s


class User:
    users = []

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = hash(password)

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

        cursor.execute("SELECT id FROM users WHERE id = {0}".format(self.id))

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
        """
        Ensure that no SQL injection is attempted
        """
        if "--" in self.username or "--" in self.password_hash:
            print("SQL INJECTION ATTEMPT")
            return 2
        """
        Do not add User to the database if they are already present
        """
        if self.user_in_database():
            print("User already in database.")
            return 1

        connection = get_sql_connection(PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users VALUES({0}, \"{1}\", \"{2}\");".format(
            self.id, self.username, self.password_hash))

        connection.commit()
        connection.close()

        return 0

    """
    Removes a User from the platform
    Includes removal from the registry and database
    """

    def remove_user(self):
        connection = get_sql_connection(PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM users WHERE id = {0}".format(self.id))
        User.users.remove(self)
        connection.commit()
        connection.close()

    """
    Updates a user in the SQL database so they are up to date with their information in the code
    """

    def update_user(self):
        self.remove_user()
        self.write_user()

    def __str__(self):
        return "ID: "+str(self.id)+"\nUsername: "+self.username+"\nPassword: " + ("*" * len(self.password))

    def generate_id(self):
        pass

    """
    Finds user in the registry by their id
    """
    @staticmethod
    def find_user_in_registry(id):
        for i in User.users:
            if i.id == id:
                return i
        return None


a = User(101, "a", "1")
b = User(102, "b", "2")
c = User(103, "c", "3")
d = User(104, "d", "4")
