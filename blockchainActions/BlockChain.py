from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import pickle

blockPath = 'data/block.dat'
class CBlock:
    data = None
    previousHash = None
    previousBlock = None

    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        return digest.finalize()

    def is_valid(self):
        if self.previousBlock == None:
            return True
        return self.previousBlock.computeHash() == self.previousHash

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