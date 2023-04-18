import socket as sock
import os
import threading
import pickle

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
# localIP = sock.gethostbyaddr('192.168.2.41')[0]
# hostname = sock.gethostname()
localIP = sock.gethostbyname("localhost")
# print(f'Hostname: {hostname} on docker container')
port = 5068
ADDR = (localIP, port)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECTED_MESSAGE = "!DISCONNECTED"
TempPoolPath = 'goodchain/network_actions/tempFiles/temp_pool.dat'

def receiveTx(conn, addr):
    while True:
        data = conn.recv(4096)
        if not data:
            break
        try:
            msg = data.decode('utf-8')
            print(f'Received message from {addr}: {msg}')
        except UnicodeDecodeError:
            with conn:
                transaction = pickle.loads(data)
                print(f"Received transaction: {transaction}")
                with open('data/pool.dat', 'ab') as f:
                    pickle.dump(transaction, f)



def start_server():
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen()
        print(f'Server started and listening on {localIP}:{port}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected with {addr}')
            threading.Thread(target=receiveTx, args=(conn,addr)).start()

threading.Thread(target=start_server).start()