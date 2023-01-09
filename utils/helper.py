import pickle
import sqlite3
connection = sqlite3.Connection('database_actions/goodchain.db')
def pluckStr(result: list, key):
    if key in result:
        return key
    else:
        return None

def get_all_transaction_in_the_pool():
    allTx = []
    with open('data/pool.dat', "rb+") as f:
        try:
            while True:
                allTx.append(pickle.load(f))
        except EOFError:
            pass
    return allTx

def get_user_name_by_pub_key(con=connection, pbcKey=''):
    cur = con.cursor()
    result = cur.execute('SELECT username FROM users WHERE public_key = ?', (pbcKey,)).fetchone()
    if result is None:
        return None
    return result[0]


def get_all_tx_in_the_chain():
    allTx = []
    with open('data/block.dat', "rb+") as f:
        try:
            while True:
                allTx.append(pickle.load(f))
        except EOFError:
            pass
    return allTx[0]
