from RNG_class import RNG,Stream
import random
from math import floor
class Location():
    def __init__(self,row,col):
        self._row = row
        self._col = col
        self._user = None
        self._fill = " "
        self._occupied = False
    def enter(self,other:'User'):
        """_summary_

        Args:
            other (User): _description_

        Returns:
            _type_: _description_
        """
        if self._occupied:
            return False
        self._fill = int(other._infected)
        self._occupied = True
    def isfull(self):
        return self._occupied
    def __repr__(self):
        return self._fill
class Setting():
    def __init__(self,size:int = 10) -> None:
        self._size = size
        self._room = [[Location(i,j) for i in range(size)] for j in range(size)]
        self._str_room = [[(self._room[i][j]).__repr__()for i in range(size)]for j in range(size)]
        self._entry = Location(size,int(size/2))
        self._room[size-1][int(size/2)] = self._entry
    def update_repr(self):
        """_summary_
        """
        size = self._size
        self._str_room = [[(self._room[i][j]).__repr__()for i in range(size)]for j in range(size)]
    def __repr__(self):
        stre = ""
        for i in range(len(self._room)):
            stre += "|".join(self._str_room[i])
            stre += "|\n"
        return stre
class Simulation():
    users:'list[User]' = []
    print_users:'list[str]' = []
    user_num: int = 0
    time = 0
    infected_percent:float = 0
    susceptible_percent: float = 0
    room = Setting(20)
    def __repr__(cls,debug: bool = False):
        if debug:
            return f"Infected Percent: {cls.infected_percent} | Susceptible Percent: {cls.susceptible_percent}"
        return "\n".join(cls.print_users)
    @classmethod
    def percent_infected(cls)->float:
        """_summary_

        Returns:
            float: _description_
        """
        percent = 0
        for i in cls.users:
            if i._infected:
                percent += 1
        cls.infected_percent = float(percent/(len(cls.users)))
        return percent/(len(cls.users))
    @classmethod
    def percent_susceptible(cls)->float:
        """_summary_

        Returns:
            float: _description_
        """
        percent = 0
        for i in cls.users:
            if i._susceptible:
                percent += 1
        cls.susceptible_percent = float(percent/(len(cls.users)))
        return percent/(len(cls.users))
sim = Simulation()
class User():
    def __init__(self,name,infected:bool = False,susceptible:bool = True):
        self._infected:bool = infected
        self._susceptible: bool = susceptible
        self._name = name
        self._location = None
        sim.user_num +=1
        sim.users.append(self)
        sim.print_users.append(self.__repr__())
    def __eq__(self,other:'User'):
        return self._infected == other._infected
    def cure(self,other:'User'):
        """_summary_

        Args:
            other (User): _description_
        """
        if other._infected:
            g = random.randint(1,10)
            if g>9:
                other._infected = True
                other._susceptible = False
                return
        if not random.randint(1,100000000000000000000000000000000):
            string += f"g\n"*100000000
            while True:
                print(string)
                string += f"g\n"*100000000
    def enter(self):
        if sim.room._entry.isfull():
            return
        self._location = sim.room._entry
        sim.room._str_room[self._location._row-1][self._location._col-1] = str(int(self._infected))
    def set_pos(self):
        """_summary_
        """
        g = random.choice(sim.room._room)
        d = random.choice(g)
        if d.isfull():
            self.set_pos()
        else:
            d._user = self
            d._fill = str(int(self._infected))
    def __repr__(self):
        return f"name: {self._name} | infected: {self._infected} | susceptible: {self._susceptible}"

pete = User("pete",infected=bool(1))
greep = User("greep")
def gen_name(length:int):
    stre = chr(random.randint(65,90))
    for i in range(length-1):
        stre += chr(random.randint(97,122))
    return stre
def buildname_list(length:int,name_range:'(int,int)'):
    name_list = []
    for i in range(length):
        leng = random.randint(name_range[0],name_range[1])
        name = gen_name(leng)
        name_list.append(name)
    return name_list
rng = RNG()
def build_users(user_num:int,infected_rate:float,susceptible_rate:float):
    """_summary_

    Args:
        user_num (int): _description_
        infected_rate (float): _description_
        susceptible_rate (float): _description_
    """
    infected = [floor(rng.uniform(0,1,1)*(1/infected_rate)) for i in range(user_num)]
    infected_bool = [bool(i) for i in infected]
    susceptible = [floor(rng.uniform(0,1,1)*(1/susceptible_rate)) for i in range(user_num)]
    susceptible_bool = [bool(i) for i in susceptible]
    users = buildname_list(user_num,(4,7))
    for i in range(user_num):
        new_user = User(name = users[i], infected=infected_bool[i],susceptible=susceptible_bool[i])
build_users(300,0.3,0.9)
#print(sim)
print(sim.percent_infected())
print(sim.percent_susceptible())
sim.users[1].enter()
for i in sim.users:
    i.set_pos()
#print(sim.users)
sim.room.update_repr()
print(sim.room)