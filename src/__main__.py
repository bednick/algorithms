# -*- coding: utf-8 -*-

""""""

# Author: Bedarev Nickolay
# Mail: n.bedarev@lcgroup.su
# Limeteam slack: nikkollaii
# Date: 14.12.2018

from random import randint
from src.rmq import RMQ


def check(rmq, arr, l, r) -> bool:
    return rmq.get(l, r) == min(arr[l:r+1])


if __name__ == '__main__':
    N = 10

    array = [randint(0, 1000) for _ in range(N)]
    rmq = RMQ(array)

    assert rmq.size == len(array)
    assert check(rmq, array, 0, 0)
    assert check(rmq, array, 0, 1)
    assert check(rmq, array, 0, 2)
    assert check(rmq, array, 0, 3)
    assert check(rmq, array, 3, 4)
    assert check(rmq, array, 3, 5)
    assert check(rmq, array, 3, 6)
    assert check(rmq, array, 3, 7)
    assert check(rmq, array, 0, 100)
