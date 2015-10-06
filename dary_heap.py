import math

# The code is based on from http://www.cs.cmu.edu/~ckingsf/class/02713-s13/src/mst.py

# Heap item
class HeapItem(object):
    """Represents an item in the heap"""
    def __init__(self, key, value):
        self.key = key
        self.pos = None
        self.value = value        
        

# d-ary Heap
class Heap():
    def __init__(self, dary=2):
        self.heap = []
        self.dary = dary
    
    def siftdown(self, node, pos):
        """ Move node down in the tree; restore heap condition after deletion 
        or replacement. """
        c = self.minchild(pos)
        while c is not None and self.heap[c].key < node.key:
            self.heap[pos] = self.heap[c]
            self.heap[pos].pos = pos
            pos = c
            c = self.minchild(c)
        self.heap[pos] = node
        node.pos = pos
        
    def siftup(self, node, pos):
        """Move hi up in heap until it's parent is smaller than hi.key"""
        p = self.parent(pos)
        while p is not None and self.heap[p].key > node.key:
            self.heap[pos] = self.heap[p]
            self.heap[pos].pos = pos
            pos = p
            p = self.parent(p)
        self.heap[pos] = node
        node.pos = pos        

    def findmin(self):
        """Return element with smallest key, or None if heap is empty"""
        return self.heap[0] if len(self.heap) > 0 else None

    def extractmin(self):
        """Delete the smallest item"""
        if len(self.heap) == 0: 
            return None
        i = self.heap[0]
        last = self.heap[-1]
        del self.heap[-1]
        if len(self.heap) > 0:
            self.siftdown(last, 0)
        return i

    def insert(self, key, value):
        """Insert an item into the heap"""
        self.heap.append(None)
        hi = HeapItem(key,value)
        self.siftup(hi, len(self.heap)-1)
        return hi

    def decreasekey(self, node, newkey):
        """Decrease the key of hi to newkey"""
        node.key = newkey
        self.siftup(node, node.pos)

    def parent(self, pos):
        """Return the position of the parent of pos"""
        if pos == 0: 
            return None
        return int(math.ceil(pos / self.dary) - 1)

    def children(self, pos):
        """Return a list of children of pos"""
        return range(self.dary * pos + 1, min(self.dary * (pos + 1) + 1, len(self.heap)))

    def minchild(self, pos):
        """Return the child of pos with the smallest key"""
        minpos = minkey = None
        for c in self.children(pos):
            if minkey == None or self.heap[c].key < minkey:
                minkey, minpos = self.heap[c].key, c
        return minpos
        