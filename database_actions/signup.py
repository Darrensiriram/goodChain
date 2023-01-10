import bcrypt
from blockchainActions.Signature import generate_keys


class signUp:
    def __init__(self, connection, username, password, coins):
        private_key, public_key = generate_keys()
        self.connection = connection
        self.username = username
        self.password = password
        self.coins = coins
        self.private_key = private_key.decode("UTF-8")
        self.public_key = public_key.decode("UTF-8")

    def signUpUser(self)-> None:
        bytes = self.password.encode('UTF-8')
        salt = bcrypt.gensalt(12)
        hashed_pwd = bcrypt.hashpw(bytes, salt)
        cur = self.connection.cursor()
        cur.execute("INSERT INTO users (username, password, coins, private_key, public_key) VALUES (?,?,?,?,?)", [self.username, hashed_pwd, self.coins, self.private_key, self.public_key])
        self.connection.commit()

    #TODO: Add a function to signup an "system user" with standard private_key and public_key

    def sign_up_system_user(self):
        bytes = "test".encode('UTF-8')
        salt = bcrypt.gensalt(12)
        hashed_pwd = bcrypt.hashpw(bytes, salt)
        cur = self.connection.cursor()
        cur.execute("INSERT INTO users (username, password, coins, private_key, public_key) VALUES (?,?,?,?,?)", ['system_user', hashed_pwd, self.coins, self.private_key, self.public_key])
        self.connection.commit() 