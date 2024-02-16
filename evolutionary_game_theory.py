"""
This module contains functions to run a simulation of an evolutionary game theory process following
a Fermi rule approximation strategy on a given network.
"""
import os
import numpy as np
import matplotlib.patches as mpatches
import random
import matplotlib.pyplot as plt
import networkx as nx
import logging
import time
import csv
from decimal import *
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
	# info: This is the output of each matchup with option 2
	# info: beta is assume to be 0.0002588235294
	# info: -- 22 average edges per node / 85000 nodes = 0.0002588235294...
	# *: i: cooperator, j: cooperator   | 0.5 or 50%
	# *: i: cooperator, j: defector		| 0.5001358823 or 50.01358823%
	# *: i: defector, j: cooperator		| 0.4998815882 or 49.98815882%
	# *: i: defector, j: defector		| 0.5 or 50%
	# bug: CANNOT HANDLE LARGE NUMBERS BUT DECIMAL SLOWS DOWN PROGRAM A LOT
	t1 = time.time()
	chance = 1 / (1 + Decimal(np.e) ** Decimal((-beta * (wj - wi))))
	t2 = time.time()
	if (t2 - t1 > 1):
		logging.warning("Chance Time: " + str(t2-t1))
	return chance


def one_replica_simulation(G, W, steps, x0, beta, choice_factor, title):
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
	title : string
		title for video frame filenames
	Returns
	-------
	p : float
		mean proportion of nodes using cooperative strategy
	time_series : deque
		time series of the proportion of nodes using cooperative strategy in each time step
	"""
	# Gets an exact proportion of initial nodes using cooperative strategy
	# Cooperator : 0, Defector : 1
	time_series = deque()
	strategy = dict(zip(G.nodes(), G.nodes()))
	strategy = strategy.fromkeys(strategy, 1)
	coop_nodes = random.sample(list(G.nodes()), int(G.number_of_nodes()*x0))
	coop_dict = dict(zip(coop_nodes, coop_nodes))
	coop_dict = coop_dict.fromkeys(coop_dict, 0)
	strategy.update(coop_dict)
	_make_influence_csv(title + ", Start", strategy, G)

	if (choice_factor == 1):
		for t in range(steps):
			payoffs = _compute_all_payoffs(G, W, strategy)
			print("--Step " + str(t))
			time_series.append(_count_coop(strategy))
			new_strategy = dict()
			for i in G.nodes():
				j_List = list(G.neighbors(i))
				for j in j_List:
					wi, wj = payoffs.get(i), payoffs.get(j)
					pij = _fermi_updating_rule(wi, wj, beta)  # probability of node i to adopt j strategy
					if np.random.random() < pij:
						new_strategy[i] = strategy.get(j)
			strategy.update(new_strategy)  # update strategies
			# TODO: Make this an option in the beginning that can be toggled on or off.
			_decide_to_make_photos(t, steps, G, strategy, title)

	elif (choice_factor == 2):
		for t in range(steps):
			payoffs = _compute_all_payoffs(G, W, strategy)
			print("--Step " + str(t))
			time_series.append(_count_coop(strategy))
			new_strategy = dict()
			for i in G.nodes():
				probj = {}
				j_List = list(G.neighbors(i))
				for j in j_List:
					wi, wj = payoffs.get(i), payoffs.get(j)
					# For updating probability based on payoff difference and beta:
					beta = G.degree(j)/(len(G.nodes)-1)
					pij = _fermi_updating_rule(wi, wj, beta)  # probability of node i to adopt j strategy
					probj[pij] = j
				new_strategy[i] = strategy.get(probj[max(probj)])
			strategy.update(new_strategy)  # update strategies
			# TODO: Make this an option in the beginning that can be toggled on or off.
			_decide_to_make_photos(t, steps, G, strategy, title)
	_make_influence_csv(title + ", End", strategy, G)
	p = np.mean(time_series)
	return p, time_series

def make_simulation_photos(G, strategy, step, title):
	"""
	Makes photos that will be combined to make a video
	Parameters
	----------
	G : nx.Graph
	strategy : dict
		Strategies of all nodes (0 for cooperator, 1 for defector)
	step : int
		Current time step
	title : str
		Name of the photos
	"""
	### make plot
	path = os.path.split(os.path.realpath(__file__))
	title = title + ", Step=" + str(step+1)
	plt.figure(figsize=(10, 10))
	ax = plt.gca()
	my_pos = nx.spring_layout(G, seed = 100)
	nx.draw(G, my_pos, node_size=10, width=0.3, ax=ax, node_color=['red' if s == 0 else 'royalblue' for s in strategy.values()])
	plt.title("Time Step : %02d" %(step+1), fontsize = 24)
	red_patch = mpatches.Patch(color='red', label='Cooperative Player')
	blue_patch = mpatches.Patch(color='royalblue', label='Non-Cooperative Player')
	plt.legend(handles=[red_patch, blue_patch], loc='lower right', fontsize = 16)
	savePath = os.path.normpath(path[0] + "/reports/figures/film/%s.png" %(title))
	plt.savefig(savePath, dpi = 500)
	plt.close()

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

def _decide_to_make_photos(t, steps, G, strategy, title):
	if (t == 0 or (t+1)%(steps/2) == 0 or t == steps-1):
		print("Making photo for timestep " + str(t))
		t1 = time.time()
		make_simulation_photos(G, strategy, t, title)
		t2 = time.time()
		if (t2 - t1 > 1):
			logging.warning("WARNING: Time to make photo at step " + str(t) + ": "+ str(t2-t1))

def _make_influence_csv(title, strategy, G):
	"""
	----------
	title : string
	strategy : dict
	G : nx.Graph
	"""
	with open(title + ", Start" + '.csv', 'w', newline='') as csvfile:
		csvWriter = csv.writer(csvfile, delimiter=',')
		csvWriter.writerow(["Node Number"] + ["Strategy (0 = cooperator, 1 = defector)"] + ["Degree"] + ["Neighbors with same strategy"])
		stratkeys = list(strategy.keys())
		stratvals = list(strategy.values())
		for ci in range(len(G.nodes())-1):
			csv_node = stratkeys[ci]
			csv_strat = stratvals[ci]
			csv_deg = G.degree(stratkeys[ci])
			csv_same_deg = 0
			for csv_neighbors in G.neighbors(stratkeys[ci]): 
				if strategy.get(csv_neighbors) == csv_strat: 
					csv_same_deg += 1
			csvWriter.writerow([csv_node] + [csv_strat] + [csv_deg] + [csv_same_deg])