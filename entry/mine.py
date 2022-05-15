"""Created: 2022/5/11"""
import requests as re
import time
from tqdm import tqdm


if __name__ == '__main__':
    # Try to estimate the speed of mining a block, aka the growth of the blockchain.
    n = 15
    t1 = time.time()
    for _ in tqdm(range(n)):
        response = re.get('http://localhost:5001/mine')
        if response.status_code != 200:
            print('Mining failed, damn it!')
            break
    t2 = time.time()
    print('Mining speed:', (t2 - t1) / n)
