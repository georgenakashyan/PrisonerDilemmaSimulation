import networkx as nx
import os as os
import matplotlib.pyplot as plt
import scipy as sp
from evolutionary_game_theory import *
from time_series_plots import *
from density_plots import *

# input variables
os.system('clear')
print("[=================== Prisoner's Dilemma Game =======================]")
while True:
    graphChoice = input("\nWhich graph would you like to simulate? (ws for Watts-Strogatz or fb for Facebook): ")
    if (graphChoice == "ws"):
        print("\nNote: Default values for these questions are: 5000 Nodes, 4 Edges Per Node (on average), 10 games, 25 turns, 0.5 Cooperators.")
        nodes = int(input("\nNumber of players/nodes (positive integer): "))
        avgEdgePerNode = int(input("\nNumber of average edges per node (positive integer): "))
        g = nx.watts_strogatz_graph(nodes, avgEdgePerNode, 0)
        break
    elif (graphChoice == "fb"):
        print("\nNote: Default values for these questions are: 10 Games, 25 Turns, 0.5 Cooperators.")
        path = os.path.split(os.path.realpath(__file__))
        g = nx.read_edgelist(os.path.normpath(path[0] + "/facebook_combined.txt.gz"), create_using = nx.Graph(), nodetype = int)
        break
    else:
        print("\nInvalid choice, type fb for Facebook network or ws for Watts-Strogatz network.")

games = int(input("\nNumber of games to simulate (positive integer): "))
turns = int(input("\nNumber of turns to run each game (positve integer): "))
init_coop = float(input("\nInitial proportion of cooperators to defectors (float between 0 and 1 inclusive): "))

# how players decide to change their strategy
while True:
    choice_factor = int(input("""\nWhat will players base their decision to change their strategy on? (Enter the choice number)
                            \n(1) Payoff difference
                            \n(2) Popularity difference
                            \n"""))
    if (choice_factor == 1):
        beta = float(input("\nImportance of payoff difference (value between 0 and 1 inclusive): "))
        break
    if (choice_factor == 2):
        break

# payoff matrix
# !: Payoff matrix based off of benefits and costs for the prisoner's dilemma game
# !: D is defector, C is cooperator. Left is 'i'or the current node, right is 'j' or neighbor node.
# !: [D:D, D:C], [C:D, C:C]
payoff = [[0, 1.8], [-0.3, 1.5]]

# running the simulation and making time series plot
pDict = plot_time_series(g, payoff, turns, init_coop, beta, games, choice_factor, "Proportion of Cooperators per Time-Step")
p = sum(pDict.values()) / len(pDict)

# output of result data
print("\n[============================= Results =============================]")
print("\nMean proportion of cooperators after", turns, "turns for", games, "games: ", p)

# video of evolution
make_simulation_video(g, payoff, turns, init_coop, beta, choice_factor, "Prisoner's Dilemma", 5)