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
            for output in x.outputs:
                pubcKey = output[0]
                amount = output[1]
                if currentLoggedInPbcKey.decode('utf-8') == pubcKey.decode('utf-8'):
                    currentbalance += amount
        return currentbalance

    def calculate_the_balance_using_pool_outcome(self):
        alltx = get_all_transaction_in_the_pool()
        pubc_key = self.get_user_pubc_key_by_id(self.authUser)
        currentbalance = 0
        for x in alltx:
            for input in x.inputs:
                pubkey_x = input[0]
                outcome = input[1]
                if pubc_key.decode('utf-8') == pubkey_x.decode('utf-8'):
                    currentbalance += outcome
        return currentbalance

    def total_balance_pool(self):
        outcome = self.calculate_the_balance_using_pool_outcome()
        income = self.calculate_the_balance_using_pool_income()
        if income != outcome:
            return income - outcome
        return 0

    def calculate_the_balance_using_chain_outcome(self):
        allTx = retrieve_blocks()
        if allTx is None:
            return "Chain is empty"
        pubc_key = self.get_user_pubc_key_by_id(self.authUser)
        balanceChain = 0
        for block in allTx:
            for transaction in block.data:
                for input in transaction.inputs:
                    pubc_keyX = input[0]
                    uitgave = input[1]
                    if pubc_key.decode('utf-8') == pubc_keyX.decode('utf-8'):
                        balanceChain += uitgave
        return balanceChain

    def calculate_the_balance_using_chain_income(self):
        alltx = retrieve_blocks()
        if alltx is None:
            return "Chain is empty"
        pubc_key = self.get_user_pubc_key_by_id(self.authUser)
        balanceChain = 0
        for block in alltx:
            for transaction in block.data:
                for output in transaction.outputs:
                    pubcKey = output[0]
                    amount = output[1]
                    if pubc_key.decode('utf-8') == pubcKey.decode('utf-8'):
                        balanceChain += amount
        return balanceChain

    def total_balance_chain(self):
        income = self.calculate_the_balance_using_chain_income()
        outcome = self.calculate_the_balance_using_chain_outcome()
        if income != outcome:
            return income - outcome
        return 0

    def current_balance(self):
        total_pool_balance = self.total_balance_pool()
        total_chain_balance = self.total_balance_chain()
        return 50 + total_pool_balance + total_chain_balance