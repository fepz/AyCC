import networkx as nx
import math
import matplotlib.pyplot as plt

# Code borrowed from http://www.cs.cmu.edu/~ckingsf/class/02713-s13/src/mst.py

# Heap item
class HeapItem(object):
    """Represents an item in the heap"""
    def __init__(self, key, item):
        self.key = key
        self.pos = None
        self.item = item        
        
# Binary heap
class Heap():
    def __init__(self):
        self.heap = []
    
    def siftdown(self, node, pos):
        """ Move node down in the tree; restore heap condition after deletion or replacement. """
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

    def deletemin(self):
        """Delete the smallest item"""
        if len(self.heap) == 0: 
            return None
        i = self.heap[0]
        last = self.heap[-1]
        del self.heap[-1]
        if len(self.heap) > 0:
            self.siftdown(last, 0)
        return i

    def insert(self, key, item):
        """Insert an item into the heap"""
        self.heap.append(None)
        hi = HeapItem(key,item)
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
        return int(math.ceil(pos / 2) - 1)

    def children(self, pos):
        """Return a list of children of pos"""
        return range(2 * pos + 1, min(2 * (pos + 1) + 1, len(self.heap)))

    def minchild(self, pos):
        """Return the child of pos with the smallest key"""
        minpos = minkey = None
        for c in self.children(pos):
            if minkey == None or self.heap[c].key < minkey:
                minkey, minpos = self.heap[c].key, c
        return minpos
        
    def count(self):
        return len(self.heap)
        

# Union-find
class UnionFind:
    def __init__(self, G):
        self.group = dict((s, s) for s in G)    # group[s] = IDs of its set
        self.size = dict((s,1) for s in G)      # size[s] = size of set s
        self.items = dict((s,[s]) for s in G)   # items[s] = list of items in set s
        
    def find(self, s):
        """ return the id for the group containing s """
        return self.group[s]
        
    def union(self, a, b):
        """ union of two sets a and b """
        assert a in self.items and b in self.items
        
        # make a the smaller set
        if self.size[a] > self.size[b]:
            a, b = b, a
            
        # put the smaller set items into the bigger set
        for s in self.items[a]:
            self.group[s] = b
            self.items[b].append(s)
            
        # increase the size of b by the size of a
        self.size[b] += self.size[a]
        
        # remove the set a, in order to save memory
        del self.size[a]
        del self.items[a]
        

def kruskal(graph):
    # list of edges that form the minimum spanning tree
    mst = []
    
    # list of all the edges in graph, ordered by weight
    edges = graph.edges(data=True)
    edges.sort(key=lambda edge: edge[2]['weight'])
    
    # cretes the union-find data structure
    uf = UnionFind(graph.nodes())
    
    # greedy loop
    for e in edges:
        u = uf.find(e[0])
        v = uf.find(e[1])
        
        if u != v:
            mst.append(e)
            uf.union(u, v)
    
    return mst
    
    
def prim(graph):
    """ uses a whatever networkx uses to keep track of the nodes that still 
    don't belong to the mst """
    # list of edges that form the minimum spanning tree
    mst = []
    
    # initialization step
    for node in graph.nodes():
        graph.node[node]['choosed'] = False       # node already added to B?
        graph.node[node]['c_v'] = float("inf")    # cost
        graph.node[node]['e_v'] = None            # edge
    
    # greedy loop
    for _ in range(graph.number_of_nodes()):
        # choose minimum lenght edge
        min_dist = float("inf")
        min_node = None
        for snode in graph.nodes():
            if graph.node[snode]['choosed'] is False:
                if graph.node[snode]['c_v'] <= min_dist:
                    min_dist = graph.node[snode]['c_v']
                    min_node = snode
                    
        # add selected node to the forest (B)
        graph.node[min_node]['choosed'] = True
        
        # add the edge to the mst if the cost is know
        if graph.node[min_node]['e_v'] is not None:
            mst.append((min_node, graph.node[min_node]['e_v']))
        
        # update the weights (costs) of the edges associated with min_node
        for n in graph.neighbors(min_node):
            if graph.node[n]['choosed'] is False:                
                if graph[min_node][n]["weight"] < graph.node[n]['c_v']:
                    graph.node[n]['c_v'] = graph[min_node][n]["weight"]
                    graph.node[n]['e_v'] = min_node
                
    return mst            
    
    
def prim2(graph):
    """ uses heap """
   
    # list of edges that form the minimum spanning tree
    mst = []

    heap = Heap()
    
    # initialization step
    for node in graph.nodes():        
        graph.node[node]['c_v'] = float("inf")    # cost
        graph.node[node]['e_v'] = None            # edge
        graph.node[node]['heap'] = heap.insert(graph.node[node]['c_v'], node)
    
    # initial arbitrary node
    item = heap.deletemin()
    
    # greedy loop
    while item is not None:
        v = item.item
        
        # the node v is now counted so c_v <- inf to exclude it from neighbors
        graph.node[v]['c_v'] = float("-inf")
        
        # add the edge to the mst if the cost is know
        if graph.node[v]['e_v'] is not None:
            mst.append((v, graph.node[v]['e_v']))
        
        # update the weights (costs) of the edges associated with min_node
        for n in graph.neighbors(v):
            if graph[v][n]["weight"] < graph.node[n]['c_v']:
               graph.node[n]['c_v'] = graph[v][n]["weight"]
               graph.node[n]['e_v'] = v
               heap.decreasekey(graph.node[n]['heap'], graph.node[n]['c_v'])                      
               
        # next
        item = heap.deletemin()
                
    return mst
    
    
def draw(graph, mst):
    pos = nx.circular_layout(graph)

    # nodos
    nx.draw_networkx_nodes(graph, pos, node_size=1000)

    # arcos
    nx.draw_networkx_edges(graph, pos, edge_color='black')
    nx.draw_networkx_edges(graph, pos, edgelist=mst, width=5, edge_color='g')

    # etiquetas
    nx.draw_networkx_labels(graph, pos)    
    edge_labels = {e[0:2]:'{}'.format(e[2]['weight']) for e in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    plt.axis('off')
    plt.show()
    

def main():
    G = nx.Graph()    
    G.add_weighted_edges_from([("1","2",1), ("2","3",2), ("4","5",3), ("5","6",8),
                               ("6","7",3), ("1","4",4), ("2","5",4), ("3","6",6),
                               ("5","7",7), ("4","2",6), ("5","3",5), ("4","7",4) ])
    
    draw(G, kruskal(G))
    draw(G, prim(G))
    draw(G, prim2(G))
    
    kruskal_mst = kruskal(G)
    prim_mst = prim(G)
    prim2_mst = prim2(G)    

    print(kruskal_mst)
    print(prim_mst)
    print(prim2_mst)

    sum = 0
    for i in prim_mst:
        sum = sum + G[i[0]][i[1]]['weight']
    print(sum)
    sum = 0

    for i in prim2_mst:
        sum = sum + G[i[0]][i[1]]['weight']
    print(sum)

    sum = 0
    for i in kruskal_mst:
        sum = sum + G[i[0]][i[1]]['weight']
    print(sum)
    
if __name__ == '__main__':
    main()
    