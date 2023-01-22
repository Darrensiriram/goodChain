import bcrypt as b
from time import sleep
from actions.print_menu import *
from datetime import datetime
import time
auth_user = 0


class login:
    # auth_user = 0
    def __init__(self, connection, username="", password=""):
        self.connection = connection
        self.username = username
        self.password = password



    @staticmethod
    def validateBlock():
        allblocks = []
        with open("block.dat", "rb") as f:
            try:
                while True:
                    allblocks.append(pickle.load(f))
            except EOFError:
                pass
        for b in allblocks[0]:
            if b.is_valid():
                return False
            else:
                return True


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

    def set_auth_user(self):
        global auth_user
        auth_user = 0

    def get_current_username(self):
        cur = self.connection.cursor()
        result = cur.execute('SELECT username FROM users WHERE id = ?', (auth_user)).fetchone()
        if result is None:
            return None
        return result

    def get_current_connected_count(self):
        cur = self.connection.cursor()
        result = cur.execute('SELECT connection_count FROM connectivity').fetchone()
        if result is None:
            return None
        return result

    def first_connection(self):
        cur = self.connection.cursor()
        cur.execute('INSERT INTO connectivity (connection_count) VALUES (1)')
        self.connection.commit()

    def update_current_connected_user(self):
        cur = self.connection.cursor()
        count = cur.execute('SELECT COUNT(*) FROM connectivity ').fetchone()
        if list(count)[0] == 0:
            self.first_connection()
        else:
            cur.execute('UPDATE connectivity SET connection_count = connection_count + 1 where id = 1 ')
            self.connection.commit()
            return "connection_count updated"


    def get_current_time(self):
        current_time = time.time()
        cur = self.connection.cursor()
        db_time = cur.execute('SELECT currentTime FROM connectivity ').fetchone()[0]
        if db_time is None:
            cur.execute('UPDATE connectivity SET currentTime = ? WHERE id = 1',[current_time])
            self.connection.commit()
            return False
        three_min = 180
        if current_time > (db_time + float(three_min)):
            return False
        return True

    def update_time_when_mine(self):
        cur = self.connection.cursor()
        current_time = time.time()
        cur.execute('UPDATE connectivity SET currentTime = ? WHERE id = 1', [current_time,])
        self.connection.commit()
    def set_default_value_connectivity(self):
        cur = self.connection.cursor()
        cur.execute('UPDATE connectivity SET connection_count = 0 where id = 1 ')
        self.connection.commit()
    def loginUser(self):
        self.update_current_connected_user()
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
                auth_user = 0
            else:
                print("Password is incorrect")
                sleep(4)
