import networkx as nx
import matplotlib.pyplot as plt
from evolutionary_game_theory import *
from time_series_plots import *
from density_plots import *
from matplotlib.cm import ScalarMappable

def makeClusteringGraph(g):
    gc = g.subgraph(max(nx.connected_components(g)))
    lcc = nx.clustering(gc)
    #cmap = plt.get_cmap('autumn')
    #norm = plt.Normalize(0, max(lcc.values()))
    #node_colors = [cmap(norm(lcc[node])) for node in gc.nodes]
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 4))
    #nx.draw_spring(gc, node_color=node_colors, with_labels=False, ax=ax1)
    #fig.colorbar(ScalarMappable(cmap=cmap, norm=norm), label='Clustering', shrink=0.95, ax=ax1)
    ax2.hist(lcc.values(), bins=10)
    ax2.set_xlabel('Clustering')
    ax2.set_ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def makeDoubleHistogram(G1, G2):
    degree_hist = nx.degree_histogram(G1) 
    degree_hist = np.array(degree_hist, dtype=float)
    degree_prob = degree_hist
    degree_hist2 = nx.degree_histogram(G2) 
    degree_hist2 = np.array(degree_hist2, dtype=float)
    degree_prob2 = degree_hist2
    plt.loglog(np.arange(degree_prob2.shape[0]),degree_prob2,'r.')
    plt.loglog(np.arange(degree_prob.shape[0]),degree_prob,'b.')
    plt.xlabel('Degree (d)')
    plt.ylabel('Frequency')
    plt.title('Degree Distribution')
    plt.show()

G1 = nx.read_edgelist(os.path.normpath(path[0] + "/facebook_combined.txt.gz"), create_using = nx.Graph(), nodetype = int)
G2 = nx.read_edgelist(os.path.normpath(path[0] + "/musae_git_edges.csv"), delimiter=",", create_using = nx.Graph(), nodetype = int)
makeClusteringGraph(G1)
makeClusteringGraph(G2)