class Grid(object):
    def __init__(self, x,y):
        _size = x*y

        self.virtual_start = 0
        self.virtual_end = _size+1

        self._id = range(0,_size+2)
        self._sz = range(0,_size+2)

        _range = x+1

        for i in self._id[1:_range]:
            self.union(i, self.virtual_start)

        for i in self._id[-_range:_size+1]:
            self.union(i, self.virtual_end)

    def union(self, p, q):
        _proot = self.root(p)
        _qroot = self.root(q)
        self._id[_proot] = _qroot

    def root(self, p):
        while (p != self._id[p]):
            p = self._id[p]
        return p

    def connected(self, p, q):
        return self.root(p) == self.root(q)

if __name__ == '__main__':
    grid = Grid(5,5)

    grid.union(10,25)
    print grid.connected(0,26)

    grid.union(10,6)
    print grid.connected(0,26)

    grid.union(1,6)
    print grid.connected(0,26)
