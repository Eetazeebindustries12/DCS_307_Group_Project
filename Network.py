import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Simulation import*
from Rumor import Rumor
from collections import deque
from User import User
from AdjacencyMatrix import AdjacencyMatrix
import names

def tree_to_graph(tree):
    graph = nx.DiGraph()
    for node in tree.all_nodes_itr():
        graph.add_node(node.identifier, data=node)
        if node.is_root():
            continue
        graph.add_edge(node.predecessor, node.identifier)
    return graph

if __name__ == "__main__":
    random.seed(142121)
    rumor_num = 1
    sim = Simulation(1000,int_range = (1,3))
    rumor_list = []
    for i in sim.pickUsers(rumor_num):
        g = Rumor(1,i,sim)
        rumor_list.append(g)
    rumor_tree = rumor_list[0]._tree
    print(rumor_list[0])
    graph = tree_to_graph(rumor_tree)
    print(graph)
    nx.draw(graph)
