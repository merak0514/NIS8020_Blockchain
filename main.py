"""Created: 2022/5/14"""
import node_host
import threading
import multiprocessing


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=node_host.run, args=('5001',))
    p2 = multiprocessing.Process(target=node_host.run, args=('5002',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print('main process end')
