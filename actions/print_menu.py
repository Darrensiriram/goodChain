from actions import check_balance

def print_menu_loggedIn(auth_user, connection):
    cur = connection.cursor()
    result = cur.execute('SELECT username FROM users WHERE id = ?', (auth_user,)).fetchone()
    print(f"Username: {result[0]}")
    print("""
    1 - Transfer Coins
    2 - Check the Balance
    3 - Explore the Chain
    4 - Check the Pool 
    5 - Cancel a transaction
    6 - Mine a Block
    7 - Log out
    """)


def actions(auth_user, connection):
    print_menu_loggedIn(auth_user, connection)
    response = int(input("What would u like to do? \n"))
    while True:
        if response == 1:
            print("Transfer my coins asah!")
            continue
        elif response == 2:
            balanceObject = check_balance.balance(connection, auth_user)
            currentBalance = balanceObject.get_current_balance()[0]
            print(f"Current coins: {currentBalance}")
            break
        elif response == 3:
            print("Explore the chain")
            continue
        elif response == 4:
            print("Check the pool")
            continue
        elif response == 5:
            print("Cancel a transaction")
            continue
        elif response == 6:
            print("Mine a block")
            continue
        elif response == 7:
            print("Log out")
            continue
