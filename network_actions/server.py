import socket as sock
import threading
import pickle
from utils import helper

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
server_ip = sock.gethostbyname("192.168.68.132")
client_ip = sock.gethostbyname("192.168.68.134")
port = 5068
ADDR = (server_ip, port)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECTED_MESSAGE = "!DISCONNECTED"

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
                transactions = data_dict.get('Data')
                with open('data/pool.dat', 'wb') as f:
                    f.write(transactions)
                print("Checking if transactions are valid...")
                helper.check_transaction_validity()
                print("Transaction pool received and written to disk.")
            elif data_dict.get('Type') == 'block':
                # Load the received block data as a Python object
                blocks = pickle.loads(data_dict.get('Data'))
                for block in blocks:
                    block.validate_block()
                    print(f"Block {block.blockId} is {'valid' if block.valid else 'not valid'}")
                # Save the validated blocks to disk
                with open('data/block.dat', 'wb') as f:
                    pickle.dump(blocks, f)
                print("Block file received and validated, and written to disk.")
                helper.fixTampering()
            elif data_dict.get('Type') == 'database':
                database_data = data_dict.get('Data')
                with open('database_actions/goodchain.db', 'wb') as f:
                    f.write(database_data)
                print("Database file received and overwritten.")
            else:
                print("Unknown data type received.")
        else:
            print("Unknown data received.")
    except pickle.UnpicklingError as e:
        print(f"Error unpickling data: {e}")
    conn.close()


def send_data(data_type):
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.connect((client_ip, port))
        if data_type == 'pool':
            with open('data/pool.dat', 'rb') as f:
                data = f.read()
                chunk_size = 65535
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i+chunk_size]
                    s.sendall(pickle.dumps({'Type': 'pool', 'Data': chunk}))
                print("Transaction pool sent.")
        elif data_type == 'block':
            with open('data/block.dat', 'rb') as f:
                data = f.read()
                chunk_size = 65535
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i+chunk_size]
                    s.sendall(pickle.dumps({'Type': 'block', 'Data': chunk}))
                print("Block file sent.")
        elif data_type == 'database':
            with open('database_actions/goodchain.db', 'rb') as f:
                data = f.read()
                s.sendall(pickle.dumps({'Type': 'database', 'Data': data}))
                print("Database file sent.")
        s.close()


def start_server():
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen()
        print(f'Server started and listening on {server_ip}:{port}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected with {addr}')
            threading.Thread(target=receive, args=(conn,addr)).start()


threading.Thread(target=start_server).start()