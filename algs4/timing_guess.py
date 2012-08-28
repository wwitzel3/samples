"""
N, t(N), R(t), lg(Rt)
2000,  .25, 0, 0
4000,  .49, 2, 1
8000,  1.0, 2, 1

1.0 = aN^b
b = log2(Rt)
a = t(N)/N^b

OR

t(N) = 0.000125 x N
N = 64,000
t(N) = 8.0
"""

import timeit

def test():
    for i in xrange(1000):
        i = 10
        j = i + i
        j = j * 100


if __name__ == '__main__':
    t = timeit.Timer("test()", "from __main__ import test")
    print t.timeit(64000)

