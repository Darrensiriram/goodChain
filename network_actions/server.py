import socket as sock
import threading
import pickle

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
localIP = sock.gethostbyname(sock.gethostname())
port = 5069
ADDR = (localIP, port)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECTED_MESSAGE = "!DISCONNECTED"

transaction_pool = []



def receiveTx(conn, addr,Address):
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(Address)
        s.listen()
        print(f'Server started and listening on {localIP}:{port}...')
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096)
                transaction = pickle.loads(data)
                with open('data/pool.dat', 'ab') as f:
                    pickle.dump(transaction, f)
                    transaction_pool.append(transaction)
            print(transaction_pool)



def send_transaction(transaction):
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.connect((localIP, port))
        serialized_transaction = pickle.dumps(transaction)
        s.sendall(serialized_transaction)
        print("Message will be send")
        s.close()


def start_server():
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen()
        print(f'Server started and listening on {localIP}:{port}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected with {addr}')
            threading.Thread(target=receiveTx, args=(conn, addr, ADDR)).start()


threading.Thread(target=start_server).start()