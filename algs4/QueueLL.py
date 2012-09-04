class Node(object):
    def __init__(self):
        self.item = None
        self.next = None

class Queue(object):
    def __init__(self):
        self.first = None
        self.last = None

    def is_empty(self):
        return self.first == None

    def enqueue(self, item):
        old = self.last
        self.last = Node()
        self.last.item = item
        self.last.next = None
        if self.is_empty():
            self.first = self.last
        else:
            old.next = self.last

    def dequeue(self):
        item = self.first.item
        self.first = self.first.next
        if self.is_empty():
            self.last = None
        return item

def main():
    q = Queue()
    q.enqueue('a')
    q.enqueue('b')
    print q.dequeue()
    print q.dequeue()

if __name__ == '__main__':
    main()
