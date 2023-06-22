from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from blockchainActions import Signature
import pickle
import uuid

blockPath = 'data/block.dat'


class CBlock:
    data = None
    previousHash = None
    previousBlock = None
    blockHash = None
    blockId = None
    valid = None
    signatures = []

    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        self.blockId = uuid.uuid1()
        if previousBlock is not None:
            self.previousHash = previousBlock.computeHash()
        self.blockHash = self.computeHash()

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        return digest.finalize()


    def is_valid_chain(self):
        if self.previousBlock is None:
            if self.blockHash == self.computeHash():
                return False
            else:
                return True
        else:
            self.blockHash = self.computeHash()
            current_block_validity = self.blockHash == self.computeHash()
            previous_block_validity = self.previousBlock.is_valid_chain()
            return current_block_validity and previous_block_validity

    def validate_block(self):
        if self.is_valid_chain() and len(self.signatures) >= 3:
            self.valid = True
        else:
            self.valid = False

    def sign_block(self, private_key):
        signature = Signature.sign(self.blockHash, private_key)
        self.signatures.append(signature)

    @staticmethod
    def get_prev_block():
        block = []
        count = 0
        with open(blockPath, "rb") as file:
            try:
                while True:
                    loadPickle = pickle.load(file)
                    block.append(loadPickle)
                    count = count + 1
            except EOFError:
                pass