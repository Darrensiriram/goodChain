import pickle
from time import sleep
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from blockchainActions.Transaction import *

poolPath = 'data/pool.dat'

class transfercoins:

    def __init__(self, connection, auth_user, chosen_user="", amount=0, transactionfee=0):
        self.connection = connection
        self.auth_user = auth_user
        self.chosen_user = chosen_user
        self.amount = amount
        self.transactionfee = transactionfee

    def createTx(self, amount, transactionfee):
        Tx1 = Tx()
        sender_user_pk_key, sender_user_pbc_key = self.get_key_credentials_current_user()
        receiver_user_pk_key, receiver_user_pbc_key = self.get_key_credentials_selected_user()
        Tx1.add_input(sender_user_pbc_key, amount)
        Tx1.add_output(receiver_user_pbc_key, amount - transactionfee)
        Tx1.sign(sender_user_pk_key)
        if Tx1.is_valid():
            Tx1.add_status("Valid")
        else:
            Tx1.add_status("Invalid")
        return Tx1

    def get_key_credentials_current_user(self):
        cur = self.connection.cursor()
        result = cur.execute('SELECT private_key , public_key from users where id = ?', (self.auth_user,))
        for x in result:
            privatekey = x[0]
            publickey = x[1]
        encoded_pk = privatekey.encode('UTF-8')
        encoded_pbKey = publickey.encode('UTF-8')
        deserializedkey = load_pem_private_key(encoded_pk, password=None)
        return deserializedkey, encoded_pbKey

    def get_key_credentials_selected_user(self):
        cur = self.connection.cursor()
        result = cur.execute('SELECT private_key , public_key from users where username = ?', (self.chosen_user,))
        for x in result:
            private_key = x[0]
            public_key = x[1]
        encoded_pk = private_key.encode('UTF-8')
        encoded_pbKey = public_key.encode('UTF-8')
        deserializedkey = load_pem_private_key(encoded_pk, password=None)
        return deserializedkey, encoded_pbKey

    @staticmethod
    def save_transaction_in_the_pool(transaction):
        savefile = open(poolPath, "ab")
        pickle.dump(transaction, savefile)
        savefile.close()

    @staticmethod
    def verify_transaction_in_the_pool(savefile):
        loadfile = open(poolPath, "rb")
        new_tx = pickle.load(loadfile)

        if new_tx.is_valid:
            status = True
            print("Success! Loaded tx is valid")
        else:
            status = False
            print("Fail!")
        loadfile.close()
        return status

    def cancel_transaction_in_the_pool(self):
        trans = []
        with open(poolPath, "rb") as file:
            try:
                while True:
                    trans.append(pickle.load(file))
            except EOFError:
                pass
        #fill the list for editing
        counter = 0
        for i in trans:
          print(f"TRANSACTION: {counter}")
          print(i)
          counter += 1
        sleep(2)
        while True:
            chosenT = int(input("Please choose which transaction u which to delete from the pool:  "))
            if chosenT < len(trans):
                trans.pop(chosenT)
                break
            else:
                print("Option is invalid")
                continue

        f1 = open(poolPath, 'rb+')
        f1.seek(0)
        f1.truncate()

        #updating the pool.dat file
        for z in trans:
            savefile = open(poolPath, "ab+")
            pickle.dump(z, savefile)


    @staticmethod
    def get_total_transaction_in_pool():
        alltrans = []
        with open(poolPath, "rb") as f:
            try:
                while True:
                    alltrans.append(pickle.load(f))
            except EOFError:
                pass
        return len(alltrans)

    @staticmethod
    def get_transactions_in_pool():
        alltrans = []
        with open(poolPath, "rb") as f:
            try:
                while True:
                    alltrans.append(pickle.load(f))
            except EOFError:
                pass
        return alltrans