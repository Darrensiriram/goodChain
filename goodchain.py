import os
# os.system("pip install -r requirements.txt")
import sqlite3
from getpass import getpass
from actions.mining_actions import *
from database_actions import login
from database_actions import signup as s
from database_actions import connectionSQL as dbcreate

connection = sqlite3.Connection('database_actions/goodchain.db')
os.system("touch block.dat")

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
        response = int(input("What would u like to do? \n "))
        if response == 1:
            username = input("Fill in your username please: ")
            password = getpass("Please fill your password in: ")
            print("Please wait while we validate our chain")
            loginUser = login.login(connection, username, password)
            # sleep(5)
            # if loginUser.validateBlock() == True:
            #     print("chain has been verified")
            loginUser.loginUser()
        elif response == 2:
             mine_actions.explore_chain()
             sleep(2)
        elif response == 3:
            dbcreate.createDatabase(connection)
            username = input("Fill in your username please: ")
            password = getpass("Please fill your password in: ")
            coins = 50
            signupUser = s.signUp(connection=connection, username=username, password=password, coins=coins)
            s.signUp.signUpUser(signupUser)
        elif response == 4:
            exit("Thank you for using the goodchain")


startMenu()
