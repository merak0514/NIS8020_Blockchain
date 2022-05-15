"""Created: 2022/5/14"""
# An honest observer that starts at very beginning, and will follow the rules honestly. It cannot mine.
# host for observer
from flask import Flask, jsonify, request
from time import time
from model import Blockchain

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain(fake=True)
current_port = '6000'  # 可以通过调用run来改变这个。

t0 = time()  # starting time
count = 1  # 计数器
last_count = 1  # 计数器
last_t = time()


@app.route('/summary', methods=['GET'])
def summarize():
    def compute_malicious():
        """计算连续的恶意节点数量"""
        max_c = 0
        c = 0  # malicious count
        for block in blockchain.chain:
            if block['creator'] == 'malicious':
                c += 1
                max_c = max(max_c, c)
            else:
                c = 0
        return max_c
    global count, last_t, last_count
    count = len(blockchain.chain)
    now = time()
    response = {
        'max_malicious_count': compute_malicious(),
        'period_speed (block/second)': f'{(count - last_count) / (now - last_t):.2f}',
        'whole_speed (block/second)': f'{count / (now - t0):.2f}',
        'block_length': f'{count}',
        'period_time': now-last_t,
        'whole_time': now-t0
    }
    last_t = now
    last_count = count
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


def run(port=None):
    global current_port, t0
    current_port = port
    t0 = time()
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    run(current_port)
