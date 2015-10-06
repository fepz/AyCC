# Code borrowed from: http://code.activestate.com/recipes/511508-binomial-queues/

class LinkError(Exception): pass
class EmptyBinomialHeapError(Exception): pass
    
class TreeItem:
    """ An item in a binomial tree. """
    def __init__(self, key, value, tree):
        self.key = key
        self.value = value
        self.tree = tree

class BinomialTree:
    """ A binomial tree implementation """
    
    def __init__(self, key, value):
        """ Create a one-node tree. key is the priority of this node """
        self.rank = 0       # tree rank
        self.item = TreeItem(key, value, self)
        self.children = []  # childrens
        self.parent = None  # parent node

    def link(self, other_tree):
        """ Make other_tree the son of self. Both trees must have the same rank
        and other_tree must have a larger minimum priority """
        if self.rank != other_tree.rank:
            raise LinkError()
        if self.item.key > other_tree.item.key:
            raise LinkError()
        self.children.append(other_tree)
        other_tree.parent = self
        self.rank += 1
        
    def decrease(self, newkey):
        """ Reduce the key and updates the tree as needed. """
        node = self
        node.item.key = newkey        
        parent = node.parent
        while parent is not None and node.item.key < parent.item.key:
            parent.item, node.item = node.item, parent.item
            parent.item.tree = parent
            node.item.tree = node
            node = parent
            parent = node.parent
        return node      
        
    def str(self, indent = 0):
        """ Returns a string representation of the tree. """
        return (" " * indent +
                "rank: %d key: %d value: %s" % (self.rank, self.item.key,self.item.value) +
                "\n" + "".join(child.str(indent+2) for child in self.children) )
    
    def __str__(self):
        return self.str()
        

class BinomialHeap:
    """  Implements a Binomial Heap """
    
    def __init__(self, infinity=1e300):
        """ Create an empty Binomial Queue. """
        self.infinity = infinity
        self.parent = self
        self.trees = []
        self.elements = 0        
        self.min_key = self.infinity
        self.min_value = self.infinity
        self.min_tree_rank = -1

    def __capacity(self):
        """ Returns the actual tree's capacity. """
        return 2 ** len(self.trees) - 1

    def __resize(self):
        """ Change the current size of the tree. """
        while self.__capacity() < self.elements:
            self.trees.append(None)

    def __add_tree(self, new_tree):
        """ Insert new_tree into self """
        self.elements = self.elements + 2 ** new_tree.rank
        self.__resize()

        while self.trees[new_tree.rank] is not None:
            if self.trees[new_tree.rank].item.key < new_tree.item.key:
                # swap
                new_tree, self.trees[new_tree.rank] = self.trees[new_tree.rank], new_tree
            r = new_tree.rank
            new_tree.link(self.trees[r])
            self.trees[r] = None

        self.trees[new_tree.rank] = new_tree
        
        if new_tree.item.key <= self.min_key:
            self.min_key = new_tree.item.key
            self.min_value = new_tree.item.value
            self.min_tree_rank = new_tree.rank

    def insert(self, key, value):
        """ Insert key and value into the heap. """
        tree = BinomialTree(key, value)        
        self.__add_tree(tree)
        return tree.item
                   
    def extractmin(self):
        """ Take the minimum element in the heap and remove it. """
        if not self:
            raise EmptyBinomialHeapError()
        
        to_remove = self.trees[self.min_tree_rank]
        self.trees[to_remove.rank] = None
        self.elements = self.elements - 2 ** to_remove.rank        

        for child in to_remove.children:
            child.parent = None
            self.__add_tree(child)
            
        self.min_key = self.infinity
        for tree in self.trees:
            if tree is not None:
                if tree.item.key <= self.min_key:
                    self.min_key = tree.item.key
                    self.min_value = tree.item.value
                    self.min_tree_rank = tree.rank
        
        return to_remove.item
                    
    def decreasekey(self, node, newkey):
        """ Change the node key to newkey. """
        updateref = node.tree.decrease(newkey)
        
        self.min_key = self.infinity
        for tree in self.trees:
            if tree is not None:
                if tree.item.key <= self.min_key:
                    self.min_key = tree.item.key
                    self.min_value = tree.item.value
                    self.min_tree_rank = tree.rank        
        
        return updateref
 
    def __str__(self):
        """ Returns a string representation of the heap. """
        s = """elements: %d min: %s
        min_tree_rank: %d
        tree vector: """ % (self.elements, str(self.min_key), self.min_tree_rank)
        s += " ".join("10"[tree is None] for tree in self.trees)
        s += "\n"
        s += "".join(str(tree) for tree in self.trees if tree is not None)
        return s
        

def test():
    bh1 = BinomialHeap()
    bh1.insert(12,"a")
    bh1.insert(5,"b")
    bh1.insert(21,"c")
    bh1.insert(8,"d")
    iteme = bh1.insert(100,"e")
    print(bh1)
    print("min item: ", bh1.min_value)
    
    print("\n")
    bh1.extractmin()
    print(bh1)
    print("min item: ", bh1.min_value)
    
    bh1.decreasekey(iteme, 1)
    print(bh1)
    
    bh1.extractmin()
    print(bh1)

        
if __name__ == '__main__':
    test()