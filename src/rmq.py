# -*- coding: utf-8 -*-

""""""

import os
import time
import psutil

from random import randint
from typing import List, Tuple

from src.lca_tree import LCAFree, Node
from src.rmq1 import RMQ1


class RMQ(object):
    def __init__(self, sequence: List[int]):
        self.size = len(sequence)
        self._tree = LCAFree(sequence)
        self._eulerian_path = self._tree.get_eulerian_path()  # type: List[Tuple[int, Node]]
        for ind, (_, node) in enumerate(self._eulerian_path):
            node.value = ind
        self._rmq1 = RMQ1([number for number, node in self._eulerian_path])

    def get(self, l: int, r: int) -> int:
        if l > r:
            l, r = r, l
        l = int(max((0, l)))
        r = int(min((self.size-1, r)))

        l_node = self._tree.nodes[l]
        r_node = self._tree.nodes[r]
        if l_node.value < r_node.value:
            ind = self._rmq1.get_ind(l_node.value, r_node.value)
        else:
            ind = self._rmq1.get_ind(r_node.value, l_node.value)

        return self._eulerian_path[ind][1].priority


def check_rmq_step(rmq, arr, l, r) -> bool:
    return rmq.get(l, r) == min(arr[l:r+1])


if __name__ == '__main__':
    N = 90000

    array = [randint(0, 1000) for _ in range(N)]
    start = time.time()
    rmq = RMQ(array)
    print(f'N: {N}')
    print(time.time() - start)
    process = psutil.Process(os.getpid())
    print('memory', process.memory_info().rss)  # in bytes
    print('memory', process.memory_info().rss / (1024 * 1024))

    assert rmq.size == len(array)
    assert check_rmq_step(rmq, array, 0, 0)
    assert check_rmq_step(rmq, array, 0, 1)
    assert check_rmq_step(rmq, array, 0, 2)
    assert check_rmq_step(rmq, array, 0, 3)
    assert check_rmq_step(rmq, array, 3, 4)
    assert check_rmq_step(rmq, array, 3, 5)
    assert check_rmq_step(rmq, array, 3, 6)

