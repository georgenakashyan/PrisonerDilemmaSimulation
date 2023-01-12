"""
This module contains functions to run a simulation of an evolutionary game theory process following
a Fermi rule approximation strategy on a given network.
"""

import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import scipy as sp
from collections import deque

def _count_coop(strategies):
    """
    Counts the portion of nodes with cooperative strategy in the network
    Parameters
    ----------
    strategies : dict
        A dict containing the strategy of each node
    Returns
    -------
    proportion_coop : float
        Proportion of nodes using a cooperative strategy
    """
    length = len(strategies)
    return (length - sum(strategies.values())) / length


def _fermi_updating_rule(wi, wj, beta):
    """
    Returns the probability of individual i adopting individual j strategy
    Parameters
    ----------
    wi : float
        Payoff of individual i
    wj : float
        Payoff of individual j
    beta : float
        Parameter that models the importance of a payoff difference
    Returns
    -------
    pij : float
        Probability of individual i adopting individual j strategy
    """
    return 1 / (1 + np.e ** (-beta * (wj - wi)))


def one_replica_simulation(G, W, steps, x0, beta, choice_factor, stationary=0.9):
    """
    Runs one replica simulation of the evolutionary game theory simulation
    Parameters
    ----------
    G : nx.Graph
    W : array
        Payoff matrix
    steps : int
        Number of epochs to run
    x0 : float
        Proportion of initial nodes using cooperative strategy
    beta : float
        Parameter that models the importance of the difference in Fermi updating rule
    choice_factor : int
        Choice of how nodes will decide to update their strategy
    stationary : float
        Proportion of epochs that correspond to the stationary phase
    Returns
    -------
    p : float
        mean proportion of nodes using cooperative strategy in the stationary phase
    time_series : deque
        time series of the proportion of nodes using cooperative strategy in each time step
    """
    time_series = deque()
    strategy = dict(zip(G.nodes(), np.random.choice([0, 1], len(G.nodes()), p=[x0, 1-x0])))

    for t in range(steps):
        if t > steps * stationary:
            time_series.append(_count_coop(strategy))
        new_strategy = dict()
        payoffs = _compute_all_payoffs(G, W, strategy)
        for i in G.nodes():
            j = random.sample(list(G.neighbors(i)), 1)[0]  # random selected neighbor
            
            if (choice_factor == 1):
                # For updating probability based on payoff difference and beta:
                wi, wj = payoffs.get(i), payoffs.get(j)  # payoffs of each node
            elif (choice_factor == 2):
                # For updating probability based on popularity and beta:
                # ?: backup wi, wj = G.degree(i), G.degree(j)  # edge degrees of each node
                wi, wj = payoffs.get(i), payoffs.get(j)  # payoffs of each node
                beta = len(list(G.neighbors(j)))/len(list(G.nodes))
            pij = _fermi_updating_rule(wi, wj, beta)  # probability of node i to adopt j strategy
            if np.random.random() < pij:
                new_strategy[i] = strategy.get(j)
        strategy.update(new_strategy)  # update strategies
    p = np.mean(time_series)
    return p, time_series


def multi_replica_simulation(G, W, steps, x0, beta, replicas, choice_factor):
    """
    Runs one a given number of  simulation replicas of the evolutionary game theory simulation
    Parameters
    ----------
    G : nx.Graph
    W : array
        Payoff matrix
    steps : int
        Number of epochs to run
    x0 : float
        Proportion of initial nodes using cooperative strategy
    beta : float
        Parameter that models the importance of the difference in Fermi updating rule
    replicas : int
        Number of replicas to execute
    choice_factor : int
        Choice of how nodes will decide to update their strategy
    Returns
    -------
    p_mean : float
        Mean proportion of nodes following a cooperative strategy
    """
    return np.mean([one_replica_simulation(G, W, steps, x0, beta, choice_factor)[0] for _ in range(replicas)])


def _compute_all_payoffs(G, W, strategy):
    """
    Computes the payoffs of each node in the network in a timestep
    Parameters
    ----------
    G : nx.Graph
    W : array
        Matrix payoff
    strategy : dict
        Dict of strategies followed by each node
    Returns
    -------
    payoffs : dict
        Payoffs of the nodes in the network
    """
    payoffs = {node: _get_payoff(G, node, W, strategy) for node in G.nodes}
    return payoffs


def _get_payoff(G, i, W, strategy):
    """
    Gets the payoff of one sample. To obtain the payoff of each node a game between each node and its neighbors is
    simulated knowing each neighbor strategy. One obtained every result of each game is added.
    Parameters
    ----------
    G : nx.Graph
    i : int, tuple, str
        The node of interest to obtain its payoff
    W : array
        Matrix payoff
    strategy : dict
        Dict of strategies followed by each node
    Returns
    -------
    payoff : float
        Payoff of the given node
    """
    payoff = sum([W[strategy.get(i)][strategy.get(j)] for j in G.neighbors(i)])
    return payoff