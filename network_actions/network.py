import socket
import threading
import pickle

class Network:
    def __init__(self):
        self.ip = socket.gethostbyname("localhost") #TODO change to public ip
        self.port = 5068
        self.transaction_pool = []

        self.listener_thread = threading.Thread(target=self.listen_for_transactions)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def send_transaction(self, transaction):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            serialized_transaction = pickle.dumps(transaction)
            s.sendall(serialized_transaction)

    def listen_for_transactions(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    transaction = pickle.loads(data)
                    with open('data/pool.dat', 'ab') as f:
                        pickle.dump(transaction, f)
                        self.transaction_pool.append(transaction)

    def load_transactions(self):
        with open('data/pool.dat', 'rb') as f:
            while True:
                try:
                    transaction = pickle.load(f)
                    self.transaction_pool.append(transaction)
                except EOFError:
                    break

    def save_transactions(self):
        with open('data/pool.dat', 'ab') as f:
            for transaction in self.transaction_pool:
                pickle.dump(transaction, f)
