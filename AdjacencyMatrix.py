import numpy as np
import pandas as pd
import random
from collections import deque
import logging
class AdjacencyMatrix():
    def __init__(self,user_list:'list[User]')-> None:
        """_summary_
            should initalize the adjacency graph for the simulation
            also initalizes a data frame to use for connections
            as long as the model is sufficiently large, once we intialize in such a way that every single person has at least one connection
            we should then be able to avoid using adjacency checks which do rely on the array style of self._graph
            we can then move to purely indexing from the data_frame using names of users to check connection
            :)
        Args:
            user_list (list[User]): _description_
        """
        dimension = len(user_list)
        dimension_list = [[i for i in range(dimension)] for j in range(dimension)]
        self._user_indeces = [i._name for i in user_list]
        self._size = dimension
        #self._index_dict = {k:v for (k,v) in zip(user_list,[i for i in range(dimension)])}
        self._graph = np.zeros((dimension,dimension))
        while not self.adjacency_check():
           for i in range(self._size):
               if not self.row_adjacency_check(i):
                   val = self.add_connections(i,debug = True)
                   if val: break
        user_name_list = [i._name for i in user_list]
        self._data_frame = pd.DataFrame(self._graph, columns = user_name_list,index = user_name_list)
    def adjacency_check(self)-> bool:
        """_summary_
                checks if the graph is entirely complete
        Returns:
            bool: true if the adjacency matrix is complete, else returns false
        """
        #this flattens the array by column, essentially, what we want here is to make sure there are no zeros in this list
        check_list = np.sum(self._graph,axis = 1)
        logging.debug(f"flattened array{check_list}")
        for i in check_list:
            truth_val = bool(i)
            if not truth_val:
                return False
        return True
    def generate_connections(self,row_num:int,debug: bool = False)->'list(tuple(int))':
        new_list = []
        used_nums = [row_num]
        for t in range(random.randint(1,3)):
            if debug:
                if self.adjacency_check():
                    return True
            gen_num = random.choice([i for i in range(0,self._size) if i not in used_nums])
            new_list.append((row_num,gen_num))
            new_list.append((gen_num,row_num))
            used_nums.append(gen_num)
        return new_list
    def row_adjacency_check(self,row_num:int)->bool:
        row_sum = np.sum(self._graph,1)[row_num]
        return bool(row_sum)
    def add_connections(self,shmoney:int,debug = False):
        """_summary_
        """
        val_list = self.generate_connections(shmoney,debug = debug)
        logging.debug(f"list from generate connections:{val_list}, from row {shmoney}")
        for i in val_list:
            logging.debug(f"i in loop {i}")
            if isinstance(i,list):
                for j in i:
                    logging.debug(f"j in loop {j}")
                    logging.debug(f"{self._graph[j]}")
                    self._graph[j[0]][j[1]] = 1
            else:
                self._graph[i[0]][i[1]] = 1
    def __repr__(self):
        return str(self._data_frame)