# NIS8020 Principle and Applications of Blockchain

SJTU

A simulation of blockchain, POW.

Tie breaking 策略：先来的先接受。

## observer node

这是模拟一个诚实节点，但是不会进行挖矿，在创世就存在，且中途不会退出。

它其实是给我观测的一个节点。让我看到现在的区块链情况。

## Honest nodes

这部分节点按照同步-挖矿的方式迭代进行。

## malicious nodes

第一部分的攻击是分叉攻击，试图生成一个新的分叉。

这一部分的攻击者们不和诚实节点双向同步（即只有诚实节点来拉取，而攻击者不拉取）。攻击者之间的同步是双向的。

这是为了模拟在效率最高的情况下，攻击者以少量算力形成分叉攻击的可能性。

成功的依据是最少三个恶意节点被写入共识区块中。
