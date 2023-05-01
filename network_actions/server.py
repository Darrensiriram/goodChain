import socket as sock
import sqlite3
import threading
import pickle
from importlib import import_module

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
localIP = sock.gethostbyname("192.168.68.130")
port = 5068
ADDR = (localIP, port)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECTED_MESSAGE = "!DISCONNECTED"

def receiveTx(conn, addr):
    my_module = import_module("actions.transferCoins")
    data = conn.recv(8096)
    unloaded_data = pickle.loads(data)
    if unloaded_data["Type"] == "Transaction":
        txInputs = unloaded_data["inputs"][0][1]
        txSender = unloaded_data["inputs"][0][0]
        txSigs = unloaded_data["signatures"][0]
        txOutputs = unloaded_data["outputs"][0][1]
        txReceiver = unloaded_data["outputs"][0][0]
        txStatus = unloaded_data["status"][0]
        txId = unloaded_data["txId"]
        auth_user = unloaded_data["auth_user"]
        print(
            f"inputs: {txInputs} \nSender: {txSender} \nsigs: {txSigs} \nReceiver: {txReceiver} \noutputs: {txOutputs} \nstatus: {txStatus} \ntxId: {txId} \nauth_user: {auth_user} \n ")
        transaction = my_module.transfer_coins.createTxNetwork(txSender, txReceiver, txSigs, txInputs, txOutputs,auth_user)
        print(transaction)

def send_transaction(transaction, auth_user):
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.connect((localIP, port))
        tx_dict = {
            "Type": "Transaction",
            "inputs": transaction.inputs,
            "signatures": transaction.sigs,
            "outputs": transaction.outputs,
            "status": transaction.status,
            "txId": transaction.txid,
            "auth_user": auth_user,
        }
        s.sendall(pickle.dumps(tx_dict))
        print("Message will be sent")
        s.close()


def send_block(block):
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.connect((localIP, port))
        block_dict = {
            "Type": "Block",
            "block": block
        }
        s.sendall(pickle.dumps(block_dict))
        print("Message will be sent")
        s.close()


def start_server():
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen()
        print(f'Server started and listening on {localIP}:{port}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected with {addr}')
            threading.Thread(target=receiveTx, args=(conn, addr)).start()


threading.Thread(target=start_server).start()