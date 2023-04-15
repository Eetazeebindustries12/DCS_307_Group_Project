import numpy as np
import random

class Rumor():
    def __init__(self,level:int,teller:'User',sim:'Simulation',debug = False)->None:
        """_summary_

        Args:
            level (int): _description_
            history: list of users that will be filled whenever the rumor propagates, the idea is that 
        """
        self._tellers: 'list[User]' = [teller]
        self._level = level
        #self._sigmoid = lambda x: 1/(1+np.exp(-x))
        #self._function = lambda a,b: 0.99*np.exp(-a*self._sigmoid(b))
        self._propagation_num:int = 0
        self.push_rumor(teller,sim,debug)
    def push_rumor(self,other:'User',sim:'Simulation',debug = False):
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
                this 
                headline = random.uniform(0.5,1)
                believe = self._function(self._propagation_num,self._level)
                if believe > headline:
                """
                if random.random() >0.8:
                       self._propagation_num +=1
                       self.push_rumor(i,sim)
                       i.rumor_spread(self,debug)
                else:
                    i.rumor_list.append(None)
        if self not in sim.rumor_list: sim.addRumor(self)
    def __repr__(self):
        return f" Number of propagations: {self._propagation_num}| Start of Rumor: {self._tellers[0]._name} | End of Rumor: {self._tellers[-1]._name}"
if __name__ == "__main__":
    print("rumor time!")