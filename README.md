# Prisoner's Dilemma Network Simulation

A comprehensive Python simulation of the Prisoner's Dilemma game on various network topologies using evolutionary game theory principles. This project implements agent-based modeling to study cooperation and defection dynamics in social networks.

## 🎯 Overview

This simulation explores how cooperation emerges and evolves in populations connected through different network structures. Players make strategic decisions (cooperate or defect) based on their neighbors' actions and payoffs, following evolutionary game theory principles with Fermi updating rules.

## 🏗️ Architecture

### Core Components

- **`main.py`** - Interactive CLI interface for simulation configuration
- **`evolutionary_game_theory.py`** - Core simulation engine implementing game mechanics
- **`time_series_plots.py`** - Time series visualization and analysis
- **`density_plots.py`** - Cooperation density heat map generation
- **`degree_dist.py`** - Network degree distribution analysis

### Network Types Supported

1. **Watts-Strogatz (ws)** - Small-world networks with configurable clustering
2. **Facebook (fb)** - Real social network from Facebook combined dataset
3. **Big Facebook (bfb)** - Extended Facebook network dataset
4. **GitHub (gh)** - Developer collaboration network from GitHub
5. **2D Grid (2d)** - Regular lattice topology

## 🚀 Getting Started

### Prerequisites

```bash
pip install networkx numpy matplotlib moviepy
```

### Required Data Files

- `facebook_combined.txt.gz` - Facebook social network
- `BFacebook.csv` - Extended Facebook dataset  
- `musae_git_edges.csv` - GitHub collaboration network

### Running a Simulation

```bash
python main.py
```

Follow the interactive prompts to configure:
1. Network type (ws/fb/bfb/gh/2d)
2. Network parameters (nodes, edges for synthetic networks)
3. Game parameters (games, turns, initial cooperators)
4. Strategy updating mechanism
5. Payoff matrix selection

## 🎲 Game Mechanics

### Prisoner's Dilemma Payoff Matrix

Players receive payoffs based on mutual interactions:
- **Mutual Cooperation (CC)**: Both benefit
- **Mutual Defection (DD)**: No benefit  
- **Exploitation (CD/DC)**: Defector benefits, cooperator pays cost

Example payoff matrices:
- **Watts-Strogatz**: `[[1.5, -0.3], [1.8, 0]]`
- **Facebook**: `[[14.5, -0.5], [15, 0]]`
- **GitHub**: `[[2.7, -0.3], [3, 0]]`

### Strategy Updating Rules

**Strategy 1: Payoff-Based (Fermi Rule)**
```python
P(i→j) = 1 / (1 + e^(-β(w_j - w_i)))
```
- `β`: Selection intensity (0-1)
- `w_i, w_j`: Payoffs of players i and j

**Strategy 2: Popularity-Based**
- Players adopt strategies from most connected successful neighbors
- `β = degree(j) / (total_nodes - 1)`

## 📊 Output and Analysis

### Generated Files

**Time Series Plots**
- Location: `reports/figures/time_series/`
- Shows cooperation proportion over time
- Format: `[Network], [Games] Games, [Turns] Turns, Strategy [X], [payoff] payoff.jpeg`

**Network Snapshots**
- Location: `reports/figures/film/`
- Visual evolution of strategies on network
- Red nodes: Cooperators, Blue nodes: Defectors

**Influence Analysis**
- CSV files tracking node influence on strategy adoption
- Columns: Node Number, Strategy, Degree, Number of Influences

**Videos** (Optional)
- Location: `reports/videos/`
- Animated evolution of cooperation patterns

### Results Interpretation

**Cooperation Metrics**
- Overall average cooperation rate
- Final equilibrium cooperation level
- Temporal dynamics and stability

**Network Effects**
- High-degree nodes often become influential
- Clustering promotes local cooperation
- Network topology affects equilibrium outcomes

## 🔬 Research Applications

### Studied Phenomena

- **Cooperation Evolution**: How mutual aid emerges in selfish populations
- **Network Effects**: Impact of social structure on collective outcomes  
- **Strategy Dynamics**: Temporal patterns of behavioral change
- **Equilibrium Analysis**: Long-term stable states
- **Influence Networks**: How connectivity affects leadership

### Academic Context

Based on established research in:
- Evolutionary game theory (Nowak, 2006)
- Network reciprocity (Santos & Pacheco, 2005)
- Social influence dynamics (Szabó & Fáth, 2007)

## 📈 Sample Results

Typical findings across network types:

**Small-World Networks (Watts-Strogatz)**
- Cooperation levels: 40-70%
- High clustering supports cooperation
- Random rewiring can destabilize cooperation

**Real Social Networks (Facebook/GitHub)**  
- Cooperation levels: 60-85%
- Scale-free properties promote cooperation
- Hub nodes become influential cooperators

**Regular Lattices (2D Grid)**
- Cooperation levels: 30-50%  
- Spatial clustering of strategies
- Slower convergence to equilibrium

## 🛠️ Configuration Options

### Network Parameters
- **Watts-Strogatz**: nodes, k (avg degree), β (rewiring probability = 0.1)
- **Real Networks**: Fixed topology from data files
- **2D Grid**: n×n lattice structure

### Simulation Parameters
- **Games**: Number of independent runs (1-100)
- **Turns**: Evolution steps per game (10-1000)
- **Initial cooperators**: Proportion (0.0-1.0)
- **Selection intensity**: Strategy updating strength (0.0-1.0)

### Payoff Matrices
Multiple predefined matrices optimized for different network types:
- Standard symmetric games
- Asymmetric exploitation scenarios  
- Network-specific calibrated values

## 🔍 Advanced Features

### Density Analysis
Generate cooperation heat maps across parameter space:
- T ∈ [0,2] (Temptation to defect)
- S ∈ [-1,1] (Sucker's payoff)  
- Reveals phase transitions and critical points

### Influence Tracking
Monitor which nodes drive strategy adoption:
- Node-level influence counts
- Degree-influence correlations
- Leadership emergence patterns

### Video Generation
Create animated visualizations:
- Frame-by-frame strategy evolution
- Customizable frame rates and quality
- Suitable for presentations and analysis

## 📚 References

1. Nowak, M. A. (2006). *Evolutionary Dynamics*. Harvard University Press.
2. Santos, F. C., & Pacheco, J. M. (2005). Scale-free networks provide a unifying framework for the emergence of cooperation. *Physical Review Letters*, 95(9), 098104.
3. Szabó, G., & Fáth, G. (2007). Evolutionary games on graphs. *Physics Reports*, 446(4-6), 97-216.
4. Watts, D. J., & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks. *Nature*, 393(6684), 440-442.

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional network topologies
- New strategy updating rules  
- Performance optimizations
- Extended analysis tools
- Interactive visualizations

## 📧 Contact

For questions about implementation or research applications, please open an issue on the repository.

---

*This simulation provides a powerful platform for exploring the emergence of cooperation in complex social systems, offering insights into fundamental questions about human social behavior and collective action.*
