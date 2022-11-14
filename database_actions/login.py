import bcrypt as b
from time import sleep
from actions.print_menu import *
auth_user = 0
class login:
    # auth_user = 0
    def __init__(self, connection, username, password):
        self.connection = connection
        self.username = username
        self.password = password

    def get_pwd_from_User(self, username):
        cur = self.connection.cursor()
        result = cur.execute('SELECT username,password FROM users WHERE username = ?', (username,)).fetchone()
        if result is None:
            return None
        return result

    def get_current_id(self, username):
        cur = self.connection.cursor()
        result = cur.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if result is None:
            return None
        return result

    def get_current_username(self):
        cur = self.connection.cursor()
        result = cur.execute('SELECT username FROM users WHERE id = ?', (auth_user)).fetchone()
        if result is None:
            return None
        return result

    def loginUser(self):
        global auth_user
        if self.get_pwd_from_User(self.username) is None:
            print("username is incorrect")
            sleep(2)
        else:
            current_password = self.get_pwd_from_User(self.username)[1]
            hashed_pwd = self.password.encode("UTF-8")
            if b.checkpw(hashed_pwd, current_password):
                auth_user = self.get_current_id(self.username)[0]
                actions(auth_user, self.connection)
            else:
                print("Password is incorrect")
                sleep(4)

