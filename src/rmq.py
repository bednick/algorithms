# -*- coding: utf-8 -*-

""""""

# Author: Bedarev Nickolay
# Mail: n.bedarev@lcgroup.su
# Limeteam slack: nikkollaii
# Date: 15.12.2018

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
