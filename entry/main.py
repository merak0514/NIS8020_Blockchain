"""Created: 2022/5/14"""
from host import node_host, observer_host
from user import honest_miner, malicious_miner, observer
import multiprocessing


if __name__ == '__main__':
    p0 = multiprocessing.Process(target=observer_host.run, args=('6000',))
    # p00 = multiprocessing.Process(target=observer.main)
    p1 = multiprocessing.Process(target=node_host.run, args=('5001',))
    p2 = multiprocessing.Process(target=node_host.run, args=('5002',))
    p3 = multiprocessing.Process(target=honest_miner.main, args=('5001',))
    p4 = multiprocessing.Process(target=honest_miner.main, args=('5002',))

    # malicious
    p5 = multiprocessing.Process(target=node_host.run, args=('5008',))
    p6 = multiprocessing.Process(target=malicious_miner.main, args=('5008',))

    # start
    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p0.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    print('main process end')
