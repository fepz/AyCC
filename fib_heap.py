# Fibonacci heap -- we have used some of the pseudocode at: 
# http://www.cs.princeton.edu/~wayne/cs423/fibonacci/FibonacciHeapAlgorithm.html

class LinkError(Exception): pass

# Heap item
class HeapItem(object):
    """ Represents an item in the heap. """
    def __init__(self, key, item):
        self.key = key
        self.pos = None
        self.item = item        
        

class HeapNode():
    """ Represents a node in the heap """
    def __init__(self, key, value):
        self.nodedegree = 0
        self.key = key
        self.value = value
        self.children = []
        self.parent = None
        self.marked = False
        
    def link(self, othertree):
        """ Add other tree to the list of childrens. """
        if self.key > othertree.key:
            raise LinkError
        self.children.append(othertree)
        othertree.parent = self
        
    def degree(self):
        """ Returns the degree (number of children) of the node. """
        return len(self.children)
        
    def str(self, indent = 0):
        """ String representation of the node. """
        return (" " * indent +
                "rank: %d key: %d value: %s (%s)" % (self.degree(), self.key, self.value, self.marked) +                
                "\n" + "".join(child.str(indent + 2) for child in self.children)
               )
    
    def __str__(self):
        return self.str()
        
        
class FibonacciHeap():
    """ Implements a Fibonacci Heap data structure. A Fibonacci heap is a 
    collection of trees satisfying the minimum-heap property, that is, the key 
    of a child is always greater than or equal to the key of the parent."""
    
    def __init__(self, key=None, value=None):
        """ Cretes a new Fibonacci Heap. """
        self.rootnodes = []
        self.minroot = None
        self.elements = 0
        self.rootdegrees = {}
        
        if key is not None and value is not None:
            self.rootnodes.append(HeapNode(key, value))
            self.minroot = self.rootnodes[0]
            #self.rootdegrees.add(self.minroot.degree())
        
    def findmin(self):
        """ Return the pointer to the node containing the minimum key value. """
        return self.minroot
        
    def merge(self, otherheap):
        """ The merge operation is implemented by concatenating the lists of 
        tree roots of the two heaps. """
        self.rootnodes.extend(otherheap.rootnodes)
        
        if self.minroot is None:
            self.minroot = self.rootnodes[0]
        
        # updates the minroot and degree list
        for root in self.rootnodes:
            if root.key <= self.minroot.key:
                self.minroot = root
        
    def insert(self, key, value):
        """ The insert operation works by creating a new heap with one element 
        and doing merge. """
        newheap = FibonacciHeap(key, value)
        self.merge(newheap)
        return newheap.minroot
        
    def extractmin(self):
        """ We take the root containing the minimum element and remove it. Its 
        children will become roots of new trees. """
        min_root = self.minroot        
        
        for child in min_root.children:
            self.rootnodes.append(child)
            child.parent = None
        
        self.rootnodes.remove(min_root)
        
        # successively linking together roots of the same degree
        for _ in range(len(self.rootnodes)):
            for root1 in self.rootnodes:
                for root2 in self.rootnodes:
                    if root1 != root2:
                        if root1.degree() == root2.degree():
                            if root1.key <= root2.key:                            
                                root1.link(root2)
                                self.rootnodes.remove(root2)
                            else:
                                root2.link(root1)
                                self.rootnodes.remove(root1)                            
                                break
                            
        # updates the minroot    
        if self.rootnodes:
            self.minroot = self.rootnodes[0]
            for root in self.rootnodes:
                if root.key <= self.minroot.key:
                    self.minroot = root
        else:
            self.minroot = None
            
        return min_root    
            
    def link(self, y, x):        
        # make y a child of x
        x.link(y)
        # remove y from the root list
        self.rootnodes.remove(y)
        y.marked = False        
         
    def decreasekey(self, node, newkey):
        parent = node.parent
        node.key = newkey        
        if parent is not None and node.key < parent.key:
            self.cutnode(node, parent)
            self.cascadecut(parent)
        if node.key < self.minroot.key:
            self.minroot = node
        
    def cutnode(self, node, parent):
        # remove node from the children list of its parent
        parent.children.remove(node)
        # add the node to the heap root list
        self.rootnodes.append(node)
        node.parent = None
        # now the node should be not marked
        node.marked = False
        
    def cascadecut(self, node):
        parent = node.parent
        if parent is not None:
            if node.marked is False:
                node.marked = True
            else:
                self.cutnode(node, parent)
                self.cascadecut(parent)
        
    def __str__(self):
        s = "elements: %d min: (%s,%s)" % (self.elements, str(self.minroot.key), str(self.minroot.value))        
        s += "\n"
        s += "".join(str(root) for root in self.rootnodes if root is not None)
        return s
        

def test():
    """ Test Fibonacci heap """
    heap = FibonacciHeap()
    heap.insert(10,1)
    heap.insert(9,2)
    heap.insert(2,3)    
    heap.insert(12,4)    
    node = heap.insert(17,5)    
    heap.insert(4,6)    
    heap.insert(15,7)
    heap.insert(22,8)
    print(heap)
    heap.extractmin2()
    print(heap)
    heap.insert(8,9)
    heap.insert(11,10)
    heap.insert(1,11)
    print(heap)
    heap.extractmin2()
    print(heap)
    heap.decreasekey(node, 3)    
    print(heap)
    
        
if __name__ == '__main__':
    test()
        