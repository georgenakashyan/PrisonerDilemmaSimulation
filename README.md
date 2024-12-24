# Popularity-Based Approach to Promote Cooperation in The Prisoner's Dilemma Game

## Introduction

This program was created to simulate the Prisoner's Dilemma Game running on different types of social networks, including Watts-Strogratz and Real-World networks. It uses different strategies including a "popularity-based" method that is further explained in the article that was posted with our findings from the program.

Read the [full paper here](https://dl.acm.org/doi/10.1145/3625007.3627723).

Examining the interaction between agents in a well-mixed population has been a prevalent area of research. Previous studies have emphasized the evolution of the impact of network architecture and payoff differences on agents' behavior in various games. There has been a recent surge in interest in incorporating popularity among researchers in this field. In this study, we employ a game theoretic approach to gain insight into the strategic behavior and decision-making processes of individuals in a network and how these decisions impact the diffusion of information when an individual's popularity is considered. The Fermi function is used to model the probability of information diffusion and the spread of influence within the network. We introduce a novel simulation module that models the dynamic process of evolutionary game theory in both synthetic and real-world networks, leveraging the Fermi update rule as a critical component. The simulation results provide valuable insight into the evolution of cooperative behavior in complex networks and hold potential for further exploration into various aspects of evolutionary game theory.

## Usage

### Setup
Download Python 2 or Python 3 at [Pythons official site](https://www.python.org/downloads/).

### Running
Run the main.py file from the command line.
```bash
python main.py
```

Enter your parameters to specify what graph type, strategy type, games, turns, and payoff matrix to use.

### Analyzing
All graphs and charts are created in the project's base directory.
You can view our examples in the "Finished Examples" folder.

## Issues

There is a list of
[Known Issues](https://github.com/georgenakashyan/PrisonerDilemmaSimulation/issues) (things
to be fixed or that aren't yet implemented).

If you found a bug or have a new idea/feature for the program,
[you can report them](https://github.com/georgenakashyan/PrisonerDilemmaSimulation/issues/new).

## Contact
If you have any questions, please contact George Nakashyan at [nakagk@farmingdale.edu](mailto:nakagk@farmingdale.edu).

## Citation
If you find this code useful, please consider citing our paper:
```bibtex
@inproceedings{10.1145/3625007.3627723,
author = {Dean, Nur and Nakashyan, George K.},
title = {Popularity-Based Approach to Promote Cooperation in The Prisoner's Dilemma Game},
year = {2024},
isbn = {9798400704093},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3625007.3627723},
doi = {10.1145/3625007.3627723},
abstract = {Examining the interaction between agents in a well-mixed population has been a prevalent area of research. Previous studies have emphasized the evolution of the impact of network architecture and payoff differences on agents' behavior in various games. There has been a recent surge in interest in incorporating popularity among researchers in this field. In this study, we employ a game theoretic approach to gain insight into the strategic behavior and decision-making processes of individuals in a network and how these decisions impact the diffusion of information when an individual's popularity is considered. The Fermi function is used to model the probability of information diffusion and the spread of influence within the network. We introduce a novel simulation module that models the dynamic process of evolutionary game theory in both synthetic and real-world networks, leveraging the Fermi update rule as a critical component. The simulation results provide valuable insight into the evolution of cooperative behavior in complex networks and hold potential for further exploration into various aspects of evolutionary game theory.},
booktitle = {Proceedings of the 2023 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining},
pages = {1–8},
numpages = {8},
keywords = {prisoner's dilemma, game theory, evolutionary game on networks, fermi function, facebook, watts-strogatz, social networks},
location = {Kusadasi, Turkiye},
series = {ASONAM '23}
}
```
