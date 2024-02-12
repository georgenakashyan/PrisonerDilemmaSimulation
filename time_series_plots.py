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
	return time_series


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
	means_arr = [0] * steps
	plt.figure(figsize=(20, 10))
	ax = plt.gca()
	for T, c in tuple(zip(range(1, games+1), mcolors.XKCD_COLORS.keys())):
		print("Game " + str(T))
		videoTitle = title + ", Game=" + str(T)
		time_series = _plot_time_serie(G, W, steps=steps, x0=x0, beta=beta, ax=ax, color=c, choice_factor=choice_factor, title=videoTitle)
		for i in range(0, steps):
			means_arr[i] = means_arr[i] + time_series[i]
	for i in range(0, steps):
		means_arr[i] = means_arr[i]/games
	mean_line = plt.plot(range(0, steps), means_arr, c='red')	 
	plt.setp(mean_line, linestyle="--")
	plt.setp(mean_line, linewidth=3)
	# labels
	# BUG: THIS OUTPUTS A RUNNING TOTAL OF THE VALUES IN means_arr, NOT THE MEAN OF THE LAST STEP.
	plt.title("Proportion of Cooperators per Time-Step {0} (Avg At Game End: {1})".format(title, str(np.mean(means_arr))), fontsize=20)
	plt.xlabel("Time Steps", fontsize=20)
	plt.ylabel("Proportion of Cooperator Nodes", fontsize=20)
	# saving file to reports folder
	if saving_path:
		plt.savefig(os.path.normpath(path[0] + "/reports/figures/time_series/" + title + " " + ".jpeg"), dpi=500)
	return means_arr

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