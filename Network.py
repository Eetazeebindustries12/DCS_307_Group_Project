import networkx as nx
from networkx import drawing
import matplotlib
from matplotlib import figure
from Simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(200)
    new_graph = nx.Graph(sim.graph._graph)
    new_graph = nx.adjacency_matrix(new_graph)
    print(new_graph)
    nx.draw(new_graph)