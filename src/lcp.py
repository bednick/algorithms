# -*- coding: utf-8 -*-

""""""

from math import log2


class LongestCommonPrefix(object):

    def __init__(self, string: str):
        self.cc = []

        s = [ord(ch) for ch in (string + '\0')]
        alphabet = max(s) + 1
        n = len(s)
        self.n = n
        self.log_n = int(log2(n))
        p = [0] * n
        cnt = [0] * alphabet
        c = [0] * n
        for i in range(n):
            cnt[s[i]] += 1
        for i in range(1, alphabet):
            cnt[i] += cnt[i - 1]
        for i in range(n):
            cnt[s[i]] -= 1
            p[cnt[s[i]]] = i
        c[p[0]] = 0
        classes = 1
        for i in range(1, n):
            if s[p[i]] != s[p[i - 1]]:
                classes += 1
            c[p[i]] = classes - 1
        self.cc.append(c[:])

        pn = [0] * n
        cn = [0] * n
        h = 0
        while (1 << h) < n:
            for i in range(n):
                pn[i] = p[i] - (1 << h)
                if pn[i] < 0:
                    pn[i] += n
            for i in range(classes):
                cnt[i] = 0
            for i in range(n):
                cnt[c[pn[i]]] += 1

            for i in range(1, classes):
                cnt[i] += cnt[i - 1]
            for i in range(n - 1, -1, -1):
                cnt[c[pn[i]]] -= 1
                p[cnt[c[pn[i]]]] = pn[i]
            cn[p[0]] = 0
            classes = 1
            for i in range(1, n):
                mid1 = (p[i] + (1 << h)) % n
                mid2 = (p[i - 1] + (1 << h)) % n
                if c[p[i]] != c[p[i - 1]] or c[mid1] != c[mid2]:
                    classes += 1
                cn[p[i]] = classes - 1
            for i, v in enumerate(cn):
                c[i] = v
            self.cc.append(c[:])
            h += 1
        self.p = p[1:]

    def get(self, i: int, j: int):
        if i < 0 or i > j or j > self.n:
            raise ValueError('Incorrect i or j')
        if i == j:
            return self.n - 1 - i
        ans = 0
        for k in range(self.log_n, -1, -1):
            if self.cc[k][i] == self.cc[k][j]:
                ans += 1 << k
                i += 1 << k
                j += 1 << k
        return ans


if __name__ == '__main__':
    lcp = LongestCommonPrefix('abacaba')
    assert (lcp.get(0, 1) == 0)
    assert (lcp.get(0, 2) == 1)
    assert (lcp.get(0, 3) == 0)
    assert (lcp.get(0, 4) == 3)
    assert (lcp.get(0, 5) == 0)
    assert (lcp.get(0, 6) == 1)
    assert (lcp.get(0, 0) == 7)
    assert (lcp.get(0, 7) == 0)
    assert (lcp.get(1, 5) == 2)
    assert (lcp.get(2, 6) == 1)
    assert (lcp.get(7, 7) == 0)
