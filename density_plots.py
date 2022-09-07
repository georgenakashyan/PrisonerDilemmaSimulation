"""
This module contains the necessary functions to plot a cooperation density plot
"""

import numpy as np
import matplotlib.pyplot as plt
from evolutionary_game_theory import multi_replica_simulation


def _compute_cooperation_density_matrix(G, x0, steps, replicas, size, beta):
    """
    Compute the average cooperator density of each set contained in the following
     range of parameters T ∈ [0, 2] and S ∈ [-1, 1]
    Parameters
    ----------
    G : nx.Graph
    x0 : float
        Initial density of cooperators
    steps : int
        Number of time-steps
    replicas : int
        Number of replicas to perform
    size : int
        Number of divisions per side, the plot will contain nxn games
    beta : float
        Parameter that models the importance of the difference between payoffs in a game
    Returns
    -------
    Z : array
        Matrix of densities
    """
    matrix = []
    for S in np.linspace(-1, 1, size):
        row = []
        for T in np.linspace(0, 2, size):
            W = np.array([[1, S], [T, 0]])
            row.append(multi_replica_simulation(G, W, steps=steps, x0=x0,
                                                    beta=beta, replicas=replicas))
        matrix.append(row)
    return np.array(matrix)


def _colormesh_coop(Z, title, ax, colorbar=False, saving_path=None):
    """
    Makes the density plot
    Parameters
    ----------
    Z : array
        Matrix of densities
    title : str
        Title of the graph
    ax : ax
    colorbar : bool, default False
        If true plots the color bar
    saving_path : str, optional
        If its given the figure will be saved in the given path
    """
    x = np.linspace(0, 2, Z.shape[0])
    y = np.linspace(-1, 1, Z.shape[1])
    plot = ax.pcolormesh(x, y, Z, cmap='turbo')
    plt.vlines(x=1.0, ymin=-1, ymax=1, colors='k', ls='--', lw=0.75)
    plt.hlines(y=0.0, xmin=0, xmax=2, colors='k', ls='--', lw=0.75)

    plt.title(title)
    plt.xlabel('T')
    plt.ylabel('S')
    if colorbar:
        plt.colorbar(plot)
    if saving_path is not None:
        plt.savefig(saving_path, dpi=300)


def plot_cooperation_density_plot(G, x0, steps, replicas, size, beta, ax, title=None, colorbar=False, saving_path=None):
    """
    Plots the density plot of cooperators
    Parameters
    ----------
    G : nx.Graph
    x0 : float
        Initial density of cooperators
    steps : int
        Number of time-steps
    replicas : int
        Number of replicas to perform
    size : int
        Number of divisions per side, the plot will contain nxn games
    beta : float
        Parameter that models the importance of the difference between payoffs in a game
    title : str
        Title of the graph
    ax : ax
    colorbar : bool, default False
        If true plots the color bar
    saving_path : str, optional
        If its given the figure will be saved in the given path
    """
    Z = _compute_cooperation_density_matrix(G=G, x0=x0, steps=steps, replicas=replicas, size=size, beta=beta)
    _colormesh_coop(Z=Z, title=title, ax=ax, colorbar=colorbar, saving_path=saving_path)