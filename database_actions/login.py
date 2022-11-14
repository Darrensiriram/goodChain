from sqlite3 import Connection
import bcrypt as b
from time import sleep


class login:

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

    def loginUser(self):
        if self.get_pwd_from_User(self.username) is None:
            print("username is incorrect")
            sleep(2)
        else:
            current_password = self.get_pwd_from_User(self.username)[1]
            hashed_pwd = self.password.encode("UTF-8")
            if b.checkpw(hashed_pwd, current_password):
                #TODO: when logged in go the next menu.
                print("Jeejyh ur logged in")
            else:
                print("Password is incorrect")
                sleep(4)

