from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import pickle
import uuid

blockPath = 'data/block.dat'
class CBlock:
    data = None
    previousHash = None
    previousBlock = None
    blockHash = None
    blockId = None
    flagValidationStatus = 0
    valid = None

    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        self.blockId = uuid.uuid1()
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        return digest.finalize()

    def update_flag_validation_status(self):
        if self.previousBlock is not None:
            previous_valid_flags = self.previousBlock.flagValidationStatus
            if previous_valid_flags >= 3:
                self.flagValidationStatus = previous_valid_flags + 1
            else:
                self.flagValidationStatus = 0

    def is_valid_chain(self):
        if self.previousBlock == None:
            if self.blockHash == self.computeHash():
                return True
            else:
                return False
        else:
            current_block_validity = self.blockHash == self.computeHash()
            previous_block_validity = self.previousBlock.is_valid_chain()
            return current_block_validity and previous_block_validity

    def validate_block(self):
        if self.is_valid_chain() and self.flagValidationStatus >= 3:
            self.valid = True
        else:
            self.valid = False

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
