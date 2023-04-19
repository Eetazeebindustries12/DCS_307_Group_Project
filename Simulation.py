import random
import numpy as np
import pandas as pd
from collections import deque
from User import User
from Rumor import Rumor
from AdjacencyMatrix import AdjacencyMatrix
import logging
import names
from time import perf_counter

def build_users(user_num:int)->'list[User]':
    user_list = [0]*user_num
    name_list = [names.get_full_name() for i in user_list]
    for i in range(user_num):
        user_list[i] = User(name_list[i],i)
        logging.debug(name_list[i])
    return user_list

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
class LinkedList:
    def __init__(self,node:'ListNode'):
        self._head = node
        self._tail = None
        grext = node.next
        while grext is not None:
            try: 
                grext = grext.next
            finally:
                self._tail = grext
                break
            #if grext.next.next is None:
               # self._tail = grext
                #break
    def __repr__(self):
        print_list = []
        g = self._head
        print_list.append(str(g.val))
        while g.next is not None:
            g = g.next
            print_list.append(str(g.val))
            
        return "->".join(print_list)
def lst2link(lst):
    cur = dummy = ListNode(0)
    for e in lst:
        cur.next = ListNode(e)
        cur = cur.next
    return dummy.next
class Simulation():
    """ideas:
    adjacency matrix 

    random misinformation 

    create random graph, ensure connectivity if a column is all zeros, drop a 1 in there. 
    
    different misinformation events can traverse different lengths of the graphs 

    
    """
    def __init__(self,user_num,debug: bool = False,int_range: 'tuple(int)'= (1,3))-> None:
        self._range = int_range
        start = perf_counter()
        self._users: 'list[User]' = build_users(user_num)
        end = perf_counter()
        logging.info(f"\nUser list build time for {user_num} users, took {end-start} seconds\n############################################################################################")
        start = perf_counter()
        self.graph = AdjacencyMatrix(self._users,int_range=int_range)
        end = perf_counter()
        logging.info(f"\nAdjacency Matrix build time for user#: {user_num}, took {end-start} seconds\n############################################################################################")
        start = perf_counter()
        self.rumor_list: 'list[Rumor]' = []
        self.user_path_rumor: 'list[LinkedList[User]]' = []
        self.rumor_path_print: 'list[LinkedList[str]]' = []
        self.rumor_path_list: 'list[LinkedList[int]]' = []
        self.rumor_dict = None
        self._rumor_tracker = self.graph._data_frame
        self._rumor_belief = None
        end = perf_counter()
        ############################################################################################
        logging.info(f"\nRest of sim initialization for {user_num} users, took {end-start} seconds\n############################################################################################ ")
        
    def addRumor(self,other:'Rumor'):
        self.rumor_list.append(other)
    def pickUsers(self,num_picks:int)->'list[User]':
        return random.choices(self._users,k = num_picks)
    def printBeliefPercent(self,rumor_num:int)->float:
        """
            outputs the percentage of the users that believed the value

        Args:
            rumor_num (int): which rumor you want the percentage of
        """
        believe_num = 0
        total_users = len(self._users)
        for i in self._users:
            if i in self.rumor_list[rumor_num]._tellers:
                believe_num += 1
        return believe_num/total_users

    def intializeRumorPaths(self):
        """_summary_ 
            builds two lists of linked lists follow the spread of some rumor:
            one of these linkedlists contains name and index while the other just contains index
            useful analytics tool to track the spread of a rumor through the graph
        """
        for i in self.rumor_list:
            self.user_path_rumor.append(k for k in i._tellers)
            self.rumor_path_print.append(LinkedList(lst2link([f"[Name: {j._name}| User#: {j.index}]" for j in i._tellers])))
            self.rumor_path_list.append(LinkedList(lst2link([j.index for j in i._tellers])))
        self.rumor_dict = {k:v for (k,v) in zip(self.rumor_list,self.rumor_path_list)}
    def printRumorPaths(self,debug = True):
        self.intializeRumorPaths()
        if debug:
            print_str = "Rumor Paths\n"
            print_list = [i.__repr__() for i in self.rumor_path_print]
            print_str += "\n".join(print_list)
            print(print_str)
        else:
            print_str = "Rumor Paths\n"
            print_list = [i.__repr__() for i in self.rumor_path_list]
            print_str += "\n".join(print_list)
            print(print_str)
    def rumorsToString(self)->str:
        print_list = [str(i) for i in self.rumor_list]            
        return "\n".join(print_list)
    def __repr__(self,debug: bool = False):
        return str(self.graph)
if __name__ == "__main__":
    logging.basicConfig(filename='simulation_perf.log', filemode='a',\
                        format='%(name)s - %(levelname)s - %(message)s', level= logging.INFO)
    logging.warning('This will get logged to a file')
    seed = 12312312
    random.seed(seed)
    #user_num is the number of users the simulation initializes, this will affect the program at roughly O(n^3)..
    #mostly because intializing the adjacency matrix runs in O(n^3)
    user_num = 2000
    #int_range is the a range for number of connections an user can have
    #current main limiter of range is that when it is too high for a high user_num
    #the rumor propagation function will generally hit recursion depth
    #this is themost critical thing that needs to be addressed,
    #while user_num slows the program down, int_range can crash it
    int_range = (9,10)
    #rumor_num just the number of rumors that we want to initalize this wil gener
    rumor_num = 20
    logging.info(
        f"\
\n############################################################################################\
\n############################################################################################\
\nLogging for seed: {seed} | {user_num} users | range {int_range} | {rumor_num} rumors\n############################################################################################")
    start = perf_counter()
    sim = Simulation(user_num,int_range = int_range)
    end = perf_counter()
    logging.info(f"\nTime to initalize Simulation for {user_num} users with a connection range of {int_range}: {end-start} seconds\n############################################################################################")
    #print(sim)
    #print(sim.graph._graph)
    #user_1 = sim._users[1]
    #print(sim) 

    start = perf_counter()
    for i in sim.pickUsers(rumor_num):
        g = Rumor(1,i,sim)
    end =perf_counter()
    logging.info(f"\nTime it took top initialize {rumor_num} rumors: {end- start} seconds\n############################################################################################")
    #sim.printRumorPaths()
    #sim.printRumorPaths(False)

    start = perf_counter()
    sim.intializeRumorPaths()
    end = perf_counter()
    logging.info(f"\nTime it took to intialize rumor paths for {rumor_num} rumors: {end- start} seconds\n############################################################################################")
    print(sim.user_path_rumor[4])
    print(f"Percentage believers: {round(sim.printBeliefPercent(4),2)}")
    g = []
    for i in sim.rumor_list[4]._tellers:
        if i not in g:
            g.append(i)
    print(len(sim.rumor_list[4]._tellers))
    print(len(g))