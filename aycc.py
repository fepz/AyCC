import networkx as nx                 # graph library
import binomial_heap as bh            # Binomial heap implementation
import dary_heap as dh                # D-ary heap implementation
import fib_heap as fh                 # Fibonacci heap implementation
import disjoint_set as ds             # Disjoint set implementation
import time                           # Time functions
import glob
import os
from argparse import ArgumentParser   # Command line argument parser


def kruskal(graph):
    """ Kruskal's algorithm for finding a minimum spanning tree. Implements
    the solution presented at Brassard's `Fundamentals of Algorithms' book. """
    
    mst = [] # list of edges that form the minimum spanning tree
    n = nx.number_of_nodes(graph)

    # list of all the edges in graph, sorted by increasing lenght
    edges = graph.edges(data=True)
    edges.sort(key=lambda edge: edge[2]['weight'])

    # Initialize n sets, each containing a different element of N
    uf = ds.DisjointSets(graph.nodes())

    # greedy loop
    tn = 0   # number of edges in the set
    en = 0
    while tn < n - 1:
        e = edges[en]
        en += 1
        u = uf.find(e[0])
        v = uf.find(e[1])

        if u != v:
            mst.append(e)
            tn += 1
            uf.merge(u, v)

    return mst


def prim(graph):
    """ Prim's algorithm for finding a minimum spanning tree. Implements the
    solution presented at Brassard's `Fundamentals of Algorithms' book. It uses
    linked lists. """
    
    # Obtiene matriz de adyacencia con <inf> en nodos no conectados.
    mx = nx.adjacency_matrix(graph).toarray()
    mx[mx == 0] = 64000                           # Reemplaza ceros por <inf>
    n = nx.number_of_nodes(graph)                 # Número de nodos del grafo.
    
    mst = []

    nearest = [0] * (n + 1)
    mindist = mx[:,0]

    # greedy loop
    for _ in range(n - 1):
        mini = 64000

        # minimum edge search
        for j in range(1, n):
            if 0 <= mindist[j] and mindist[j] < mini:
                mini = mindist[j]
                k = j

        mst.append((nearest[k]+1, k+1, graph.get_edge_data(nearest[k]+1, k+1)))
        mindist[k] = -1

        for j in range(1, n):
            if mx[j,k] < mindist[j]:
                mindist[j] = mx[j, k]
                nearest[j] = k

    return mst
    

def prim_heap(graph, dary):
    """ Prim's algorithm for finding a minimum spanning tree. It implements the
    solution presented at Brassard's `Fundamentals of Algorithms' book, but uses 
    a d-ary Heap instead of a linked-list. """
    
    # initialization step    
    
    mx = nx.adjacency_matrix(graph).toarray() # adjacency matrix
    mx[mx == 0] = 64000                       # Reemplaza ceros por <inf>
    n = nx.number_of_nodes(graph)             # Número de nodos del grafo

    mst = []

    nearest = [0] * n     # nearest edge to i-node
    mindist = [64000] * n
    heapnode = [None] * n # item in the heap
    
    # create d-ary heap initialized with the first node
    heap = dh.Heap(dary)
    heapnode[0] = heap.insert(mindist[0], 0)
    
    # greedy loop
    for _ in range(n):
        # Use heap to obtain minimum edge
        k = heap.deletemin().item
        
        mindist[k] = -1
        if graph.get_edge_data(nearest[k]+1, k+1) is not None:
            mst.append((nearest[k]+1, k+1, graph.get_edge_data(nearest[k]+1, k+1)))
        
        for j in range(1, n):
            if mx[j,k] <= mindist[j]:
                mindist[j] = mx[j, k] # cost
                nearest[j] = k        # edge
                # update heap
                if heapnode[j] is None:
                    heapnode[j] = heap.insert(mindist[j], j)                 
                else:
                    heap.decreasekey(heapnode[j], mindist[j])

    return mst


def prim_binomial_heap(graph):
    """ Prim's algorithm for finding a minimum spanning tree. It implements the
    solution presented at Brassard's `Fundamentals of Algorithms' book, but uses 
    a Binomial Heap instead of a linked-list. """
    
    # initialization step    
    
    # Obtiene matriz de adyacencia con <inf> en nodos no conectados.
    mx = nx.adjacency_matrix(graph).toarray()
    mx[mx == 0] = 64000                           # Reemplaza ceros por <inf>
    n = nx.number_of_nodes(graph)                 # Número de nodos del grafo

    mst = []

    nearest = [0] * n     # nearest edge to i-node
    mindist = [64000] * n
    heapnode = [None] * n # item in the heap
    
    # create d-ary heap initialized with the first node
    heap = bh.BinomialHeap(infinity=64000)
    heapnode[0] = heap.insert(mindist[0],0)
    
    # greedy loop
    for _ in range(n):
        # Use heap to obtain minimum edge        
        k = heap.extractmin().value
        
        mindist[k] = -1
        if graph.get_edge_data(nearest[k]+1, k+1) is not None:
            mst.append((nearest[k]+1, k+1, graph.get_edge_data(nearest[k]+1, k+1)))
        
        for j in range(1, n):
            if mx[j,k] < mindist[j]:
                mindist[j] = mx[j, k] # cost
                nearest[j] = k        # edge
                if heapnode[j] is None:
                    heapnode[j] = heap.insert(mindist[j], j)
                else:                    
                    heap.decreasekey(heapnode[j], mindist[j])

    return mst
    
    
def prim_fibonacci_heap(graph):
    """ Prim's algorithm for finding a minimum spanning tree. It implements the
    solution presented at Brassard's `Fundamentals of Algorithms' book, but uses 
    a Fibonacci Heap instead of a linked-list. """
    
    # initialization step    
    
    # Obtiene matriz de adyacencia con <inf> en nodos no conectados.
    mx = nx.adjacency_matrix(graph).toarray()
    mx[mx == 0] = 64000                           # Reemplaza ceros por <inf>
    n = nx.number_of_nodes(graph)                 # Número de nodos del grafo

    mst = []

    nearest = [0] * n     # nearest edge to i-node
    mindist = [64000] * n
    heapnode = [None] * n # item in the heap
    
    # create d-ary heap initialized with the first node
    heap = fh.FibonacciHeap()
    heapnode[0] = heap.insert(mindist[0],0)
    
    # greedy loop
    for _ in range(n):
        # Use heap to obtain minimum edge
        k = heap.extractmin().value
        
        mindist[k] = -1
        if graph.get_edge_data(nearest[k]+1, k+1) is not None:
            mst.append((nearest[k]+1, k+1, graph.get_edge_data(nearest[k]+1, k+1)))
        
        for j in range(1, n):
            if mx[j,k] < mindist[j]:
                mindist[j] = mx[j, k] # cost
                nearest[j] = k        # edge
                if heapnode[j] is None:
                    heapnode[j] = heap.insert(mindist[j], j)
                else:                    
                    heap.decreasekey(heapnode[j], mindist[j])

    return mst
    
       
def get_args():
    """ Parse arguments from the command line """
    parser = ArgumentParser()
    parser.add_argument("--graphpath", help="Directory with graphs", default=".", type=str)    
    parser.add_argument("--numreps", help="Number of test reps per method", default=10, type=int)
    return parser.parse_args()
    
    
def test_mst(graph):
    tests = {}
    clockt = 0
    mst = []

    #clockt = time.clock()
    #mst = nx.minimum_spanning_tree(graph)
    #clockt = time.clock() - clockt
    #tests["kruskal_nx"] = [mst.edges(data=True), clockt]
    
    clockt = time.clock()
    mst = kruskal(graph)
    clockt = time.clock() - clockt
    tests["kruskal"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim(graph)
    clockt = time.clock() - clockt
    tests["prim"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_heap(graph, 2)
    clockt = time.clock() - clockt
    tests["prim_bh"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_heap(graph, 3)
    clockt = time.clock() - clockt
    tests["prim_th"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_binomial_heap(graph)
    clockt = time.clock() - clockt
    tests["prim_binomial"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_fibonacci_heap(graph)
    clockt = time.clock() - clockt
    tests["prim_fibonacci"] = [mst, clockt]
    
    return [nx.number_of_nodes(graph), 
            nx.number_of_edges(graph), 
            nx.density(graph), 
            tests]
                    

def main():    
    args = get_args()
    
    graph_path = args.graphpath

    # save file path
    save_file_path = "test-results.txt"
    
    # search for all the edge files in directory
    edge_files = glob.glob("{0}/*.edgelist".format(graph_path))
       
    with open(save_file_path, "w") as save_file:
        
        save_file.write("Test\tFile\tNodes\tEdges\tDensity\tAlgorithm\tTime\n")
        
        for edge_file in edge_files:
            
            print("Testing {0} ...".format(edge_file))
            
            for rep in range(args.numreps):
                # read the graph from the file
                graph = nx.read_weighted_edgelist(edge_file, nodetype=int)

                # test methods
                result = test_mst(graph)
                
                # save results
                for method, method_results in result[3].items():
                    save_file.write("{0}\t{1}\t{2}\t{3}\t{4:0.1}\t".format(rep, os.path.basename(edge_file), result[0], result[1], result[2]))
                    save_file.write("{0}\t{1}\n".format(method, method_results[1]))
                save_file.write("\n")
                
            save_file.flush()
                
    print("Done!")
        

if __name__ == '__main__':
    main()
