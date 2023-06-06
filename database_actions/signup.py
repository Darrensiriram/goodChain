import bcrypt
from blockchainActions.Signature import generate_keys
from network_actions import server


class signUp:
    def __init__(self, connection, username, password, coins):
        private_key, public_key = generate_keys()
        self.connection = connection
        self.username = username
        self.password = password
        self.coins = coins
        self.private_key = private_key.decode("UTF-8")
        self.public_key = public_key.decode("UTF-8")

    def signUpUser(self) -> None:
        cur = self.connection.cursor()
        username_exists_query = "SELECT COUNT(*) FROM users WHERE username = ?"
        cur.execute(username_exists_query, [self.username])
        result = cur.fetchone()
        if result[0] > 0:
            print("Username already exists. Please choose a different username.")
            return
        bytes = self.password.encode('UTF-8')
        salt = bcrypt.gensalt(12)
        hashed_pwd = bcrypt.hashpw(bytes, salt)
        query = "INSERT INTO users (username, password, coins, private_key, public_key) VALUES (?,?,?,?,?)"
        cur.execute(query, [self.username, hashed_pwd, self.coins, self.private_key, self.public_key])
        self.connection.commit()
        server.send_data("database")

    def sign_up_system_user(self):
        private_keyNew, public_keyNew = generate_keys()
        pvKey = private_keyNew.decode("UTF-8")
        pbKey = public_keyNew.decode("UTF-8")
        bytes = "test".encode('UTF-8')
        salt = bcrypt.gensalt(12)
        hashed_pwd = bcrypt.hashpw(bytes, salt)
        cur = self.connection.cursor()
        userFound = cur.execute('SELECT * FROM users where username = "system"').fetchone()
        if userFound is not None:
            return None
        else:
            cur.execute("INSERT INTO users (username, password, coins, private_key, public_key) VALUES (?,?,?,?,?)",
                        ['system', hashed_pwd, 0, pvKey, pbKey])
            self.connection.commit()
