from LinkedList import*
import numpy as np
import random
class Rumor():
    def __init__(self,level:int,)->None:
        """_summary_

        Args:
            level (int): _description_
            history: list of users that will be filled whenever the rumor propagates, the idea is that 
        """
        self._history: 'list[User]' = []
        self._level = level
        self._sigmoid = lambda x: 1/(1+np.exp(-x))
        self._function = lambda a,b: 0.99*np.exp(-a*self._sigmoid(b))
        self._propagation_num:int = 1
    def push_rumor(self,other:'User',switch: bool = False):
        """_summary_

        Args:
            other (User): _description_
            switch (bool, optional): _description_. Defaults to False.
        """
        if not switch: self._history.append(other)
        headline = random.uniform(0.5,1)
        believe = self._function(self._propagation_num,self._level)
        if believe > headline:
            for i in other._connections:
                if i not in self._history:
                    self.push_rumor(i,switch = True)
if __name__ == "__main__":
    print("rumor time!")