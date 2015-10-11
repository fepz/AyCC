import pandas as pd
import matplotlib.pyplot as plt

# Labels
labels_text = {"kruskal_sorted1":"Kruskal (KS1)",
               "kruskal_sorted2":"Kruskal (KS2)",
               "prim":"PrimArr", 
               "prim_2h":"Prim2H (A)", #Prim 2-Heap
               "prim_3h":"Prim3H (A)", #Prim 3-Heap
               "prim_binomial":"PrimBi (A)", # Binomial
               "prim_fibonacci":"PrimFib (A)", # Fibonacci                   
               "prim_binomial_nx":"PrimBi",
               "prim_2h_nx":"Prim2H",
               "prim_3h_nx":"Prim3H",
               "prim_fibonacci_nx":"PrimFib"}
               
all_methods = list(labels_text.keys())
prim_methods = [m for m in all_methods if m.startswith("prim")]
prim_methods_nx = [m for m in all_methods if m.endswith("_nx")]
kruskal_methods = [m for m in all_methods if m.startswith("kruskal")]

def graph(df, title, save_file, methods=[], colors=[], variant="Density", log=False):
    fig, ax = plt.subplots(figsize=(10,7.5))
    
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel("Density", fontsize=16)
    plt.ylabel(r'Time (secs)', fontsize=16)
    plt.title(title, fontsize=18)
    plt.grid(True)
    
    if log:
        plt.xscale("log")
        plt.yscale("log")
        
    for rank, v in enumerate(df.groupby(["Algorithm"])):
        algorithm, group = v[0], v[1]
        if algorithm in methods:
            group_agg = group.groupby([variant]).mean()["Time"]        
            group_agg.plot(ax=ax, kind="line", lw=2.5, ms=7, color=colors[rank], label=labels_text[algorithm])
    
    plt.legend(loc="best")
    plt.savefig(save_file)
    
    plt.close(fig)
        
            
def generate_simple_report(file, save_file_path, methods=[]):   
    """ Generate a simple report """    
    import numpy as np
    data = pd.read_csv(file, sep='\t')
    with open(save_file_path, "w") as save_file:        
        for k, v in data.groupby(["Algorithm"]):
            save_file.write(labels_text[k])
            save_file.write(v.groupby(["Density"])["Time"].agg([len, np.mean, np.std, np.max, np.min]))
            

def generate_simple_report_csv(file, save_file_path):
    """ Generate a CSV report. """
    data = pd.read_csv(file, sep='\t')
    data1 = data.groupby(["Algorithm","Density"])["Time"].describe().unstack()
    data1.to_csv(save_file_path)
        
        
def generate_graphs(file, save_path):
    """ Graph results in file. """
    data = pd.read_csv(file, sep='\t')
    generate_graphs2(data, save_path)
    
#    # These are the "Tableau 20" colors as RGB.
#    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
#                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
#                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
#                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
#                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]                
#    
#    # Scale the RGB values to the [0, 1] range, which is the format matplotlib 
#    # accepts.    
#    for i in range(len(tableau20)):    
#        r, g, b = tableau20[i]    
#        tableau20[i] = (r / 255., g / 255., b / 255.)
#        
#    graph(data, "Kruskal", "{0}/kruskal.pdf".format(save_path), kruskal_methods, tableau20)
#    graph(data, "Prim", "{0}/prim.pdf".format(save_path), prim_methods, tableau20)
#    graph(data, "Prim (nx)", "{0}/primnx.pdf".format(save_path), prim_methods_nx, tableau20)
#    
#    # Graph Prim (nx) methods, Prim and Kruskal
#    ppk = []
#    ppk.extend(prim_methods_nx)
#    ppk.append("kruskal_sorted1")
#    ppk.append("kruskal_sorted2")
#    ppk.append("prim")
#    graph(data, "PPK", "{0}/ppk.pdf".format(save_path), ppk, tableau20)
    
    
def generate_graphs2(data, save_path, filename_prefix=""):
    # These are the "Tableau 20" colors as RGB.
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]                
    
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib 
    # accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)
        
    graph(data, "Kruskal", "{0}/{1}kruskal.pdf".format(save_path,filename_prefix), kruskal_methods, tableau20)
    graph(data, "Prim (A)", "{0}/{1}primA.pdf".format(save_path,filename_prefix), prim_methods, tableau20)
    graph(data, "Prim", "{0}/{1}prim.pdf".format(save_path,filename_prefix), prim_methods_nx, tableau20)
    
    # Graph Prim (nx) methods, Prim and Kruskal
    ppk = []
    ppk.extend(prim_methods_nx)
    ppk.append("kruskal_sorted1")
    ppk.append("kruskal_sorted2")
    ppk.append("prim")
    graph(data, "Prim & Kruskal", "{0}/{1}pk.pdf".format(save_path, filename_prefix), ppk, tableau20)    
    
    
def generate_graphs_by_density(path):
    import os
    import os.path
    
    # These are the "Tableau 20" colors as RGB.
    tableau20 = [(174, 199, 232), (255, 127, 14), (31, 119, 180), (255, 187, 120),    
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]                
    
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib 
    # accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)

    # Iterate over each subdir in path, and add any test-result file to the 
    # data-frame df
    dfs = []    
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.startswith("test-result")]:            
            dfs.append(pd.read_csv(dirpath+"\\"+filename, sep='\t'))            
    df = pd.concat(dfs)

    kruskal_heap = ["kruskal_sorted1", "kruskal_sorted2","prim_2h_nx","prim_3h_nx","prim_binomial_nx","prim_fibonacci_nx"]        

    # Graph Prim (nx) methods, Prim and Kruskal -- all densities
    graph(df, "Edges", "{0}/edges.pdf".format(path), kruskal_heap, tableau20, variant="Edges", log=True)
    
    # One graph for each density
    for rank, v in enumerate(df.groupby(["Density"])):
        density, group = v[0], v[1]
        graph(group, "Density {0}".format(str(density)), "{0}/Cruces/{1}_pc.pdf".format(path,str(density)), kruskal_heap, tableau20, variant="Edges", log=True)
        
        
def graphX(path):
    import os
    import os.path
    
    # These are the "Tableau 20" colors as RGB.
    tableau20 = [(174, 199, 232), (255, 127, 14), (31, 119, 180), (255, 187, 120),    
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]                
    
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib 
    # accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)

    # Iterate over each subdir in path, and add any test-result file to the 
    # data-frame df
    dfs = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.startswith("test-result")]:            
            dfs.append(pd.read_csv(dirpath+"\\"+filename, sep='\t'))            
    df = pd.concat(dfs)

    kruskal_heap = ["kruskal_sorted1", "kruskal_sorted2","prim_2h_nx","prim_3h_nx","prim_binomial_nx","prim_fibonacci_nx"]        

    # Graph Prim (nx) methods, Prim and Kruskal -- all densities
    graph(df, "Edges", "{0}/edges.pdf".format(path), kruskal_heap, tableau20, variant="Edges", log=True)
    
    # One graph for each density
    for rank, v in enumerate(df.groupby(["Density"])):
        density, group = v[0], v[1]
        graph(group, "Density {0}".format(str(density)), "{0}/{1}-cruce-pk.pdf".format(path,str(density)), kruskal_heap, tableau20, variant="Edges", log=True)
        
    # Graphs by number of edges
    df_100 = df[df["File"].str.contains("graph_100_")]
    df_1000 = df[df["File"].str.contains("graph_1000_")]
    df_10000 = df[df["File"].str.contains("graph_10000_")]
    df_100000 = df[df["File"].str.contains("graph_100000_")]
    df_1000000 = df[df["File"].str.contains("graph_1000000_")]
    
    generate_graphs2(df_100, path, "100-")
    generate_graphs2(df_1000, path, "1000-")
    generate_graphs2(df_10000, path, "10000-")
    generate_graphs2(df_100000, path, "100000-")   
    generate_graphs2(df_1000000, path, "1000000-")
    
    
    

