import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def graph(df):
    fig, ax = plt.subplots(figsize=(8,6))
    labels = []
    for algorithm, group in df.groupby(["Algorithm"]):    
        group_agg = group.groupby(["Density"]).mean()["Time"]        
        ax = group_agg.plot(ax=ax, kind="line", x="Density", y="Time")
        labels.append(algorithm)
    lines, _ = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='best')
    plt.show()


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
    
    graph(data[data.Edges < 110]) # 100 edges    
    graph(data[(data.Edges < 1100) & (data.Edges > 110)]) # 1000 edges
    graph(data[(data.Edges < 11000) & (data.Edges > 1100)]) # 10000 edges
    

if __name__ == '__main__':
    main()