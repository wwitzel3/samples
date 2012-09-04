
class Stack(object):
    def __init__(self, sz):
        self.sz = sz
        self._list = [None]*self.sz
        self._n = 0

    def push(self, item):
        if self.sz == self._n:
            self._list.extend([None] * self.sz)
            self.sz = self.sz * 2
        self._list[self._n] = item
        self._n += 1

    def pop(self):
        if self._n == 0:
            return None

        if (self.sz / self._n) % 4 == 0:
            pass

        self._n -= 1
        return self._list[self._n]

if __name__  == '__main__':
    s = Stack(5)
    s.push('a')
    s.push('a')
    s.push('b')
    s.push('c')
    s.push('d')
    s.push('e')
    print len(s._list)
