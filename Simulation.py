import random
import numpy as np
import pandas as pd
from collections import deque
from User import User
from AdjacencyMatrix import AdjacencyMatrix
import names
def gen_name():
    stre = chr(random.randint(65,90))
    for i in range(random.randint(1,4)):
        stre += chr(random.randint(97,122))
    return stre
def build_users(user_num:int)->'list[User]':
    user_list = [0]*user_num
    for i in range(user_num):
        user_list[i] = User(gen_name,i)
    return user_list   
class Simulation():
    """ideas:
    adjacency matrix 

    random misinformation 

    create random graph, ensure connectivity if a column is all zeros, drop a 1 in there. 
    
    different misinformation events can traverse different lengths of the graphs 

    
    """
    def __init__(self,user_num,debug: bool = False):
        self._users:'list[User]' = build_users(user_num)
        self.graph = AdjacencyMatrix(self._users)
    def __repr__(self,debug: bool = False):
        return str(self.graph)
if __name__ == "__main__":
    sim = Simulation(20)
    print(sim.graph)
