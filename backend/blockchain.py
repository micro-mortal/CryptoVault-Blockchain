import json
import hashlib
import time
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()  # Load blockchain from file when the app starts

    def load_chain(self):
        if os.path.exists('blockchain.json'):
            with open('blockchain.json', 'r') as file:
                self.chain = json.load(file)
        else:
            self.create_genesis_block()
            
    def save_chain(self):
        with open('blockchain.json', 'w') as file:
            json.dump(self.chain, file, indent=4)

    def create_genesis_block(self):
        # Create the first block (genesis block)
        genesis_block = {
            "index": 0,
            "timestamp": time.time(),
            "data": "Genesis Block",
            "previous_hash": "0",
            "hash": self.compute_hash(0, "Genesis Block", "0")
        }
        self.chain.append(genesis_block)
        self.save_chain()  # Save the genesis block to the file

    def add_block(self, data, key):
        index = len(self.chain)
        timestamp = time.time()
        previous_hash = self.chain[-1]["hash"]
        block_hash = self.compute_hash(index, data, previous_hash)

        new_block = {
            "index": index,
            "timestamp": timestamp,
            "data": data,
            "previous_hash": previous_hash,
            "hash": block_hash,
            "key": key  # Store the key with the block
        }

        self.chain.append(new_block)
        self.save_chain()  # Save the updated chain to the file
        return new_block

    def compute_hash(self, index, data, previous_hash):
        block_string = f"{index}{data}{previous_hash}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def delete_block(self, index):
        if index == 0:
            raise ValueError("Cannot delete the genesis block")

        if index < 0 or index >= len(self.chain):
            raise IndexError("Invalid block index")

        # Delete the block at the specified index
        self.chain.pop(index)

        # Recalculate hashes and reindex after the deletion
        for i in range(index, len(self.chain)):
            self.chain[i]["index"] = i
            self.chain[i]["previous_hash"] = self.chain[i-1]["hash"] if i > 0 else "0"
            self.chain[i]["hash"] = self.compute_hash(self.chain[i]["index"], self.chain[i]["data"], self.chain[i]["previous_hash"])

        self.save_chain()  # Save the updated chain after deletion
        return self.chain

    def delete_all_blocks(self):
        # Only keep the genesis block
        self.chain = [self.chain[0]]
        self.save_chain()  # Save after deleting all blocks
        return self.chain

    def get_chain(self):
        return self.chain
