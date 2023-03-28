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
# localIP = sock.gethostbyaddr('192.168.2.31')[0]
localIP = sock.gethostbyname("localhost")
port = 5068
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


def start_client():
    socket.connect(ADDR)
    print(f'Made a connection with the server {localIP}:{port}...')
    data = socket.recv(1024)
    msg = data.decode(FORMAT)
    print(f'Received response from server: {msg}')

    response = 'Message received'
    socket.sendall(response.encode(FORMAT))




def startMenu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        helper.broadcast("Dit is een test bericht", localIP, port)
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
