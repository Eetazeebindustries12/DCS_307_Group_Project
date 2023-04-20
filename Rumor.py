import numpy as np
import random
from treelib import Tree,Node

class Rumor():
    def __init__(self,level:int,teller:'User',sim:'Simulation',debug = False)->None:
        """_summary_

        Args:
            level (int): _description_
            history: list of users that will be filled whenever the rumor propagates, the idea is that 
        """
        self._tree = Tree()
        self._tree.create_node(teller._name,teller.index)
        self._tellers: 'list[User]' = [teller]
        self._non_believer: 'list[User]' = []
        self._level = level #currently does nothing lol 
        #self._sigmoid = lambda x: 1/(1+np.exp(-x))
        #self._function = lambda a,b: 0.99*np.exp(-a*self._sigmoid(b))
        self._propagation_num:int = 0
        self.push_rumor(teller,sim,debug)
        #self._track = [] #
    '''
    def push_rumor(self,other:'User',sim:'Simulation',debug = False)-> None:
        #recursive version of push_rumor, hits rumor
        """_summary_
            serious issues associated with this function when number of connections
            gets too high, it will generally hit recursion depth
            I think adding in something to 
        Args:
            other (User): _description_
            switch (bool, optional): _description_. Defaults to False.
        """
        if other != self._tellers[0]:
            self._tellers.append(other)
        other.rumor_list.append(other)
        for i in other.connections:
            if i not in self._tellers:
                """_summary_
                headline = random.uniform(0.5,1)
                believe = self._function(self._propagation_num,self._level)
                if believe > headline:
                """
                if random.random() >0.5:
                       self._propagation_num +=1
                       self.push_rumor(i,sim)
                       i.rumor_spread(self,debug)
                else:
                    i.rumor_list.append(None)
        if self not in sim.rumor_list: sim.addRumor(self)
    '''

    def push_rumor(self, other: 'User', sim: 'Simulation', debug=False) -> None:
        """
        Propagate the rumor to other users iteratively.
        
        issue currently with users appearing multiple times in the rumor list with iterative approach

        Args:
            other (User): The user to propagate the rumor to.
            sim (Simulation): The simulation object.
            debug (bool, optional): Whether to print debug information. Defaults to False.
        """
        #integer list for users
        heard_num_level = 3
        user_heard_num_list = [0 for i in range(sim._size)]
        queue = [other]
        tracking_list = [other]
        iter_number = 0
        last_user = other
        while queue:
            #iter_number+= 1
            if iter_number > sim._size:
                #this is a debug clause for when the iteration breaks 
                print(f"iteration number: {iter_number}, max sim depth {sim._size}")
                print(f"returned out of function because of iteration issues, issue still present")
                sim.addRumor(self)
                return None
            current_user = queue.pop(0)
            if current_user not in tracking_list:
                self._tellers.append(current_user)
                self._tree.create_node(current_user._name,current_user.index,parent = last_user.index)
                tracking_list.append(current_user)
                #guard clause to try to prevent repeats, very much does not work.
                #if self in current_user.rumor_list:
                #    continue
            current_user.rumor_list.append(current_user)
            for i in current_user.connections:
                #self._tellers is the list of people who have told the rumor so far

                if i not in (self._tellers or self._non_believer): #
                    if random.random() > 0.5:
                        self._propagation_num += 1
                        queue.append(i)
                        i.rumor_spread(self, debug)
                    elif user_heard_num_list[i.index] < heard_num_level:
                        user_heard_num_list[i.index] +=1
                    else:
                        if i not in self._tellers:
                            self._non_believer.append(i)
                        #print(self._non_believer)
                        i.rumor_list.append(None)
                #self._track.append(current_user.connections[i] for i in len(current_user.connections))
                last_user = current_user
            if self not in sim.rumor_list:
                #adds the rumor to the simulations rumor list
                sim.addRumor(self)
    def __repr__(self):
        self._tree.show()
        return f" Number of propagations: {self._propagation_num}| Start of Rumor: {self._tellers[0]._name} | End of Rumor: {self._tellers[-1]._name}"
if __name__ == "__main__":
    print("rumor time!")