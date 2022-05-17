# NIS8020 Principle and Applications of Blockchain

SJTU

A simulation of blockchain, POW.

Tie breaking 策略：先来的先接受。

参考：https://medium.com/@vanflymen/learn-blockchains-by-building-one-117428612f46

## observer node

这是模拟一个诚实节点，但是不会进行挖矿，在创世就存在，且中途不会退出。

它其实是给我观测的一个节点。让我看到现在的区块链情况。

使用方法：

    python3 host/observer_host.py
    python3 user/observer.py

## Honest nodes

这部分节点按照同步-挖矿的方式迭代进行。

使用方法：

    python3 host/observer_host.py 5001 <port>
    python3 user/observer.py <port>


## malicious nodes

### 分叉攻击

第一部分的攻击是分叉攻击，试图生成一个新的分叉。

这一部分的攻击者们不和诚实节点双向同步（即只有诚实节点来拉取，而攻击者不拉取）。攻击者之间的同步是双向的。

这是为了模拟在效率最高的情况下，攻击者以少量算力形成分叉攻击的可能性。

成功的依据是最少三个恶意节点被写入共识区块中。

恶意节点之间可以自由通讯（not implemented yet）。

使用方法：

    python3 host/observer_host.py 5001 <port>
    python3 user/observer.py <port>

# 挖矿模拟

    python3 host/node_host.py 5001
    python3 entry/mine.py 

# 多线程运行模拟分叉攻击

    python3 entry/main.py
    python3 user/observer.py  # at another terminal.


