import pickle

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from blockchainActions.Transaction import *


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
        savefile = open("pool.dat", "ab")
        pickle.dump(transaction, savefile)
        savefile.close()

    @staticmethod
    def verify_transaction_in_the_pool(savefile):
        loadfile = open("pool.dat", "rb")
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
        current_user_pk_key, current_user_pbc_key = self.get_key_credentials_current_user()
        # print(current_user_pbc_key)
        with open("pool.dat", "rb") as file:
            try:
                while True:
                    loadPickle = pickle.load(file)
                    trans.append(loadPickle)
                    trans.append(counterPool)
            except EOFError:
                pass

        for item in trans:
            pbc_key_from_file = item.inputs[0][0]
            print(pbc_key_from_file)

        # print(trans)
