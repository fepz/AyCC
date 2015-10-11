from __future__ import print_function # stderr

import networkx as nx                 # graph library
import binomial_heap as bh            # Binomial heap implementation
import dary_heap as dh                # D-ary heap implementation
import fib_heap as fh                 # Fibonacci heap implementation
import disjoint_set as ds             # Disjoint set implementation
import time                           # Time functions
import glob
import os
import sys
import process_results as pr
from argparse import ArgumentParser   # Command line argument parser

def kruskal(graph, edges=[], sort=False):
    """ Kruskal's algorithm for finding a minimum spanning tree. Implements
    the solution presented at Brassard's `Fundamentals of Algorithms' book. """
    
    mst = [] # list of edges that form the minimum spanning tree
    n = nx.number_of_nodes(graph)

    # list of all the edges in graph, sorted by increasing lenght
    if not edges:
        edges = graph.edges(data=True)        
        if sort:
            edges.sort(key=lambda edge: edge[2]['weight'])

    # Initialize n sets, each containing a different element of N
    uf = ds.DisjointSets(graph.nodes())
    
    while_count = 0
    if_count = 0

    # greedy loop
    tn = 0   # number of edges in the set
    en = 0
    while tn < n - 1:
        while_count += 1
        e = edges[en]
        en += 1
        u = uf.find(e[0])
        v = uf.find(e[1])

        if u != v:
            if_count += 1
            mst.append(e)
            tn += 1
            uf.merge(u, v)

    #print(while_count, if_count, if_count/while_count)

    return mst


def prim(graph):
    """ Prim's algorithm for finding a minimum spanning tree. Implements the 
    Brassard's `Fundamentals of Algorithms' pseudocode, using lists. """
    
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
    

def prim_generic_heap(graph, heap):
    """ Prim's algorithm for finding a minimum spanning tree. It implements the
    solution presented at Brassard's `Fundamentals of Algorithms' book. It uses
    a Heap (concrete implementation by the heap param) and a adjacency matrix. """
    
    # initialization step    
    
    # Obtiene matriz de adyacencia con <inf> en nodos no conectados.
    mx = nx.adjacency_matrix(graph).toarray()
    mx[mx == 0] = 64000                           # Reemplaza ceros por <inf>
    n = nx.number_of_nodes(graph)                 # Número de nodos del grafo

    mst = []

    nearest = [0] * n     # nearest edge to i-node
    mindist = [64000] * n
    heapnode = [None] * n # item in the heap
    
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
        
    
def prim_generic_heap_nx(graph, heap):
    """ Prim's algorithm for finding a minimum spanning tree. It implements the
    solution presented at Brassard's `Fundamentals of Algorithms' book, but uses 
    a Heap instead of a linked-list. The particular heap implementation is user
    defined by the heap param. """

    # initialization step
    mst = [] # list of edges that form the minimum spanning tree
    for node in graph.nodes():        
        graph.node[node]['c_v'] = float("inf")    # cost
        graph.node[node]['e_v'] = None            # edge
        graph.node[node]['heap'] = heap.insert(float("inf"), node)
    
    # greedy loop
    for _ in range(nx.number_of_nodes(graph)):
        # Use heap to obtain minimum edge        
        v = heap.extractmin().value
        
        # the node v is now counted so c_v <- inf to exclude it from neighbors
        graph.node[v]['c_v'] = float("-inf")
        
        # add the edge to the mst if the cost is know
        if graph.node[v]['e_v'] is not None:
            v1 = graph.node[v]['e_v']
            mst.append((v, graph.node[v]['e_v'], {'weight':graph[v][v1]["weight"]}))
        
        # update the weights (costs) of the edges associated with min_node
        for n in graph.neighbors(v):
            if graph[v][n]["weight"] < graph.node[n]['c_v']:
               graph.node[n]['c_v'] = graph[v][n]["weight"]
               graph.node[n]['e_v'] = v
               heap.decreasekey(graph.node[n]['heap'], graph.node[n]['c_v'])

    return mst
    
       
def get_args():
    """ Parse arguments from the command line """
    parser = ArgumentParser()
    parser.add_argument("--graphpath", help="Directory with graphs/results", default=".", type=str)    
    parser.add_argument("--numreps", help="Number of test reps per method", default=10, type=int)
    parser.add_argument("--graph", help="Generate graphs", action="store_true")
    parser.add_argument("--reportgraph", help="Generate report and complete graphs for the report", action="store_true")
    parser.add_argument("--test", help="Run the test", action="store_true")
    return parser.parse_args()
    
    
def test_mst(graph):
    """ Calculates the mst of graph with kruskal and prim. Returns a dictionary
    with the results for each methods: mst, calc time in usecs and number of 
    edges in the mst. """
    results = {}
    clockt = 0
    mst = []

    #clockt = time.clock()
    #mst = nx.minimum_spanning_tree(graph)
    #clockt = time.clock() - clockt
    #tests["kruskal_nx"] = [mst.edges(data=True), clockt]
    
    edges = graph.edges(data=True)
    edges.sort(key=lambda edge: edge[2]['weight'])
    clockt = time.clock()
    mst = kruskal(graph, edges)
    clockt = time.clock() - clockt
    results["kruskal_sorted1"] = [mst, clockt]
    
    clockt = time.clock()
    mst = kruskal(graph, sort=True)
    clockt = time.clock() - clockt
    results["kruskal_sorted2"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim(graph)
    clockt = time.clock() - clockt
    results["prim"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_generic_heap(graph, dh.Heap(2))
    clockt = time.clock() - clockt
    results["prim_2h"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_generic_heap_nx(graph, dh.Heap(2))
    clockt = time.clock() - clockt
    results["prim_2h_nx"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_generic_heap(graph, dh.Heap(3))
    clockt = time.clock() - clockt
    results["prim_3h"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_generic_heap_nx(graph, dh.Heap(3))
    clockt = time.clock() - clockt
    results["prim_3h_nx"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_generic_heap(graph, bh.BinomialHeap())
    clockt = time.clock() - clockt
    results["prim_binomial"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_generic_heap_nx(graph, bh.BinomialHeap())
    clockt = time.clock() - clockt
    results["prim_binomial_nx"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_generic_heap(graph, fh.FibonacciHeap())
    clockt = time.clock() - clockt
    results["prim_fibonacci"] = [mst, clockt]
    
    clockt = time.clock()
    mst = prim_generic_heap_nx(graph, fh.FibonacciHeap())
    clockt = time.clock() - clockt
    results["prim_fibonacci_nx"] = [mst, clockt]
    
    # calculates length and sum weight for each mst
    for method, result in results.items():
        rmst = result[0]
        result.append(len(rmst))
        result.append(sum(edge[2]['weight'] for edge in rmst))
    
    return [nx.number_of_nodes(graph), 
            nx.number_of_edges(graph), 
            nx.density(graph), 
            results]
                    

def main():    
    args = get_args()

    # Output file path
    save_file_path = "{0}/test-result.txt".format(args.graphpath)
    
    if args.test:
        # Search for all the edge files in grappath directory
        edge_files = glob.glob("{0}/*.edgelist".format(args.graphpath))
        
        # Verifies that there are .edgelist files in graphpath
        if not edge_files:
            path_string = "current" if args.graphpath == "." else args.graphpath
            print("Error: No *.edgelist files found in {0} directory!".format(path_string), file=sys.stderr)
            return        
           
        with open(save_file_path, "w") as save_file:        
            save_file.write("Test\tFile\tNodes\tEdges\tDensity\tAlgorithm\tTime\n")
            
            for edge_file in edge_files:            
                print("Testing {0} ...".format(edge_file), file=sys.stdout)
                
                for rep in range(args.numreps):
                    # Read graph from the file
                    graph = nx.read_weighted_edgelist(edge_file, nodetype=int)
    
                    # Test the mst methods
                    result = test_mst(graph)
                    
                    # Verifies that all the methods give the same mst length
                    mst_lengths = []
                    for method, method_results in result[3].items():
                        mst_lengths.append((method, method_results[2]))
                    lmst = mst_lengths[0]
                    for r in mst_lengths[1:]:
                        if r[1] != lmst[1]:
                            print("ERROR!!! {0} |mst|={1}, {2} |mst|={3}".format(lmst[0],lmst[1],r[0],r[1]), file=sys.stderr)                        
                            return
                            
                    # Verifies that all the methods give the same mst weight
                    mst_weights = []
                    for method, method_results in result[3].items():
                        mst_weights.append((method, method_results[3]))
                    wmst = mst_weights[0]
                    for r in mst_weights[1:]:
                        if r[1] != wmst[1]:
                            print("ERROR!!! {0} wmst={1}, {2} wmst={3}".format(wmst[0],wmst[1],r[0],r[1]), file=sys.stderr)                        
                            return                
                    
                    # Write the results into the output file
                    for method, method_results in result[3].items():
                        save_file.write("{0}\t{1}\t{2}\t{3}\t{4:0.1}\t".format(rep, os.path.basename(edge_file), result[0], result[1], result[2]))
                        save_file.write("{0}\t{1}\n".format(method, method_results[1]))
                    save_file.write("\n")
                 
                # Flush last rep results into the output file
                save_file.flush()
            
        # Generate the graphs for this test
        if args.graph:
            print("Generating PDFs...", file=sys.stdout)
            pr.generate_graphs(save_file_path, args.graphpath)
                      
    if args.reportgraph:
        print("Generating PDFs..")
        pr.graphX(args.graphpath)
    
    print("Done!", file=sys.stdout)
        

if __name__ == '__main__':
    main()
