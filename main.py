import networkx as nx
import os as os
from evolutionary_game_theory import *
from time_series_plots import *
from density_plots import *

# input variables
os.system('cls' if os.name == 'nt' else 'clear')
print("[=================== Prisoner's Dilemma Game =======================]")
while True:
	graphChoice = input("\nWhich graph would you like to simulate? (ws for Watts-Strogatz, fb for Facebook, bfb for Big Facebook, gh for GitHub, or 2d for two dimensional grid): ").lower()
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
	elif (graphChoice == "bfb"):
		print("\nNote: Default values for these questions are: 10 Games, 25 Turns, 0.5 Cooperators.")
		path = os.path.split(os.path.realpath(__file__))
		g = nx.read_edgelist(os.path.normpath(path[0] + "/BFacebook.csv"), delimiter=",", create_using = nx.Graph(), nodetype = int)
		# *: Updating title to match graph type.
		title = "{0}".format(graphChoice.upper())
		break
	elif (graphChoice == "gh"):
		print("\nNote: Default values for these questions are: 10 Games, 25 Turns, 0.5 Cooperators.")
		path = os.path.split(os.path.realpath(__file__))
		g = nx.read_edgelist(os.path.normpath(path[0] + "/musae_git_edges.csv"), delimiter=",", create_using = nx.Graph(), nodetype = int)
		# *: Updating title to match graph type.
		title = "{0}".format(graphChoice.upper())
		break
	elif (graphChoice == "2d"):
		print("\nNote: Default values for these questions are: 2 Nodes, 10 games, 25 turns, 0.5 Cooperators.")
		nodes = int(input("\nNumber of players/nodes (positive integer): "))
		g = nx.grid_2d_graph(nodes, nodes)
		title = "{0}".format(graphChoice.upper())
		break
	else:
		print("\nInvalid choice")

games = int(input("\nNumber of games to simulate (positive integer): "))
turns = int(input("\nNumber of turns to run each game (positve integer): "))
init_coop = float(input("\nInitial proportion of cooperators to defectors (float between 0 and 1 inclusive): "))
# *: Updating title to show games and turns.
title = "{0}, {1} Games, {2} Turns".format(title, games, turns)

# How players decide to change their strategy
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
	elif (choice_factor == 2):
		# *: Updating title to show choice factor.
		title = "{0}, Strategy {1}".format(title, choice_factor)
		break
	else:
		print("\nInvalid choice")

# Choosing which payoff matrix
# info: b = benefit given by cooperators, c = cost cooperators bear for giving out b
# info: D is defector, C is cooperator. Left is 'i'or the current node, right is 'j' or neighbor node.
# info: Assignment of values: [C:C,C:D], [D:C, D:D]
# info: Values dictated by:   [b-c, -c], [b, 0]
while True:
	payoff_factor = str(input("""\nChoose your payoff matrix
							\n(ws) Watts-Strogatz's Normal Payoff - [[1.5, -0.3], [1.8, 0]]
							\n(fb) Facebook's Normal Payoff - [[14.5, -0.5], [15, 0]]
							\n(gh) GitHub's Normal Payoff - [[2.7, -0.3], [3, 0]]
							\n(gh_new) GitHub's NEW Payoff - [[14.7, -0.3], [15, 0]]
							\n(gh_k15) GitHub's k15 Payoff - [[4.2, -0.3], [4.5, 0]]
							\n(gh_k12) GitHub's k12 Payoff - [[3.3, -0.3], [3.6, 0]]
							\n(gh_k55) GitHub's k55 Payoff - [[16.2, -0.3], [16.5, 0]]
							\n(gh_k60) GitHub's k60 Payoff - [[17.7, -0.3], [18, 0]]
							\n(gh_k65) GitHub's k65 Payoff - [[19.2, -0.3], [19.5, 0]]
							\n(gh_k70) GitHub's k70 Payoff - [[20.7, -0.3], [21, 0]]
							\n(gh_k75) GitHub's k75 Payoff - [[22.2, -0.3], [22.5, 0]]
							\n"""))
	if (payoff_factor == "ws"):
		payoff = [[1.5, -0.3], [1.8, 0]]
		break
	elif (payoff_factor == "fb"):
		payoff = [[14.5, -0.5], [15, 0]]
		break
	elif (payoff_factor == "gh"):
		payoff = [[2.7, -0.3], [3, 0]]
		break
	elif (payoff_factor == "gh_new"):
		payoff = [[14.7, -0.3], [15, 0]]
		break
	elif (payoff_factor == "gh_k15"):
		payoff = [[4.2, -0.3], [4.5, 0]]
		break
	elif (payoff_factor == "gh_k12"):
		payoff = [[3.3, -0.3], [3.6, 0]]
		break
	elif (payoff_factor == "gh_k55"):
		payoff = [[16.2, -0.3], [16.5, 0]]
		break
	elif (payoff_factor == "gh_k60"):
		payoff = [[17.7, -0.3], [18, 0]]
		break
	elif (payoff_factor == "gh_k65"):
		payoff = [[19.2, -0.3], [19.5, 0]]
		break
	elif (payoff_factor == "gh_k70"):
		payoff = [[20.7, -0.3], [21, 0]]
		break
	elif (payoff_factor == "gh_k75"):
		payoff = [[22.2, -0.3], [22.5, 0]]
		break
	else:
		print("\nInvalid choice")

title = title + ", " + payoff_factor + " payoff"
# running the simulation and making time series plot
p_arr = plot_time_series(g, payoff, turns, init_coop, beta, games, choice_factor, title)
p = np.mean(p_arr)

# video of evolution
# make_simulation_video(g, payoff, turns, init_coop, beta, choice_factor, "Prisoner's Dilemma", 5)