import socket
import threading

PORT = 5060
local_ip = socket.gethostbyname('localhost')
ADDR = (local_ip, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = "!DISCONNECTED"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    client_name = conn.recv(2048).decode(FORMAT)

    print(f"[NEW CONNECTION] {client_name}@{addr} is connected.")
    connection_message = f"...\nHi {client_name}! \nYour are successfully connected to the server"
    conn.send(connection_message.encode(FORMAT))
    connected = True
    while connected:
        msg_lenth = conn.recv(HEADER).decode(FORMAT)
        if msg_lenth:
            msg_lenth = int(msg_lenth)
            msg = conn.recv(msg_lenth).decode(FORMAT)
            if msg == DISCONNECTED_MESSAGE:
                connected = False
            print(f"[{client_name}]@[{addr}] {msg}")
            return_message = f'Server received your message: "{msg}"'
            conn.send(return_message.encode(FORMAT))

    bye_message = f"\nBye {client_name}!"
    conn.send(bye_message.encode(FORMAT))
    conn.close(f"\n[ACTIVE CONNECTION] {threading.active_count() - 2}")
    print()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {local_ip}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
