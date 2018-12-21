# -*- coding: utf-8 -*-

""""""

# Author: Bedarev Nickolay
# Mail: n.bedarev@lcgroup.su
# Limeteam slack: nikkollaii
# Date: 15.12.2018

from typing import List, Tuple


class Node(object):
    def __init__(self, key: int, priority: float, value: object = None, parent: "Node" = None,
                 left: "Node" = None, right: "Node" = None):
        self.key = key
        self.priority = priority
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class LCAFree(object):
    sequence: List[int] = None
    root: Node = None
    _last: Node = None

    def __init__(self, sequence: List[int]):
        self.sequence = sequence
        self.nodes = list()
        for key, priority in enumerate(sequence):
            if self.root is None:
                self.root = Node(key, priority, parent=None)
                self.nodes.append(self.root)
                self._last = self.root
                continue
            node = Node(key, priority)
            self.nodes.append(node)

            parent = None
            for check in self._up_iter(self._last):
                if check.priority <= priority:
                    parent = check
                    break
            if parent is None:
                # Устанавливаем как root
                tail = self.root
                self.root.parent = node
                self.root = node
            else:
                tail = parent.right
                parent.right = node
                node.parent = parent
            node.left = tail
            if tail is not None:
                tail.parent = node
            self._last = node

    def __str__(self):
        return f"LCAFree: {self.root}"

    def _up_iter(self, node: Node):
        while node is not None:
            yield node
            node = node.parent

    def _get_eulerian_path(self, level: int, node: Node) -> List[Tuple[int, Node]]:
        """

        :param node:
        :param level:
        :return: List[Tuple(level: int,  int)
        """
        if node is None:
            return []
        res = list()  # type: List[Tuple(int, Node)]
        res.append((level, node))
        if node.left is not None:
            res.extend(self._get_eulerian_path(level+1, node.left))
            res.append((level, node))
        if node.right is not None:
            res.extend(self._get_eulerian_path(level+1, node.right))
            res.append((level, node))
        return res

    def get_eulerian_path(self) -> List[Tuple[int, Node]]:
        return self._get_eulerian_path(0, self.root)
