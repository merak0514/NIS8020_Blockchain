"""Created: 2022/5/14"""
import time

from host import node_host, observer_host
from user import honest_miner, malicious_miner, observer
import multiprocessing


if __name__ == '__main__':
    s1 = multiprocessing.Process(target=observer_host.run, args=('6000',))
    # p00 = multiprocessing.Process(target=observer.main)
    s2 = multiprocessing.Process(target=node_host.run, args=('5001',))  # s for server
    s3 = multiprocessing.Process(target=node_host.run, args=('5002',))
    s4 = multiprocessing.Process(target=node_host.run, args=('5003',))
    s5 = multiprocessing.Process(target=node_host.run, args=('5004',))
    s6 = multiprocessing.Process(target=node_host.run, args=('5005',))
    u2 = multiprocessing.Process(target=honest_miner.main, args=('5001',))  # u for user
    u3 = multiprocessing.Process(target=honest_miner.main, args=('5002',))
    u4 = multiprocessing.Process(target=honest_miner.main, args=('5003',))
    u5 = multiprocessing.Process(target=honest_miner.main, args=('5004',))
    u6 = multiprocessing.Process(target=honest_miner.main, args=('5005',))

    # malicious
    s10 = multiprocessing.Process(target=node_host.run, args=('5008',))
    u10 = multiprocessing.Process(target=malicious_miner.main, args=('5008',))

    # start
    s1.start()
    s2.start()
    s3.start()
    s4.start()
    s5.start()
    s6.start()
    s10.start()
    time.sleep(0.5)
    u2.start()
    u3.start()
    u4.start()
    u5.start()
    u6.start()
    time.sleep(2)
    u10.start()
    s1.join()
    s2.join()
    s3.join()
    s4.join()
    s5.join()
    s6.join()
    s10.join()
    u2.join()
    u3.join()
    s4.join()
    u4.join()
    u5.join()
    u6.join()
    u10.join()
    print('main process end')
