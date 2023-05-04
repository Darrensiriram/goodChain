import pickle
import sqlite3
import hashlib
import os
#connection = sqlite3.Connection('database_actions/goodchain.db')
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

def get_user_name_by_pub_key(con, pbcKey=''):
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
    if len(allTx) == 0:
        return None
    else:
        return allTx[0]

# fix that is also works on windowss
def create_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    hash_value = sha256.hexdigest()
    backup_directory = os.path.join(".", "backup")
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
    backup_file = os.path.join(backup_directory, "backup.txt")
    with open(backup_file, "w") as f:
        f.write(hash_value)
    return hash_value

def compare_hashes(file_path):
    backup_directory = os.path.join(".", "backup")
    backup_file = os.path.join(backup_directory, "backup.txt")
    if not os.path.exists(backup_file):
        return "No backup file found!"
    with open(backup_file, "r") as f:
        backup_hash = f.read()
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    current_hash = sha256.hexdigest()
    if validateBlock():
        print("The hash values match.")
        return True
    else:
        print("Tampering detected!")
        return False
    # if current_hash == backup_hash:
    #     print("The hash values match.")
    #     return True
    # else:
    #     print("Tampering detected!")
    #     # create_hash(file_path)
    #     return False


def retrieve_blocks():
    allblocks = []
    with open("data/block.dat", "rb") as f:
        try:
            while True:
                allblocks.append(pickle.load(f))
        except EOFError:
            pass
    return allblocks



def validateBlock():
    allblocks = retrieve_blocks()
    if len(allblocks) == 0:
        print("Chain is empty")
        return True
    for b in allblocks:
        if b.is_valid_chain():
            return True
        else:
            return False


# def broadcast(msg, localIP, port):
#     try:
#         s.getpeername()
#     except socket.error:
#         s.connect((localIP, port))
#     print(f'Broadcasting message all over the network: {msg} ')
#     s.sendall(msg.encode("UTF-8"))

# def update_file(current_file, new_file):
#     with open(new_file, 'rb') as f:
#         new_data = f.read()
#     with open(current_file, 'wb') as f:
#         f.write(new_data)
#     print(f'File {current_file} has been updated with data from {new_file}.')
#
#
# def broadcast_file(filename, localIP, port):
#     try:
#         s.getpeername()
#         print("Socket is already connected")
#     except socket.error:
#         s.connect((localIP, port))
#
#     with open(filename, 'rb') as f:
#         filedata = f.read()
#     pickled_data = pickle.dumps(filedata)
#     print(f"File broadcasted all over the network: {filename}")
#     s.sendall(pickled_data)
#     print("File sent successfully")
