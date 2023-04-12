from LinkedList import*
import numpy as np
import random
class Rumor():
    def __init__(self,level:int,)->None:
        self._history: 'list[User]' = []
        self._level = level
        self._sigmoid = lambda x: 1/(1+np.exp(-x))
        self._function = lambda a,b: 0.99*np.exp(a*self._sigmoid(b))
        self._propagation_num:int = 1
    def push_rumor(self,other:'User'):
        headline = random.uniform(0.5,1)
        