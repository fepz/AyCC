import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
             
labels_text = {"kruskal":"Kruskal", "prim":"Prim", "prim_2h":"Prim 2-Heap",
               "prim_binomial":"Prim Binomial", "prim_fibonacci":"Prim Fibonacci",
               "prim_3h":"Prim 3-Heap", "kruskal_sorted1":"Kruskal (Sorted 1)",
               "kruskal_sorted2":"Kruskal (Sorted 2)",
               "prim_binomial_nx":"Prim Binomial (nx)",
               "prim_2h_nx":"Prim 2-Heap (nx)",
               "prim_3h_nx":"Prim 3-Heap (nx)",
               "prim_fibonacci_nx":"Prim Fibonacci (nx)"}
               
all_methods = list(labels_text.keys())
prim_methods = [m for m in all_methods if m.startswith("prim")]
prim_methods_nx = [m for m in all_methods if m.endswith("_nx")]
kruskal_methods = [m for m in all_methods if m.startswith("kruskal")]

def graph(df, title, save_file, methods=[]):        
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
            group_agg = group.groupby(["Density"]).mean()["Time"]        
            ax = group_agg.plot(ax=ax, kind="line", lw=2.5, ms=7, color=tableau20[rank], label=labels_text[algorithm])
    
    plt.legend(loc="best")
    
    ax.get_figure().savefig(save_file)


def graph2(df):
    """ remove outliers """
    fig, ax = plt.subplots(figsize=(8,6))
    labels = []
    for algorithm, group in df.groupby(["Algorithm"]):
        group = group[np.abs(group.Time - group.Time.mean()) <= (2 * group.Time.std())]
        group_agg = group.groupby(["Density"]).mean()["Time"]    
        ax = group_agg.plot(ax=ax, kind="line", c=algorithm, x="Density", y="Time")
        labels.append(algorithm)
    lines, _ = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='best')
    plt.show()
        
    
def scatter(df):
    for algorithm, data in df.groupby(["Algorithm"]):
        data.plot(kind="scatter", x="Density", y="Time")
    

def main():
    data = pd.read_csv("test-results.txt", sep='\t')
    
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)
    
    # Graph kruskal methods    
    graph(data[data.Edges < 110], "100 Edges - Kruskal", "100K.pdf", kruskal_methods) # 100 edges    
    graph(data[(data.Edges < 1100) & (data.Edges > 110)], "1000 Edges - Kruskal", "1000K.pdf", kruskal_methods) # 1000 edges
    graph(data[(data.Edges < 11000) & (data.Edges > 1100)], "10000 Edges - Kruskal", "10000K.pdf", kruskal_methods) # 10000 edges    
    
    # Graph all Prim methods
    graph(data[data.Edges < 110], "100 Edges - Prim", "100P.pdf", prim_methods) # 100 edges    
    graph(data[(data.Edges < 1100) & (data.Edges > 110)], "1000 Edges - Prim", "1000P.pdf", prim_methods) # 1000 edges
    graph(data[(data.Edges < 11000) & (data.Edges > 1100)], "10000 Edges - Prim", "10000P.pdf", prim_methods) # 10000 edges
    #graph(data[(data.Edges < 110000) & (data.Edges > 11000)], "100000.pdf") # 100000 edges
    #graph(data[(data.Edges < 1100000) & (data.Edges > 110000)], "1000000.pdf") # 1000000 edges
    
    # Graph all Prim methods
    graph(data[data.Edges < 110], "100 Edges - Prim (nx)", "100Pnx.pdf", prim_methods_nx) # 100 edges    
    graph(data[(data.Edges < 1100) & (data.Edges > 110)], "1000 Edges - Prim (nx)", "1000Pnx.pdf", prim_methods_nx) # 1000 edges
    graph(data[(data.Edges < 11000) & (data.Edges > 1100)], "10000 Edges - Prim (nx)", "10000Pnx.pdf", prim_methods_nx) # 10000 edges
    #graph(data[(data.Edges < 110000) & (data.Edges > 11000)], "100000.pdf") # 100000 edges
    #graph(data[(data.Edges < 1100000) & (data.Edges > 110000)], "1000000.pdf") # 1000000 edges
    
    # Graph Prim (nx) methods, Prim and Kruskal
    ppk = []
    ppk.extend(prim_methods_nx)
    ppk.append("kruskal")
    ppk.append("prim")
    graph(data[data.Edges < 110], "100 Edges - Prim (nx)", "100Ppk.pdf", ppk) # 100 edges    
    graph(data[(data.Edges < 1100) & (data.Edges > 110)], "1000 Edges - Prim (nx)", "1000Ppk.pdf", ppk) # 1000 edges
    graph(data[(data.Edges < 11000) & (data.Edges > 1100)], "10000 Edges - Prim (nx)", "10000Ppk.pdf", ppk) # 10000 edges

if __name__ == '__main__':
    main()