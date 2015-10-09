import pandas as pd
import matplotlib.pyplot as plt

# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Labels
labels_text = {"kruskal":"Kruskal (no sorted)", 
               "kruskal_sorted1":"Kruskal (sorted 1)",
               "kruskal_sorted2":"Kruskal (sorted 2)",
               "prim":"Prim", 
               "prim_2h":"Prim 2-Heap",
               "prim_3h":"Prim 3-Heap",
               "prim_binomial":"Prim Binomial", 
               "prim_fibonacci":"Prim Fibonacci",                   
               "prim_binomial_nx":"Prim Binomial (nx)",
               "prim_2h_nx":"Prim 2-Heap (nx)",
               "prim_3h_nx":"Prim 3-Heap (nx)",
               "prim_fibonacci_nx":"Prim Fibonacci (nx)"}
               
all_methods = list(labels_text.keys())
prim_methods = [m for m in all_methods if m.startswith("prim")]
prim_methods_nx = [m for m in all_methods if m.endswith("_nx")]
kruskal_methods = [m for m in all_methods if m.startswith("kruskal")]


def graph(df, title, save_file, methods=[], colors=[], variant="Density"):
    if not colors:
        colors = tableau20
       
    fig, ax = plt.subplots(figsize=(10,7.5))
    
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel("Density", fontsize=16)
    plt.ylabel(r'Time ($\mu$ secs)', fontsize=16)
    plt.title(title, fontsize=18)
    plt.grid(True)
        
    for rank, v in enumerate(df.groupby(["Algorithm"])):
        algorithm, group = v[0], v[1]
        if algorithm in methods:
            group_agg = group.groupby([variant]).mean()["Time"]        
            group_agg.plot(ax=ax, kind="line", lw=2.5, ms=7, color=colors[rank], label=labels_text[algorithm])
    
    plt.legend(loc="best")
    plt.savefig(save_file)
    
    plt.close(fig)
        
    
def scatter(df):
    for algorithm, data in df.groupby(["Algorithm"]):
        data.plot(kind="scatter", x="Density", y="Time")
        
        
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
        
    graph(data, "Kruskal", "{0}/kruskal.pdf".format(save_path), kruskal_methods, tableau20)
    graph(data, "Prim", "{0}/prim.pdf".format(save_path), prim_methods, tableau20)
    graph(data, "Prim (nx)", "{0}/primnx.pdf".format(save_path), prim_methods_nx, tableau20)
    
    # Graph Prim (nx) methods, Prim and Kruskal
    ppk = []
    ppk.extend(prim_methods_nx)
    ppk.append("kruskal")
    ppk.append("prim")
    graph(data, "PPK", "{0}/ppk.pdf".format(save_path), ppk, tableau20)    
    