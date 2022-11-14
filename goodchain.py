import sqlite3
from getpass import getpass
from database_actions import login
from database_actions import signup as s
from database_actions import connectionSQL as dbcreate


connection = sqlite3.Connection('database_actions/goodchain.db')

def print_public_menu():
    print("""
    Public Menu
    Menu for sign up in Goodchain

    1 - Login
    2 - Explore the blockchain
    3 - Sign up
    4 - Exit
    """)

# def switchCase(response):
#     if response == 1:
#        username = input("Fill in your username please: ")
#        password = getpass("Please fill your password in: ")
#        loginUser = login.login(connection, username, password)
#        loginUser.loginUser()
#     elif response == 2:
#         print("Exploring the blockchain")
#     elif response == 3:
#         dbcreate.createDatabase(connection)
#         username = input("Fill in your username please: ")
#         password = getpass("Please fill your password in: ")
#         coins = 50
#         signupUser = s.signUp(connection=connection,username=username, password=password, coins=coins)
#         s.signUp.signUpUser(signupUser)
#     elif response == 4:
#         exit("Thank you for using the goodchain")


while True:
    print_public_menu()
    response = int(input("What would u like to do? \n "))
    if response == 1:
        username = input("Fill in your username please: ")
        password = getpass("Please fill your password in: ")
        loginUser = login.login(connection, username, password)
        loginUser.loginUser()
        break
    elif response == 2:
        print("Exploring the blockchain")
        break
    elif response == 3:
        dbcreate.createDatabase(connection)
        username = input("Fill in your username please: ")
        password = getpass("Please fill your password in: ")
        coins = 50
        signupUser = s.signUp(connection=connection, username=username, password=password, coins=coins)
        s.signUp.signUpUser(signupUser)
    elif response == 4:
        exit("Thank you for using the goodchain")
