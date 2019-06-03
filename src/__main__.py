# -*- coding: utf-8 -*-

""""""

import os
import time
import psutil

from random import randint

from src.rmq import RMQ


def check_rmq_step(rmq, arr, l, r) -> bool:
    return rmq.get(l, r) == min(arr[l:r+1])


def check_rmg():
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


if __name__ == '__main__':
    pass
    print(set('qwe'))

    # check_rmg()
