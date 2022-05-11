"""Created: 2022/5/10"""

import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests


class Blockchain(object):
    def __init__(self, difficulty=4):  # 难度+1，困难16倍。
        self.current_transactions = []
        self.chain = []
        self.neighbour = set()
        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)
        self.difficulty = difficulty

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        print(proof)
        return proof

    def valid_proof(self, prev_hash, proof):
        guess = f'{prev_hash}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()  # 十六进制的哈希。
        return guess_hash[:self.difficulty] == "0" * self.difficulty

    def valid_chain(self, chain):
        chain_length = len(chain)
        if chain_length == 1:
            return True
        counter = 1
        p1 = chain[counter - 1]  # pointer 1
        p2 = chain[counter]
        while True:
            p1_hash = self.hash(p1)
            if p1_hash != p2['previous_hash']:  # 检查哈希
                return False
            if not self.valid_proof(p1_hash, p2['proof']):
                return False
            counter += 1
            if counter >= chain_length:
                break
            p1 = p2
            p2 = chain[counter]
        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.neighbour
        new_chain = None
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            length, chain = self.query_node(node)
            if length == -1:
                print(f"Invalidate node {node}")
                continue
            # Check if the length is longer and the chain is valid
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url:
            self.neighbour.add(parsed_url.netloc)

    @staticmethod
    def query_node(node):
        response = requests.get(f'http://{node}/chain')
        if response.status_code == 200:
            js = response.json()
            return js['length'], js['chain']
        return -1, {}
