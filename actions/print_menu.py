import pickle

from actions import check_balance
from actions import transferCoins
from database_actions import login
import os
from time import sleep


def print_menu_loggedIn(auth_user, connection):
    cur = connection.cursor()
    result = cur.execute('SELECT username FROM users WHERE id = ?', (auth_user,)).fetchone()
    print(f"Username: {result[0]}")
    print("""
    1 - Transfer Coins
    2 - Check the Balance
    3 - Explore the Chain
    4 - Check the Pool 
    5 - Mine a Block
    6 - Log out
    """)


def actions(auth_user, connection):
    while True:
        print_menu_loggedIn(auth_user, connection)
        response = int(input("What would u like to do? \n"))
        if response == 1:
            chosen_user = input("please enter the username: ")
            amount = int(input("please specify the coin amount: "))
            transactionfee = int(input("please enter a transaction fee: "))
            transferCoinsobject = transferCoins.transfercoins(connection, auth_user, chosen_user, amount,
                                                              transactionfee)
            tx = transferCoinsobject.createTx(amount, transactionfee)
            transferCoinsobject.save_transaction_in_the_pool(tx)
            print("Coins have been transferred")
            continue
        elif response == 2:
            balanceObject = check_balance.balance(connection, auth_user)
            currentBalance = balanceObject.get_current_balance()[0]
            print(f"Current coins: {currentBalance}")
            sleep(2)
            break
        elif response == 3:
            print("Explore the chain")
            continue
        elif response == 4:
            pool = []
            loadfile = open("pool.dat", "rb")
            try:
                while True:
                    data = pickle.load(loadfile)
                    pool.append(data)
            except EOFError:
                pass
            print(pool)
            sleep(4)
        # elif response == 5:
        #     print("Cancel a transaction")
        #     tcObject = transferCoins.transfercoins(connection, auth_user)
        #     transferCoins.transfercoins.cancel_transaction_in_the_pool(tcObject)
        #     break
        elif response == 5:
            print("Mine a block")
            continue
        elif response == 6:
            print("Log out")
            break
