import socket as sock
import sqlite3
import threading
import pickle
from importlib import import_module

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
localIP = sock.gethostbyname("192.168.2.44")
port = 5068
ADDR = (localIP, port)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECTED_MESSAGE = "!DISCONNECTED"

# def receiveTx(conn, addr):
#     with conn:
#         print("Receiving block file...")
#         data = conn.recv(8096)
#         block = pickle.loads(data)
#         with open('data/block.dat', 'wb') as f:
#             f.write(block)
#         print("Block file received and written to disk.")

def receive(conn, addr):
    buffer = b""
    while True:
        data = conn.recv(65535)
        if not data:
            break
        buffer += data

    try:
        data_dict = pickle.loads(buffer)
        if isinstance(data_dict, dict):
            if data_dict.get('Type') == 'pool':
                with open('data/pool.dat', 'wb') as f:
                    f.write(data_dict.get('Data'))
                print("Transaction pool received and written to disk.")

            elif data_dict.get('Type') == 'block':
                print(data_dict.get('Data'))
                with open('data/block.dat', 'wb') as f:
                    f.write(data_dict.get('Data'))
                print("Block file received and written to disk.")
            else:
                print("Unknown data type received.")
        else:
            print("Unknown data received.")
    except pickle.UnpicklingError as e:
        print(f"Error unpickling data: {e}")




def send_data(data_type):
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.connect((localIP, port))
        if data_type == 'pool':
            with open('data/pool.dat', 'rb') as f:
                data = f.read()
                s.sendall(pickle.dumps({'Type': 'pool', 'Data': data}))
                print("Transaction pool sent.")
        elif data_type == 'block':
            with open('data/block.dat', 'rb') as f:
                data = f.read()
                s.sendall(pickle.dumps({'Type': 'block', 'Data': data}))
                print("Block file sent.")
        s.close()



# def send_transaction(transaction, auth_user):
#     with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
#         s.connect((localIP, port))
#         tx_dict = {
#             "Type": "Transaction",
#             "inputs": transaction.inputs,
#             "signatures": transaction.sigs,
#             "outputs": transaction.outputs,
#             "status": transaction.status,
#             "txId": transaction.txid,
#             "auth_user": auth_user,
#         }
#         s.sendall(pickle.dumps(tx_dict))
#         print("Message will be sent")
#         s.close()


# def send_tx():
#     with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
#         s.connect((localIP, port))
#         with open('data/pool.dat', 'rb') as f:
#             data = f.read()
#             s.sendall(pickle.dumps(data))
#             print("Transaction file sent.")
#         s.close()
#
# def send_block():
#     with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
#         s.connect((localIP, port))
#         with open('data/block.dat', 'rb') as f:
#             data = f.read()
#             s.sendall(pickle.dumps(data))
#             print("Block file sent.")
#         s.close()

def start_server():
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen()
        print(f'Server started and listening on {localIP}:{port}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected with {addr}')
            threading.Thread(target=receive, args=(conn,addr)).start()


threading.Thread(target=start_server).start()