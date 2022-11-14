from sqlite3 import Connection
import bcrypt

class signUp:

    def __init__(self, connection, username, password, coins):
        self.connection = connection
        self.username = username
        self.password = password
        self.coins = coins

    def signUpUser(self)-> None:
        bytes = self.password.encode('UTF-8')
        salt = bcrypt.gensalt(12)
        hashed_pwd = bcrypt.hashpw(bytes, salt)
        cur = self.connection.cursor()
        cur.execute("INSERT INTO users (username, password, coins) VALUES (?,?,?)", [self.username, hashed_pwd, self.coins])
        self.connection.commit()
