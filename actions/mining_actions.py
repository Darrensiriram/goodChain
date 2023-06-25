import pickle
import time
import collections
import blockchainActions.BlockChain
from blockchainActions.TxBlock import *
from blockchainActions.BlockChain import *
from actions.transferCoins import *
from utils import helper
import os

MIN_MINING_TIME = 30
MAX_MINING_TIME = 60
DIFFICULTY_LEVEL = 2
poolPath = 'data/pool.dat'
blockPath = 'data/block.dat'

class mine_actions:
    def __init__(self, transaction):
        self.transaction = transaction

    @staticmethod
    def create_block(transaction: list, prevBlock: list = []):
        global root
        if not os.path.isfile(blockPath):
            root = TxBlock(None)
            i = 0
            while i <= 5:
                root.addTx(transaction[i])
                i += 1
            mine_actions.save_to_chain(root)
        else:
            B = TxBlock(prevBlock)
            i = 0
            while i <= 5:
                B.addTx(transaction[i])
                i += 1
            mine_actions.save_to_chain(B)

    @staticmethod
    def save_to_chain(block):
        savefile = open(blockPath, "ab+")
        pickle.dump(block, savefile)
        savefile.close()

    @staticmethod
    def get_block_chain():
        blockchain = []
        with open(blockPath, "rb") as f:
            try:
                while True:
                    blockchain.append(pickle.load(f))
            except EOFError:
                pass
        return blockchain

    @staticmethod
    def explore_chain():
        blockchain = helper.retrieve_blocks()
        if len(blockchain) == 0:
           return print("The chain is empty")

        i = 0
        genesis = lambda x: 'Genesis' if (i == 0) else x
        for x in blockchain:
            print("-----------------------------------------------------------------")
            print(f"                        block: {genesis(i)}                     ")
            print("-----------------------------------------------------------------")
            print(f"Transaction {x.data}                                            ")
            print("-----------------------------------------------------------------")
            i += 1

    @staticmethod
    def load_all_transaction_per_block():
        all_transactions_in_the_pool = transfer_coins.get_transactions_in_pool()
        temp = []
        transactionBlock = [[]]
        mintx = 5
        totaltx = len(all_transactions_in_the_pool) // mintx

        i = 0
        count = 0
        while i < totaltx:
            j = 0
            while j < mintx:
                temp.append(all_transactions_in_the_pool[count])
                count += 1
                j += 1
            transactionBlock.append([temp])
            temp = []
            i += 1
        for x in transactionBlock:
            if x == []:
                transactionBlock.remove(x)
        return transactionBlock

    def mine_block(block, index):
        prevblock = blockchainActions.BlockChain.CBlock.get_prev_block()
        txBlock = TxBlock(prevblock)

        for x in block[index]:
            for y in x:
                txBlock.addTx(y)
                if txBlock.is_valid():
                    mine_actions.mine_timer(txBlock)
        mine_actions.save_to_chain(txBlock)
        helper.fixTampering()

    def mine_timer(txblock):
        start = time.time()
        print("Mining block...")
        if txblock.mine(leading_zeros = DIFFICULTY_LEVEL):
            if time.time() - start < 10:
                sleep(10 - int(time.time() - start < 10))
            print("Success! Mining was successful!")
        else:
            print("ERROR! Mining was not sucessful!")

        elapsed = time.time() - start

        print("elapsed time: " + str(elapsed) + " s.")
        if elapsed < MIN_MINING_TIME:
            print("Alarm! Mining is too fast")
        elif elapsed > MAX_MINING_TIME:
            print("Alarm! Mining is too Slow")

    @staticmethod
    def clear_transaction_after_mining(blockchain):
        for x in blockchain:
            transfer_coins.delete_transaction_in_pool(x)