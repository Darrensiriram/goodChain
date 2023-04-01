import socket as sock
import threading

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
# localIP = sock.gethostbyaddr('192.168.2.41')[0]
hostname = sock.gethostname()
localIP = sock.gethostbyname(hostname)
print(f'Hostname: {hostname} on docker container')
port = 5068
ADDR = (localIP, port)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECTED_MESSAGE = "!DISCONNECTED"



def handle_client(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = data.decode('utf-8')
        print(f'Received message from {addr}: {msg}')
    print(f'Connection with {addr} closed.')



def start_server():
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen()
        print(f'Server started and listening on {localIP}:{port}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected with {addr}')
            threading.Thread(target=handle_client, args=(conn, addr)).start()



threading.Thread(target=start_server).start()