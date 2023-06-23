from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import pickle
import uuid

blockPath = 'data/block.dat'


class CBlock:
    data = None
    previousHash = None
    previousBlock = None
    blockHash = None
    blockId = None
    valid = 0

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
        if self is None:
            return True
        # Check if the current block is valid
        if not self.validate_block():
            return False
        # Recursively validate the previous blocks in the chain
        return self.previousBlock.is_valid_chain()

    def validate_block(self):
        # Verify data integrity and correctness
        if self.data is None:
            return False
        # Check if the block has a previous block
        if self.previousBlock is None:
            return True
        # Check block linkage
        if self.previousBlock.computeHash() != self.previousHash:
            return False
        # Calculate block hash and compare
        calculated_hash = self.computeHash()
        if self.blockHash != calculated_hash:
            return False
        # Optionally check other flags
        if self.blockId is None or self.valid is None:
            return False

        return True

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

        if count > 0:
            prev_block = block[-1]
            if prev_block.previousBlock is None and count > 1:
                prev_block.previousBlock = block[-2]
                prev_block.previousHash = block[-2].computeHash()
            return prev_block
        return None