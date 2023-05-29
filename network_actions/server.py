import socket as sock
import threading
import pickle

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
server_ip = sock.gethostbyname("145.137.73.143")
client_ip = sock.gethostbyname("145.137.31.136")
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
                with open('data/pool.dat', 'wb') as f:
                    f.write(data_dict.get('Data'))
                print("Transaction pool received and written to disk.")

            elif data_dict.get('Type') == 'block':
                with open('data/block.dat', 'wb') as f:
                    f.write(data_dict.get('Data'))
                print("Block file received and written to disk.")
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