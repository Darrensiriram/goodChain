
class balance:

    def __init__(self,connection, auth):
        self.connection = connection
        self.authUser = auth

    def get_current_balance(self):
        cur = self.connection.cursor()
        return cur.execute('SELECT coins FROM users where id = ?',(self.authUser,)).fetchone()



