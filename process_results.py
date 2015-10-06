import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
             

def graph(df, title, save_file):        
    labels_text = {"kruskal":"Kruskal", "prim":"Prim", "prim_bh":"Prim 2-Heap",
                   "prim_binomial":"Prim Binomial", "prim_fibonacci":"Prim Fibonacci",
                   "prim_th":"Prim 3-Heap"}

    fig, ax = plt.subplots(figsize=(10,7.5))
    
    plt.xticks(fontsize=12)    
    plt.yticks(fontsize=12)
    plt.xlabel("Density", fontsize=16)
    plt.ylabel(r'Time ($\mu$ secs)', fontsize=16)
    plt.title(title, fontsize=18)
    plt.grid(True)
        
    labels = []
    for rank, v in enumerate(df.groupby(["Algorithm"])):    
        algorithm, group = v[0], v[1]
        group_agg = group.groupby(["Density"]).mean()["Time"]        
        ax = group_agg.plot(ax=ax, kind="line", lw=2.5, ms=7, color=tableau20[rank])
        labels.append(labels_text[algorithm])
    
    lines, _ = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='best')
    
    ax.get_figure().savefig(save_file)


def graph_old(df, save_file):
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)

    marker = itertools.cycle(('D', '+', 's', 'o', '*','x'))
    
    fig, ax = plt.subplots(figsize=(10,7.5))
    
    #plt.xticks(range(0, 91, 10), [str(x) + "%" for x in range(0, 91, 10)], fontsize=14)    
    plt.xticks(fontsize=14)    
    plt.yticks(fontsize=14)    
    
    labels = []
    for rank, v in enumerate(df.groupby(["Algorithm"])):    
        algorithm, group = v[0], v[1]
        group_agg = group.groupby(["Density"]).mean()["Time"]        
        ax = group_agg.plot(ax=ax, kind="line", x="Density", y="Time", lw=2.5,
                            marker=next(marker), ms=7, color=tableau20[rank])
        labels.append(algorithm)
    lines, _ = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='best')
    #plt.show()
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
    
    graph(data[data.Edges < 110], "100 Edges", "100.pdf") # 100 edges    
    graph(data[(data.Edges < 1100) & (data.Edges > 110)], "1000 Edges", "1000.pdf") # 1000 edges
    graph(data[(data.Edges < 11000) & (data.Edges > 1100)], "10000 Edges", "10000.pdf") # 10000 edges
    #graph(data[(data.Edges < 110000) & (data.Edges > 11000)], "100000.pdf") # 100000 edges
    #graph(data[(data.Edges < 1100000) & (data.Edges > 110000)], "1000000.pdf") # 1000000 edges
    

if __name__ == '__main__':
    main()