from blockchainActions.BlockChain import CBlock
from blockchainActions.Signature import generate_keys, sign, verify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import random

REWARD_VALUE = 25.0
leading_zeros = 2
next_char_limit = 20


class TxBlock(CBlock):

    def __init__(self, previousBlock):
        self.nonce = "A random nonce"
        super(TxBlock, self).__init__([], previousBlock)

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def __count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr, amt in tx.inputs:
                total_in = total_in + amt
            for addr, amt in tx.outputs:
                total_out = total_out + amt
        return total_in, total_out

    def is_valid(self):
        if super(TxBlock, self).is_valid_chain():
            return False
        for tx in self.data:
            if tx.is_valid():
                print("Invalid transaction found in block")
                return False

        total_in, total_out = self.__count_totals()

        Tx_Balance = round(total_out - total_in, 10)
        print(f'csdsaghdbahsjbdsjalbdsajlbdashjbdsahdbshabdsahdjsabdsajhbdashdjbashjdbasjh')
        if Tx_Balance > REWARD_VALUE:
            return False
        return True

    # ----------------------------------
    def mine(self, leading_zeros):

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))

        found = False
        nonce = 0
        while not found:
            # print(nonce, end='\r')
            digest_temp = digest.copy()
            digest_temp.update(bytes(str(nonce), 'utf8'))
            hash = digest_temp.finalize()
            # print(hash)
            zeros = bytes('0' * leading_zeros, 'utf8')
            if hash[:leading_zeros] == zeros:
                found = True
                self.nonce = nonce
            nonce += 1
            del digest_temp
            print(f'trying nonce: {nonce}', end='\r')

        self.blockHash = self.computeHash()
        print('\n')

        return True

