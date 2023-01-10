import pickle

import utils.helper
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
        return str.encode(result[0])

    def calculate_the_balance_using_pool_income(self):
        alltx = get_all_transaction_in_the_pool()
        currentLoggedInPbcKey = self.get_user_pubc_key_by_id(self.authUser)
        currentbalance = 0
        for x in alltx:
           amount = x.outputs[0][1]
           pubcKey = x.outputs[0][0]
           if currentLoggedInPbcKey.decode('utf-8') == pubcKey.decode('utf-8'):
            currentbalance += amount
        return currentbalance

    def calculate_the_balance_using_pool_outcome(self):
        alltx = get_all_transaction_in_the_pool()
        pubc_key = self.get_user_pubc_key_by_id(self.authUser)
        currentbalance = 0
        for x in alltx:
            pubkey_x = x.inputs[0][0]
            if pubc_key.decode('utf-8') == pubkey_x.decode('utf-8'):
                outcome = x.inputs[0][1]
                currentbalance += outcome
        return currentbalance

    def total_balance_pool(self):
        outcome = self.calculate_the_balance_using_pool_outcome()
        income = self.calculate_the_balance_using_pool_income()
        balance = 50
        if income != outcome:
            return balance - outcome
        return None

    def calculate_the_balance_using_chain_outcome(self):
        allTx = get_all_tx_in_the_chain()
        if allTx is None:
            return "Chain is empty"
        else:
            pubc_key = self.get_user_pubc_key_by_id(self.authUser)
            balanceChain = 0
            for x in allTx[0]:
                pubc_keyX = x.inputs[0][0]
                if pubc_key.decode('UTF-8') == pubc_keyX.decode('utf-8'):
                    uitgave = x.inputs[0][1]
                    balanceChain += uitgave
            return balanceChain

    def calculate_the_balance_using_chain_income(self):
        alltx = get_all_tx_in_the_chain()
        if alltx is None:
            return "Chain is empty"
        else:
            pubc_key = self.get_user_pubc_key_by_id(self.authUser)
            balanceChain = 0
            for x in alltx:
                amount = x.outputs[0][1]
                pubcKey = x.outputs[0][0]
                if pubc_key.decode('utf-8') == pubcKey.decode('utf-8'):
                    balanceChain += amount
            return balanceChain

    def total_balance_chain(self):
        income = self.calculate_the_balance_using_chain_income()
        outcome = self.calculate_the_balance_using_chain_outcome()
        balance = 50
        if income != outcome:
            return (balance - outcome) + income
        return None
    def current_balance(self):
        if self.total_balance_pool() is not None and self.total_balance_chain() is not None:
            return self.total_balance_pool() + self.total_balance_chain()
        elif self.total_balance_pool() is not None:
            return self.total_balance_pool()
        elif self.total_balance_chain() is not None:
            return self.total_balance_chain()
        return 50
