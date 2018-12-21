# -*- coding: utf-8 -*-

""""""

# Author: Bedarev Nickolay
# Mail: n.bedarev@lcgroup.su
# Limeteam slack: nikkollaii
# Date: 14.12.2018

import sys

from typing import List, Tuple
from math import log


class RMQ1(object):
    def __init__(self, A: List[int]):
        self.A = A
        N = len(A)
        self.block_size = int(log(N)+1 / 2)
        K = int(N / self.block_size) if N % self.block_size == 0 else int(N / self.block_size) + 1
        # предподсчитаем позиции минимумов в каждом блоке
        cur_block = -1
        B = [-1]*K
        for i in range(N):
            if i % self.block_size == 0:
                cur_block += 1
            if B[cur_block] == -1 or A[B[cur_block]] > A[i]:
                B[cur_block] = i
        # построим Sparse table на массиве B
        self.ST = [[-1]*(int(log(N)+1)+1) for _ in range(K)]
        for i, value in enumerate(B):
            self.ST[i][0] = value
        j = 1
        while j <= log(N)+1:
            for i in range(K):
                ind = (1 << (j - 1)) + i
                if ind >= K:
                    self.ST[i][j] = self.ST[i][j - 1]
                # elif A[self.ST[ind][j - 1]] <= A[self.ST[i][j - 1]]:
                elif self.ST[ind][j - 1] <= self.ST[i][j - 1]:
                    self.ST[i][j] = self.ST[ind][j - 1]
                else:
                    self.ST[i][j] = self.ST[i][j - 1]
            j += 1
        # Посчитаем тип для каждого блока
        self._type = [0]*K
        cur_block = 0
        j = 0
        i = 0
        while i < N or j < self.block_size:
            if j == self.block_size:
                j = 0
                cur_block += 1
            if j > 0 and (i >= N or A[i - 1] < A[i]):
                self._type[cur_block] += (1 << (j-1))
            i += 1
            j += 1
        # Осталось только для каждого блока предподсчитать позиции минимумов на всех подотрезках
        self.block_min = [None for _ in range(K)]

        for i in range(K):
            t = self._type[i]
            if self.block_min[t] is None:
                self.block_min[t] = [[None for _ in range(self.block_size)] for _ in range(self.block_size)]
            else:
                continue
            for l in range(self.block_size):
                self.block_min[t][l][l] = l
                for r in range(l+1, self.block_size):
                    self.block_min[t][l][r] = self.block_min[t][l][r-1]
                    if i*self.block_size+r < N:
                        if A[i * self.block_size + r] < self.A[i*self.block_size + self.block_min[t][l][r]]:
                            self.block_min[t][l][r] = r

        j = 0
        self.log2 = [0]*N
        for i in range(N):
            if 1 << (j + 1) <= i:
                j += 1
            self.log2[i] = j

    def _block_rmq(self, block_number: int, l: int, r: int) -> int:
       return self.block_min[self._type[block_number]][l][r] + block_number * self.block_size
    #
    # def get(self, l: int, r: int) -> int:
    #     bl = int(l / self.block_size)
    #     br = int(r / self.block_size)
    #     if bl == br:
    #         return self.A[self._block_rmq(bl, l % self.block_size, r % self.block_size)]
    #     ansl = self.A[self._block_rmq(bl, l % self.block_size, self.block_size - 1)]
    #     ansr = self.A[self._block_rmq(br, 0, r % self.block_size)]
    #     if bl + 1 < br:
    #         power = self.log2[br-bl-1]
    #         ansb = min((self.A[self.ST[bl + 1][power]], self.A[self.ST[br - (1 << power)][power]]))
    #         return min((ansb, min(ansl, ansr)))
    #     return min(ansl, ansr)

    def get(self, l: int, r: int) -> int:
        return self.A[self.get_ind(l, r)]

    def get_ind(self, l: int, r: int) -> int:
        bl = int(l / self.block_size)
        br = int(r / self.block_size)
        if bl == br:
            return self._block_rmq(bl, l % self.block_size, r % self.block_size)

        answers = []
        indl = self._block_rmq(bl, l % self.block_size, self.block_size - 1)
        ansl = self.A[indl]
        answers.append((indl, ansl))

        indr = self._block_rmq(br, 0, r % self.block_size)
        ansr = self.A[indr]
        answers.append((indr, ansr))

        if bl + 1 < br:
            power = self.log2[br - bl - 1]
            indll = self.ST[bl + 1][power]
            indrr = self.ST[br - (1 << power)][power]
            if self.A[indll] < self.A[indrr]:
                answers.append((indll, self.A[indll]))
            else:
                answers.append((indrr, self.A[indrr]))

        return sorted(answers, key=lambda x: x[1])[0][0]

    def size(self):
        return len(self.A)
