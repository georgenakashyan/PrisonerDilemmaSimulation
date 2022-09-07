import os
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import moviepy.video.io.ImageSequenceClip
from evolutionary_game_theory import one_replica_simulation, _compute_all_payoffs, _fermi_updating_rule

path = os.path.split(os.path.realpath(__file__))

def _plot_time_serie(G, W, steps, x0, beta, ax, color):
    """
    Plots a single time-series
    Parameters
    ----------
    G : nx.Graph
    W : array
        Payoff matrix
    steps : int
        Numebr of time-steps
    x0 : float
        Initial density of cooperators
    beta : float
        Models the importance of the difference of payoffs in a game
    ax : ax
    color: str
        Color of the plot
    Returns
    -------
    p : float
        Mean density
    """
    p, time_series = one_replica_simulation(G, W, steps, x0, beta, stationary=0.0)
    ax.plot(time_series, c=color)
    return p


def plot_time_series(G, W, steps, x0, beta, games, title, saving_path=True):
    """
    Makes times series plots
    Parameters
    ----------
    G : nx.Graph
    W : array
        Payoff matrix
    steps : int
        Number of steps
    x0 : float
        Initial density of cooperators
    beta : float
        Models the importance of the difference of payoffs in a game
    games : int
        Number of games to run and then graph.
    title : str
        Title of the plot
    saving_path : bool, default True
        If True, the image will be saved
    -------
    means_dict : dict
        Mean proportion of cooperators at every stage
    """
    means_dict = dict()
    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    for T, c in tuple(zip(np.linspace(1, 10, games), mcolors.TABLEAU_COLORS.keys())):
        p = _plot_time_serie(G, W, steps=steps, x0=x0, beta=beta, ax=ax, color=c)
        means_dict[T] = p
    plt.title(title)
    plt.xlabel('Time Steps')
    plt.ylabel('Proportion of Cooperator Nodes')
    if saving_path:
        plt.savefig(os.path.normpath(path[0] + "/reports/figures/time_series/" + title + '.jpeg'), dpi=500)
    return means_dict

def make_simulation_video(G, W, steps, x0, beta, name, fps):
    """
    Makes a video with the simulation evolution of the nodes strategies
    Parameters
    ----------
    G : nx.Graph
    W : array
        Payoff matrix
    steps : int
        Number of steps
    x0 : float
        Initial density of cooperators
    beta : float
        Models the importance of the difference of payoffs in a game
    name : str
        Name of the video
    fps : int
    """
    strategy = dict(zip(G.nodes(), np.random.choice([0, 1], len(G.nodes()), p=[x0, 1 - x0])))

    for t in range(steps):
        ### make plot
        plt.figure(figsize=(10, 10))
        ax = plt.gca()
        my_pos = nx.spring_layout(G, seed = 100)
        nx.draw(G, my_pos, node_size=10, width=0.3, ax=ax, node_color=['red' if s == 0 else 'royalblue' for s in strategy.values()])
        plt.title("Time Step : %02d" %(t+1))
        red_patch = mpatches.Patch(color='red', label='Cooperative Player')
        blue_patch = mpatches.Patch(color='royalblue', label='Non-Cooperative Player')

        plt.legend(handles=[red_patch, blue_patch], loc='lower right')
        savePath = os.path.normpath(path[0] + "/reports/figures/film/%s%02d.png" %(name, t+1))
        print(savePath)
        plt.savefig(savePath, dpi = 500)
        plt.close()
        ###
        new_strategy = dict()
        payoffs = _compute_all_payoffs(G, W, strategy)
        for i in G.nodes():
            j = random.sample(list(G.neighbors(i)), 1)[0]  # random selected neighbor
            wi, wj = payoffs.get(i), payoffs.get(j)  # payoffs of each node
            pij = _fermi_updating_rule(wi, wj, beta)  # probability of node i to adopt j strategy
            if np.random.random() < pij:
                new_strategy[i] = strategy.get(j)
        strategy.update(new_strategy)  # update strategies

    # make video
    image_folder = os.path.normpath(path[0] + "/reports/figures/film")
    print(image_folder)
    image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(sorted(image_files), fps=fps)
    clip.write_videofile(os.path.normpath(path[0] + "/reports/videos/" + name + ".mp4"))