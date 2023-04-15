class User():
    """_summary_
    """
    def __init__(self,name,user_num):
        """_summary_
            intializes user with name and connection

        Args:
            name (_type_): _description_
            user_num (_type_): _description_
        """
        self._name = name
        self.index= user_num
        self.rumor_list: 'list[Rumor]' = []
        self.connections:list['User'] = []
    def add_connection(self,other:'User')->None:
        """_summary_

        Args:
            other (User): _description_
        """
        if other not in self.connections:
            self.connections.append(other)
    def rumor_spread(self,other:'Rumor',debug = False)->'Rumor|None':
        """_summary_

        Args:
            other (Rumor): _description_

        Returns:
            Rumor|None: _description_
        """
        self.rumor_list.append(other)
        if debug :print(f"{self._name} believed a new rumor from {other._tellers[0]}")
    def __hash__(self):
        return self.index 
    def __eq__(self,other:'User'):
        return id(self) == id(other)
    def __repr__(self):
        connection_print = [i._name for i in self.connections]
        return f"Name:{self._name}, User#: {self.index}, Connections: {connection_print}"