"""Created: 2022/5/10"""

import hashlib
import json
from time import time, sleep
from urllib.parse import urlparse
import requests
import random


class Blockchain(object):
    def __init__(self, difficulty=5, fake: bool=False):  # 难度+1，困难16倍。
        self.fake = fake
        self.current_transactions = []
        self.chain = []
        self.neighbour = set()
        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)
        self.difficulty = difficulty

    def new_block(self, proof, previous_hash=None, creator=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'creator': creator,
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

    def fake_pow(self, last_proof):
        # BASE_TIME = 2.56e-5 * 2  # 模拟测试出来的; *2 是因为模拟出来的是平均值。
        BASE_TIME = 3e-4  # 每一轮的耗时，预计16轮出块
        difficulty = pow(2, self.difficulty)
        real_time = BASE_TIME * difficulty
        sleep(real_time)
        if random.random() < 1/256:  # 成功出块
            return 1, 'success'
        return 0, 'fail'  # 失败出块

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
        if self.fake:  # fake mode
            return True
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
                # print(f"Invalidate node {node}")  # enable to debug
                continue
            # Current tie breaking strategy: keep the first one.
            # if length == max_length and self.valid_chain(chain):
            #     if random.random() < 0.5:  # 两条链相等则50%的概率接收
            #         max_length = length
            #         new_chain = chain
            if length > max_length and self.valid_chain(chain):  # 接收长的
                max_length = length
                new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def register_node(self, address):
        self.neighbour.add(address)

    @staticmethod
    def query_node(node):
        response = requests.get(f'http://0.0.0.0:{node}/chain')  # 所以就算节点不存在也不会中断程序。
        if response.status_code == 200:
            js = response.json()
            return js['length'], js['chain']
        return -1, {}
