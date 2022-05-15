"""Created: 2022/5/14"""
# An honest observer that starts at very beginning, and will follow the rules honestly. It cannot mine.
from flask import Flask, jsonify, request
from time import time
from block_chain import Blockchain

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain(fake=True)
current_port = '6000'  # 可以通过调用run来改变这个。

t0 = time()  # starting time
count = 1  # 计数器
last_t = time()


@app.route('/summarize', methods=['GET'])
def summarize():
    global count, last_t
    count = len(blockchain.chain)
    now = time()
    response = {
        'period_speed (block/second)': f'{count / (now - last_t):.2f}',
        'whole speed (block/second)': f'{count / (now - t0):.2f}',
        'block length': f'{count}',
        'total_nodes': list(blockchain.neighbour),
        'period_time': now-last_t,
        'whole_time': now-t0
    }
    last_t = now
    return response, 200


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


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain,
    }
    return jsonify(response), 200


def run(port):
    global current_port, t0
    current_port = port
    t0 = time()
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    run(current_port)
