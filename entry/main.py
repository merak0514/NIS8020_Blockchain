"""Created: 2022/5/14"""
from host import node_host
from user import honest_miner, malicious_miner, observer
import multiprocessing


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=node_host.run, args=('5001',))
    p2 = multiprocessing.Process(target=node_host.run, args=('5002',))
    p3 = multiprocessing.Process(target=honest_miner.main, args=(0,))
    p4 = multiprocessing.Process(target=honest_miner.main, args=(1,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    print('main process end')
