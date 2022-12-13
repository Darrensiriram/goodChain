class balance:

    def __init__(self, connection, auth):
        self.connection = connection
        self.authUser = auth

    def get_current_balance(self):
        cur = self.connection.cursor()
        return cur.execute('SELECT coins FROM users where id = ?', (self.authUser,)).fetchone()

    def update_balance(self):
        cur = self.connection.cursor()
        cur.execute('UPDATE users SET coins = coins + 50 where id = ?', (self.authUser,))
        self.connection.commit()

    def get_current_balance_from_user(self, username):
        cur = self.connection.cursor()
        result = cur.execute('SELECT coins FROM users where username = ?', (username,)).fetchone()
        if result is None:
            return False
        else:
            return result
