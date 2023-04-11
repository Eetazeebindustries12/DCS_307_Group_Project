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
    '''
    @classmethod
    def percent_infected(self)->float:
        """_summary_

        Returns:
            float: _description_
        """
        percent = 0
        for i in self.users:
            if i._infected:
                percent += 1
        self.infected_percent = float(percent/(len(self.users)))
        return percent/(len(self.users))
    @classmethod
    def percent_susceptible(self)->float:
        """_summary_

        Returns:
            float: _description_
        """
        percent = 0
        for i in self.users:
            if i._susceptible:
                percent += 1
        self.susceptible_percent = float(percent/(len(self.users)))
        return percent/(len(self.users))
    def check_connection(self,user1:'User',user2:'User')->bool:
        return bool(self.graph._data_frame[user1._name][user2._name])
    '''
if __name__ == "__main__":
    sim = Simulation(20)
    print(sim.graph)