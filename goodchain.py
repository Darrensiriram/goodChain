import os
import platform
# os.system("pip install -r requirements.txt")
import sqlite3
from getpass import getpass
from actions.mining_actions import *
from database_actions import login
from database_actions import signup as s
from database_actions import connectionSQL as dbcreate
import pathlib
connection = sqlite3.Connection('database_actions/goodchain.db')


if platform.system() == 'Darwin':
    if os.path.exists('data'):
        os.system("touch data/block.dat")
        os.system("touch data/pool.dat")
    else:
        os.mkdir('data')
else:
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

def startMenu():
    while True:
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
        elif int(response) == 4:
            exit("Thank you for using the goodchain")


startMenu()
