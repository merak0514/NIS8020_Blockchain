"""Created: 2022/5/10"""
# host for miners
from time import time

from flask import Flask, jsonify, request
from model import Blockchain
import argparse

# Instantiate our Node
app = Flask(__name__)

FAKE = True  # To protect your computer, use this to enable fake mining,
# which will use time.sleep to simulate the mining of a block.

# Instantiate the Blockchain
blockchain = Blockchain(fake=FAKE)
current_port = '5001'  # 可以通过调用run来改变这个。
t0 = time()  # starting time


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    # add neighbor nodes to current chain
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.neighbour),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain,
            'replace_code': 1,
            'length': len(blockchain.chain)
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain,
            'replace_code': 0,
            'length': len(blockchain.chain)
        }

    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    q = 16  # 每次轮可以做的RO查询数

    type_ = request.args.get('type')

    last_block = blockchain.last_block
    prev_hash = blockchain.hash(last_block)
    # proof = blockchain.proof_of_work(prev_hash)
    for _ in range(q):
        # 挖一下
        success, proof = blockchain.fake_pow(prev_hash)
        if success:
            # We must receive a reward for finding the proof.
            if type_ == 'malicious':
                income = 100
                recipient = 'malicious'
            else:
                income = 1
                recipient = current_port
            blockchain.new_transaction(
                sender="0",
                recipient=recipient,
                amount=income,
            )

            # Forge the new Block by adding it to the chain
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash, creator=type_)

            response = {
                'found': True,
                'message': "New Block Forged",
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
            }
            return jsonify(response), 200
    response = {
        'found': False
    }
    return jsonify(response), 200


@app.route('/test', methods=['POST'])
def test():
    print(request.get_json())
    return '1', 201


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain,
    }
    return jsonify(response), 200


@app.route('/nodes/compute_m', methods=['GET'])
def compute_malicious():
    """计算连续的恶意节点数量"""
    max_c = 0
    c = 0  # malicious count
    for block in blockchain.chain:
        if block['creator'] == 'malicious':
            if c == 0:
                c = 1
            elif c > 0:
                c += 1
        else:
            max_c = max(max_c, c)
            c = 0
    max_c = max(max_c, c)
    return max_c


def run(port):
    global current_port, t0
    current_port = port
    t0 = time()
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    run(args.port)
