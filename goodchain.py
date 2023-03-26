import os
import subprocess as sp
import socket as sock
import threading
import platform
# os.system("pip install -r requirements.txt")
import sqlite3
from getpass import getpass
import threading
from actions.mining_actions import *
from database_actions import login
from database_actions import signup as s
from database_actions import connectionSQL as dbcreate
import pathlib
from utils import helper

connection = sqlite3.Connection('database_actions/goodchain.db')

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
localIP = sock.gethostbyname("localhost")
port = 5067
ADDR = (localIP, port)
FORMAT = 'utf-8'
HEADER = 64
DISCONNECTED_MESSAGE = "!DISCONNECTED"


if platform.system() == 'Darwin':
    if os.path.exists('data'):
        os.system("touch data/block.dat")
        os.system("touch data/pool.dat")
    else:
        os.mkdir('data')
else:
    pathlib.Path('data').mkdir(parents=True, exist_ok=True)
    pathlib.Path('data/block.dat').touch()
    pathlib.Path('data/pool.dat').touch()

choiceList = ("1", "2", "3", '4')
def print_public_menu():
    print("""
    Public Menu 
    Menu for sign up in Goodchain

    1 - Login
    2 - Explore the blockchain
    3 - Sign up
    4 - Exit
    """)



def handle_client(conn, addr):
    # Handle incoming messages from the client
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = data.decode('utf-8')
        print(f'Received message from {addr}: {msg}')

    conn.close()
    print(f'Connection with {addr} closed.')

def start_server():
    # Start the server and listen for incoming connections
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.bind(ADDR)
        s.listen()
        print(f'Server started and listening on {localIP}:{port}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected with {addr}')
            threading.Thread(target=handle_client, args=(conn, addr)).start()


def start_client():
    # Start the client and connect to a remote server
    with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
        s.connect(ADDR)
        print(f'Connected to server on {localIP}:{port}...')

        # Send some messages to the server
        s.sendall('Hello, server!'.encode('utf-8'))
        s.sendall('How are you?'.encode('utf-8'))

        # Wait for the server to send a response
        data = s.recv(1024)
        msg = data.decode('utf-8')
        print(f'Received response from server: {msg}')




def startMenu():
    threading.Thread(target=start_server).start()
    threading.Thread(target=start_client).start()
    while True:
        sleep(5)
        os.system('cls' if os.name == 'nt' else 'clear')
        print_public_menu()
        response = input("What would u like to do? \n ")
        if response not in choiceList:
            print("Please select a valid option")
            sleep(2)
        elif int(response) == 1:
            username = input("Fill in your username please: ")
            password = getpass("Please fill your password in: ")
            loginUser = login.login(connection, username, password)
            loginUser.loginUser()
        elif int(response) == 2:
            mine_actions.explore_chain()
            sleep(2)
        elif int(response) == 3:
            dbcreate.createDatabase(connection)
            username = input("Fill in your username please: ")
            password = getpass("Please fill your password in: ")
            coins = 50
            signupUser = s.signUp(connection=connection, username=username, password=password, coins=coins)
            s.signUp.signUpUser(signupUser)
            signupUser.sign_up_system_user()
        elif int(response) == 4:
            exit("Thank you for using the goodchain")


if os.path.exists('backup'):
    pass
else:
    helper.create_hash('data/block.dat')

startMenu()
