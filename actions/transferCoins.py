from cryptography.hazmat.primitives.serialization import load_pem_private_key
from blockchainActions.Transaction import *
class transfercoins:

    def __init__(self, connection, auth_user, chosen_user, amount, transactionfee):
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
        return Tx1.is_valid()

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