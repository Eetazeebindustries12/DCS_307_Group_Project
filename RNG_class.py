from numpy.random import MT19937, Generator
import numpy.typing
import numpy as np
import random
import matplotlib.pyplot as plt
import collections
import pandas as pd
class Stream(int):
    def __new__(cls,other:int)->None:
        """
        I wanted to make it so that the stream class inherited integer properties and also could only select integers within 
        the stream length, I went with 25 and made it so that you couldnt initalize a stream that would give an index error
        """
        if other > 25:
            return super(Stream,cls).__new__(cls,random.randint(1,25))
        else:
            return super(Stream,cls).__new__(cls,other)

class RNG:
    #class level variables
    _seed: 'numpy.int64' = None
    _streams: 'list[numpy.random.Generator]' = []
    _initialized: bool = False
    
    @classmethod
    def seedSet(cls,seed: 'numpy.int64')->None:
        """
        Description:
            uses the numpy.generator.exponential() method to return a float from the generator stream 
        Args:
            mu: a float object that will not be negative and if a negative is input it will be turned positive with abs()
            which_stream: a Stream object that selects the Stream to be used, mimics int except it can't exceed stream index 
        Returns:
            returns a numpy float
        """
        cls._seed = seed
        cls.intializeStreams()
    @classmethod
    def intializeStreams(cls)->None:
        """
        Description:
            uses the numpy.generator.exponential() method to return a float from the generator stream 
        Args:
            mu: a float object that will not be negative and if a negative is input it will be turned positive with abs()
            which_stream: a Stream object that selects the Stream to be used, mimics int except it can't exceed stream index 
        Returns:
            returns a numpy float
        """
        rng = MT19937(cls._seed)
        for i in range(25):
            cls._streams.append(Generator(rng.jumped(i)))
        cls._initialized = True
    @classmethod
    def geometrics(cls,p:float,which_stream:int)->'numpy.int64':
        """
        Description:
            uses the numpy.generator.exponential() method to return a float from the generator stream 
        Args:
            mu: a float object that will not be negative and if a negative is input it will be turned positive with abs()
            which_stream: a Stream object that selects the Stream to be used, mimics int except it can't exceed stream index 
        Returns:
            returns a numpy float
        """
        if not cls._initialized:
            cls.intializeStreams()
        generator = cls._streams[which_stream]
        return generator.geometric(p)
    @classmethod
    def random(cls,which_stream: 'Stream') -> 'numpy.float64':
        """
        Description:
            uses the numpy.generator.exponential() method to return a float from the generator stream 
        Args:
            mu: a float object that will not be negative and if a negative is input it will be turned positive with abs()
            which_stream: a Stream object that selects the Stream to be used, mimics int except it can't exceed stream index 
        Returns:
            returns a numpy float
        """
        if not cls._initialized:
            cls.intializeStreams()
        return np.float64(cls._streams[which_stream].random())
        pass
    @classmethod
    def randint(cls,a:int,b:int,which_stream:'Stream')->'numpy.int64':
        """
        Description:
            uses the numpy.generator.exponential() method to return a float from the generator stream 
        Args:
            mu: a float object that will not be negative and if a negative is input it will be turned positive with abs()
            which_stream: a Stream object that selects the Stream to be used, mimics int except it can't exceed stream index 
        Returns:
            returns a numpy float
        """
        if not cls._initialized:
            cls.intializeStreams()
        return cls._streams[which_stream].integers(a,b)
    @classmethod
    def uniform(cls,a:float,b:float,which_stream:'Stream'):
        """
        Description:
            uses the numpy.generator.exponential() method to return a float from the generator stream 
        Args:
            mu: a float object that will not be negative and if a negative is input it will be turned positive with abs()
            which_stream: a Stream object that selects the Stream to be used, mimics int except it can't exceed stream index 
        Returns:
            returns a numpy float
        """
        if not cls._initialized:
            cls.intializeStreams()
        return cls._streams[which_stream].uniform(a,b)
    @classmethod
    def exponential(cls, mu: float, which_stream: 'Stream') -> numpy.float64:
        """
        Description:
            uses the numpy.generator.exponential() method to return a float from the generator stream 
        Args:
            mu: a float object that will not be negative and if a negative is input it will be turned positive with abs()
            which_stream: a Stream object that selects the Stream to be used, mimics int except it can't exceed stream index 
        Returns:
            returns a numpy float
        """
        if not cls._initialized:
            cls.intializeStreams()
        return cls._streams[which_stream].exponential(mu)
    @classmethod
    def gamma(cls, shape: float, scale: float, which_stream: 'Stream') -> numpy.float64:
        if not cls._initialized:
            cls.intializeStreams()
        shape,scale = abs(shape),abs(scale)
        return cls._streams[which_stream].gamma(shape,scale)

def main()-> None:
    stream = 0
    newRNG = RNG()
    newRNG.intializeStreams()
    init = 'gamma'
    for i in range(10000):
        if init == 'gamma': print(newRNG.gamma(1,1,0))
        elif init == 'uniform': print(newRNG.uniform(0,1,0))
        elif init == 'exponential': print(newRNG.exponential(0.6,1))
        else: print(newRNG.geometrics(0.2,0))
    #value_table = collections.Counter(g)
    #print(type(value_table))
    #hist_dataframe = pd.DataFrame().from_dict(value_table,orient = 'index') 
    #print(hist_dataframe)
    #print(len(newRNG._streams))
if __name__ == '__main__':
    main()  