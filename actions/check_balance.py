import pickle
from utils.helper import *
import sqlite3
poolPath = 'data/pool.dat'
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

    def get_current_username(self, userId):
        cur = self.connection.cursor()
        result = cur.execute('SELECT username FROM users WHERE id = ?', (userId,)).fetchone()
        if result is None:
            return None
        return result
    def get_current_balance_in_pool(self):
        allTx = []
        with open(poolPath, "rb+") as f:
            try:
                while True:
                    allTx.append(pickle.load(f))
            except EOFError:
                pass

        new_balance = 0
        startingBalance = self.get_current_balance()[0]
        for x in allTx:
            if x.userId[0] == self.authUser:
                amount_from_transaction = x.outputs[0][1]
                new_balance += amount_from_transaction
        return new_balance + startingBalance


    def get_user_pubc_key_by_id(self,userId):
        cur = self.connection.cursor()
        result = cur.execute('SELECT public_key FROM users WHERE id = ?', (userId,)).fetchone()
        if result is None:
            return None
        return result[0]



    def subtract_of_balance_when_transaction_made(self):
        alltx = get_all_transaction_in_the_pool()
        pubc_key = self.get_user_pubc_key_by_id(self.authUser)
        for x in alltx:
            amount = x.inputs[0][1]
            print(x.inputs[0][0][0])

        #TODO: checken in de pool welke transacties er zijn, dan kijken of het Pubc key in de db bestaat, zo ja dan moet je zijn balance updaten.