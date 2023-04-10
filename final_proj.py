from RNG_class import RNG,Stream
import random
from math import floor
from time import perf_counter,sleep
import logging
logging.basicConfig(filename = "logging_final_proj.txt",level = 10, filemode = 'w')
logging.debug(1)
rng = RNG()
sim = Simulation()

################################################################################################

class Location():
    """_summary_
        location class: this can store one user in a specific position in the setting

    """ 
    def __init__(self,row,col):
        """_summary_

        Args:
            row (_type_): _description_
            col (_type_): _description_
        """
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
    def closeness(self,other:'Location')->int:
        """_summary_
            hueristic that returns an integer value between two locations
        Args:  
            other (Location): other location input

        Returns:
            int : integer value of the manhattan distance between two locations
        """
        return self._row-other._row + self._col - other._col
    def __eq__(self,other:'Location')->bool:
        if self._row != other._row:
            return False
        if self._col != other._col:
            return False
        if self._user != other._user:
            return False
        return True
    def __repr__(self):
        return self._fill
    
################################################################################################


class Setting():
    def __init__(self,size:int = 10) -> None:
        """_summary_

        Args:
            size (int, optional): _description_. Defaults to 10.
        """
        self._size = size
        self._room = [[Location(i,j) for i in range(size)] for j in range(size)]
        self._str_room = [[(self._room[i][j]).__repr__()for i in range(size)]for j in range(size)]
        self._entry = Location(size,int(size/2))
        self._room[size-1][int(size/2)] = self._entry
    def update_repr(self)->None:
        """_summary_ :updates the repr for for the setting
        """
        size = self._size
        self._str_room = [[(self._room[i][j]).__repr__()for i in range(size)]for j in range(size)]
    def __repr__(self)-> str:
        stre = ""
        for i in range(len(self._room)):
            stre += "|".join(self._str_room[i])
            stre += "|\n"
        return stre
    def __eq__(self,other:'Setting')-> bool:
        """_summary_: equation check for two rooms, just a helper function we can use to debug

        Args:
            other (Setting): other setting type

        Returns:
            bool: _description_
        """
        bool_turn = True
        for i in range(len(self._room)):
            bool_turn = self._room[i] == other._room[i]
            if not bool_turn:
                return bool_turn
        return bool_turn


################################################################################################


class Simulation():
    users:'list[User]' = []
    print_users:'list[str]' = []
    user_num: int = 0
    time = 0
    infected_percent:float = 0
    susceptible_percent: float = 0
    room = Setting(20)
    change_list = []
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
    def shuffle(cls,sim:'Simulation')->'Simulation':
        """_summary_: main function used in the simulation, shuffles the users in the setting using the set_pos method
        then has users interact based on hueristic closeness and then User interaction functions are called.
        this updates the simulation and returns itself

        Args:
            sim (Simulation): _description_ the simulation you want to input, generally inputting the return from the last shuffle

        Returns:
            _type_: self
        """
        user_ord = cls.users.copy()
        random.shuffle(user_ord)
        new_list = []
        while len(user_ord) != 0:
            person_one = user_ord.pop()
            #print(person_one)
            if len(user_ord) == 0:
                new_list.append(person_one)
                break
            other_person = person_one.find_nearest(user_ord)
            length_val = person_one.location_closeness(other_person)
            if length_val > 4:
                logging.debug(f"{person_one}: before questioning")
                person_one.question()
                logging.debug(f"{person_one}: after questioning")
                continue
            
            try:
                if other_person == None:
                    break
            except: None
            #user_num = len(cls.users)
            #logging.debug(f"Same person:{other_person is person_one} user nums: {user_num}")
            #print(person_one)
            #print(other_person)
            #grub = "#".join(("#"*1000))
            #change_person_one = 
            person_one.interact(other_person)
            #change_person_other = 
            other_person.interact(person_one)
            '''
            if change_person_one is not None:
                cls.change_list.append(change_person_one)
            if change_person_other is not None:
                cls.change_list.append(change_person_other)
            '''
            new_list.append(person_one)
            new_list.append(other_person)
        #for some reason the new_list keeps doubling in size whenever this runs
        gru_list = []
        return_list = []
        #gorn = f"run time: {cls.time}" + "\n".join(cls.change_list)
        for i in new_list:
            if id(i) not in gru_list:
                gru_list.append(id(i))
                return_list.append(i)
        #logging.debug(f"new_list len: {len(new_list)} \n gru_list len: {len(gru_list)}")
        cls.users = return_list
        #logging.debug(f"{gorn}")
        for i in cls.users:
            sim = i.set_pos(sim,debug = True)
        cls.room.update_repr()
        return cls
    
################################################################################################

################################################################################################

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
        return id(self) == id(other)
    def location_closeness(self,other:'User')->int:
        #print(other)
        return self._location.closeness(other._location)
    def find_nearest(self,user_ord:list)->'User':
        new_list = [self.location_closeness(i) for i in user_ord]
        new_dict = {k:v for (k,v) in zip(new_list,user_ord)}
        while None in new_list:
            new_list.remove(None)
        if len(new_list) == 0:
            return None
        val = new_dict[min(new_list)]
        return val

#######################################################################################


    def interact(self,other:'User')->'str | None':
        """_summary_
            interaction function: edits the user that is calling the function and the other it is interacting with
            this function only really works within the context of the the shuffle method in the simulation class 
            this also is restrained by 
        Args:
            other (User):
            different user: 
        """
        g = None
        if not other._susceptible:
            if not self._infected:
                self.argue(other)
            return
        if not(self._infected + other._infected):
            g = self.cure(other)
        elif self._infected:
            if not other._infected:
                g = self.argue(other)
            else:
                g = self.convince(other)
        return g
    def convince(self,other:'User'):
        t = rng.random(1)
        g = rng.gamma(t,t+.3,1)
        if g < 0.5:
            #other._susceptible = True
            other._infected = self._infected
            return None

    def question(self):
        if self._susceptible:
            g = round(rng.gamma(1,1.5,1))
            self._infected = bool(g)   
        elif bool(round(rng.random(1))):
            self._susceptible = not(self._susceptible)

    def argue(self,other:'User'):
        """_summary_

        Args:
            other (User): _description_
        """
        t = rng.random(1)
        g = rng.exponential(t,1)
        if g>1:
            gorn = other._infected
            glorn = ""
            if gorn == True:
                gorn = "infected"
                glorn = "not infected"
            else:
                gorn = "not infected"
                glorn = "infected"
            other._infected = self._infected
            #other._susceptible = False
            return (f"Change in User: {other._name} from {gorn} to {glorn}")
        
#######################################################################################


    def cure(self,other:'User'):
        """_summary_
            this is the interaction between two users
        Args:
            other (User): _description_
        """
        t = rng.random(1)
        g = rng.uniform(0,t,1)
        if g>0.5:
            other._susceptible = False
            return f"Change in User: {other._name} from susceptible to not susceptible, cured"
        
#######################################################################################


    def enter(self):
        """_summary_
            this intializes the entry
        """
        if sim.room._entry.isfull():
            return
        self._location = sim.room._entry
        sim.room._str_room[self._location._row-1][self._location._col-1] = str(int(self._infected))

#######################################################################################


    def set_pos(self, sim: 'Simulation',debug = False)-> 'Simulation':
        """_summary_

        Args:
            sim (Simulation): _description_
            debug (bool, optional): _description_. Defaults to False.

        Returns:
            Simulation: _description_
        """
        g = random.choice(sim.room._room)
        d = random.choice(g)
        if d.isfull():
            self.set_pos(sim)
        else:
            d._user = self

            if debug: t = self._location
            self._location = d
            if debug: t._fill = " "
            d._fill = str(int(self._infected))
            return sim
        
#######################################################################################


    def __repr__(self):
        g = f"name: {self._name} | infected: {self._infected} | susceptible: {self._susceptible}"
        if self._location is not None:
            g+= f" location: ({self._location._row},{self._location._col})"
        return g
    

#######################################################################################


def gen_name(length:int):
    stre = chr(random.randint(65,90))
    for i in range(length-1):
        stre += chr(random.randint(97,122))
    return stre

#######################################################################################

def buildname_list(length:int,name_range:'(int,int)'):
    name_list = []
    for i in range(length):
        leng = random.randint(name_range[0],name_range[1])
        name = gen_name(leng)
        name_list.append(name)
    return name_list
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

#######################################################################################

if __name__ == "__main__":
    sim = Simulation()
    sim.room = Setting(40)
    build_users(600,0.5,0.1)
    start = perf_counter()
    for i in sim.users:
        i.set_pos(sim)
    sim.room.update_repr()
    while sim.time < 20:
        sim.time +=1
        print(f"infected%: {sim.percent_infected()} | susceptible% :{sim.percent_susceptible()}")
        print("")
        g = sim
        user_set = []
        for i in sim.users:
            if id(i) not in user_set:
                user_set.append(id(i))
        logging.debug(f"\n unique user_num: {len(user_set)} \n total user num: {len(sim.users)} ")
        start = perf_counter()
        sim = sim.shuffle(sim)
        print(f"Shuffle time in seconds {perf_counter() - start}")
        logging.debug(f"logging check same simulation: {g is sim}")
        print(sim.room)
        sleep(1)