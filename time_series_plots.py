import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import moviepy.video.io.ImageSequenceClip
from evolutionary_game_theory import one_replica_simulation

path = os.path.split(os.path.realpath(__file__))

def _plot_time_serie(G, W, steps, x0, beta, ax, color, choice_factor, title):
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
	choice_factor : int
		Choice of how nodes will decide to update their strategy
	Returns
	-------
	p : float
		Mean density
	"""
	p, time_series = one_replica_simulation(G, W, steps, x0, beta, choice_factor, title)
	ax.plot(time_series, c=color)
	#!: PUT VALUES IN SOMETHING TO GIVE TO MEANLINE OUTSIDE THIS
	return p


def plot_time_series(G, W, steps, x0, beta, games, choice_factor, title, saving_path=True):
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
	choice_factor : int
		Choice of how nodes will decide to update their strategy
	title : str
		Title of the plot
	saving_path : bool, default True
		If True, the image will be saved
	-------
	means_dict : dict
		Mean proportion of cooperators at every stage
	"""
	means_dict = dict()
	plt.figure(figsize=(20, 10))
	ax = plt.gca()
	# !: Currently skipping last game.
	# *: for T, c in tuple(zip(np.linspace(1, 10, games), mcolors.CSS4_COLORS.keys())):
	for T, c in tuple(zip(range(1, games+1), mcolors.XKCD_COLORS.keys())):
		gameTitle = title + ", Game=" + str(T)
		p = _plot_time_serie(G, W, steps=steps, x0=x0, beta=beta, ax=ax, color=c, choice_factor=choice_factor, title=gameTitle)
		# TODO: Fixing the mean_dict. It doesnt seam to work properly?
		means_dict[T] = p
		print("game " + str(T))
	# TODO: Fixing the mean_line. It prints but not in the right spots
	mean_line = plt.plot(list(means_dict.keys()), list(means_dict.values()), c='blue')	 
	plt.setp(mean_line, linestyle="--")
	plt.setp(mean_line, linewidth=4)
	# labels
	plt.title("Proportion of Cooperators per Time-Step {0} (Avg At Game End: {1})".format(title, str(sum(means_dict.values()) / len(means_dict))))
	plt.xlabel("Time Steps")
	plt.ylabel("Proportion of Cooperator Nodes")
	# saving file to reports folder
	if saving_path:
		plt.savefig(os.path.normpath(path[0] + "/reports/figures/time_series/" + title + " " + ".jpeg"), dpi=500)

	# ?: Created a Mean line of all games but in a seperate graph. 
	# ?: Not sure if it should be a part of the first one or seperate.
	# plt.figure(figsize=(5, 5))
	# plt.plot(list(means_dict.keys()), list(means_dict.values()), c='blue')
	# plt.scatter(list(means_dict.keys()), list(means_dict.values()), c='blue')
	# plt.title(title)
	# plt.xlabel('Time Steps')
	# plt.ylabel('Mean proportion of Cooperative Nodes')
	# if saving_path:
	#	 plt.savefig(os.path.normpath(path[0] + "/reports/figures/time_series/" + title + " - Mean" + ".jpeg"), dpi=500)
	# ?: end
	return means_dict

def make_simulation_video(name, fps):
	"""
	Makes a video with the simulation evolution of the nodes strategies
	Parameters
	----------
	name : str
		Name of the video
	fps : int
	"""
	# make video
	image_folder = os.path.normpath(path[0] + "/reports/figures/film")
	image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
	clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(sorted(image_files), fps=fps)
	clip.write_videofile(os.path.normpath(path[0] + "/reports/videos/" + name + ".mp4"))