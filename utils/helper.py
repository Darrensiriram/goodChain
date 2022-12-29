import pickle

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
