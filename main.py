import networkx as nx
import os as os
from evolutionary_game_theory import *
from time_series_plots import *
from density_plots import *

# input variables
os.system('cls' if os.name == 'nt' else 'clear')
print("[=================== Prisoner's Dilemma Game =======================]")
while True:
	graphChoice = input("\nWhich graph would you like to simulate? (ws for Watts-Strogatz or fb for Facebook): ").lower()
	if (graphChoice == "ws"):
		print("\nNote: Default values for these questions are: 1000 Nodes, 4 Edges Per Node (on average), 10 games, 25 turns, 0.5 Cooperators.")
		nodes = int(input("\nNumber of players/nodes (positive integer): "))
		avgEdgePerNode = int(input("\nNumber of average edges per node (positive integer): "))
		g = nx.watts_strogatz_graph(nodes, avgEdgePerNode, 0.1)
		# *: Updating title to match graph type.
		title = "{0}, {1} Nodes, K={2}".format(graphChoice.upper(), nodes, avgEdgePerNode)
		break
	elif (graphChoice == "fb"):
		print("\nNote: Default values for these questions are: 10 Games, 25 Turns, 0.5 Cooperators.")
		path = os.path.split(os.path.realpath(__file__))
		g = nx.read_edgelist(os.path.normpath(path[0] + "/facebook_combined.txt.gz"), create_using = nx.Graph(), nodetype = int)
		# *: Updating title to match graph type.
		title = "{0}".format(graphChoice.upper())
		break
	else:
		print("\nInvalid choice, type fb for Facebook network or ws for Watts-Strogatz network.")

games = int(input("\nNumber of games to simulate (positive integer): "))
turns = int(input("\nNumber of turns to run each game (positve integer): "))
init_coop = float(input("\nInitial proportion of cooperators to defectors (float between 0 and 1 inclusive): "))
# *: Updating title to show games and turns.
title = "{0}, {1} Games, {2} Turns".format(title, games, turns)

# how players decide to change their strategy
beta = 0
while True:
	choice_factor = int(input("""\nWhat will players base their decision to change their strategy on? (Enter the choice number)
							\n(1) Payoff difference
							\n(2) Popularity difference
							\n"""))
	if (choice_factor == 1):
		beta = float(input("\nImportance of payoff difference (value between 0 and 1 inclusive): "))
		# *: Updating title to show choice factor.
		title = "{0}, Strategy {1}, Beta={2}".format(title, choice_factor, beta)
		break
	if (choice_factor == 2):
		# *: Updating title to show choice factor.
		title = "{0}, Strategy {1}".format(title, choice_factor)
		break

# payoff matrix
# info: b = benefit given by cooperators, c = cost cooperators bear for giving out b
# info: D is defector, C is cooperator. Left is 'i'or the current node, right is 'j' or neighbor node.
# info: Assignment of values: [C:C,C:D], [D:C, D:D]
# info: Values dictated by:   [b-c, -c], [b, 0]
payoff = [[1.5, -0.3], [1.8, 0]]
#payoff = [[9, -0.3], [1.8, 0]]
#payoff = [[2, -0.3], [1.8, 0]]
#payoff = [[2.2, -0.3], [1.8, 0]]
#payoff = [[5, -1], [6, 0]]
#payoff = [[5.7, -0.3], [6, 0]]

# running the simulation and making time series plot
pDict = plot_time_series(g, payoff, turns, init_coop, beta, games, choice_factor, title)
p = sum(pDict.values()) / len(pDict)

# video of evolution
make_simulation_video(g, payoff, turns, init_coop, beta, choice_factor, "Prisoner's Dilemma", 5)