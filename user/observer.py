"""Created: 2022/5/15"""
# start an honest miner connected to the args.port_id port.
import requests as re
import time
from tqdm import tqdm
import argparse


def main():
    time.sleep(0.5)
    # Try to estimate the speed of mining a block, aka the growth of the blockchain.
    all_nodes = ['5001', '5002', '5003', '5004', '5005', '5006', '5007', '5008', '5009', '5010']
    # all_nodes = ['5001', '5002']
    port = '6000'
    print("All neighbours for observer:", all_nodes)
    re.post(f'http://localhost:{port}/nodes/register', json={'nodes': all_nodes},
            headers={'Content-Type': 'application/json'})

    longest = 0

    while True:
        # resolve conflicts
        r = re.get(f'http://localhost:{port}/nodes/resolve')
        # if r.json()['replace_code']:
        #     print(f'Chain replaced, new length is {r.json()["length"]}')
        r2 = re.get(f'http://localhost:{port}/summary')
        print('Summary: ', r2.json())
        if r2.json()['max_malicious_count'] >= 3:
            print("Malicious Win!")
            input()
        time.sleep(1)


if __name__ == '__main__':
    main()
