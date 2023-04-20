import numpy as np
import pandas as pd
import random
from collections import deque
import logging
from time import perf_counter
class AdjacencyMatrix():
    def __init__(self,user_list:'list[User]',int_range: 'tuple(int)' = (1,3))-> None:
        """_summary_
            should initalize the adjacency graph for the simulation
            also initalizes a data frame to use for connections
            as long as the model is sufficiently large, once we intialize in such a way that every single person has at least one connection
            we should then be able to avoid using adjacency checks which do rely on the array style of self._graph
            we can then move to purely indexing from the data_frame using names of users to check connection
            :)
        Args:
            user_list (list[User]): _description_
            int_range tuple(int): range of the number of users connections
        """
        dimension = len(user_list)
        dimension_list = [[i for i in range(dimension)] for j in range(dimension)]
        #self._user_indeces = [i._name for i in user_list]
        self._size = dimension
        #self._index_dict = {k:v for (k,v) in zip(user_list,[i for i in range(dimension)])}
        self._graph = np.zeros((dimension,dimension))
        start = perf_counter()
        while not self.adjacency_check():
            adjacency_iters = 0
            for i in range(self._size):
                #checks whether the matrix is fully connected
                if not self.row_adjacency_check(i):
                   adjacency_iters +=1
                   val = self.add_connections(i,int_range=int_range)
                   if val: break
            print(f"Number of iterations in the adjacency loop: {adjacency_iters}")
        end = perf_counter()
        logging.info(f"\nAdjacency while loop for {dimension} users: in {end-start} seconds\n############################################################################################")
        user_name_list = [i._name for i in user_list]
        start = perf_counter()
        self._data_frame = pd.DataFrame(self._graph, columns = user_name_list,index = user_name_list)
        end = perf_counter()
        logging.info(f"\nIntializing dataframe for {dimension} users: took {end-start} seconds \n############################################################################################")
        start = perf_counter()
        # this is currently at roughly O(N^3) not sure if this can be fixed however as it is fully initializing the adjacaency matrix
        # it can potentially be improved by only adding above or below the diagonal
        for i in range(dimension):
            for j in range(dimension):
                if self._graph[i][j]:
                    #this is not the self.addConnection this is the user class add connection
                    user_list[i].add_connection(user_list[j])
        end = perf_counter()
        logging.info(f"\nIntializing connections for {dimension} users: took {end-start} seconds\n############################################################################################")
    def adjacency_check(self)-> bool:
        """_summary_
                checks if the graph is entirely complete
        Returns:
            bool: true if the adjacency matrix is complete, else returns false
        """
        #this flattens the array by column, essentially, what we want here is to make sure there are no zeros in this list
        check_list = np.sum(self._graph,axis = 1)
        for i in check_list:
            truth_val = bool(i)
            if not truth_val:
                return False
        return True
    def generate_connections(self,row_num:int,debug: bool = False, int_range: 'tuple(int)' = (1,3))->'list(tuple(int))':
        new_list = []
        used_nums = [row_num]
        if int_range[0] > int_range[1]:
            raise ValueError("int_range input 0 must be smaller than int_range intput 1")
        #start = perf_counter()
        for t in range(random.randint(int_range[0],int_range[1])):
            if debug:
                if self.adjacency_check():
                    return True
            gen_num = random.choice([i for i in range(0,self._size) if i not in used_nums])
            new_list.append((row_num,gen_num))
            new_list.append((gen_num,row_num))
            used_nums.append(gen_num)
        #end = perf_counter()
        #print(f"for row number {row_num} took: {end-start} seconds")
        return new_list
    def row_adjacency_check(self,row_num:int)->bool:
        row_sum = np.sum(self._graph,1)[row_num]
        return bool(row_sum)
    def add_connections(self,shmoney:int,int_range: 'tuple(int)' = (1,3)):
        """_summary_
        """
        val_list = self.generate_connections(shmoney, int_range= int_range)
            
        #start = perf_counter()
        for i in val_list:
            if isinstance(i,list):
                for j in i:
                    self._graph[j[0]][j[1]] = 1
            else:
                self._graph[i[0]][i[1]] = 1
        #end = perf_counter()
    def __repr__(self):
        return str(self._data_frame)
if __name__ == "__main__":
    print("gorn")