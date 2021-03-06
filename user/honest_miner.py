"""Created: 2022/5/12"""
# start an honest miner connected to the args.port_id port.
import requests as re
import time
from tqdm import tqdm
import argparse


def main(port):
    # Try to estimate the speed of mining a block, aka the growth of the blockchain.
    all_nodes = ['5001', '5002', '5003', '5004', '5005', '5006', '5007', '5008', '5009', '5010']
    print("Adding neighbours:", all_nodes)
    re.post(f'http://localhost:{port}/nodes/register', json={'nodes': all_nodes},
            headers={'Content-Type': 'application/json'})
    while True:
        # resolve conflicts
        r = re.get(f'http://localhost:{port}/nodes/resolve')
        # if r.json()['replace_code']:
        #     print(f'Chain replaced, new length is {r.json()["length"]}')

        response_js = re.get(f'http://localhost:{port}/mine?type=honest').json()
        # if response_js['found']:
        #     print('index', response_js['index'])


if __name__ == '__main__':
    time.sleep(1)
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=str, default='5001')
    args = parser.parse_args()
    main(args.port)
