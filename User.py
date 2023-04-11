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
        self._connections:list['User'] = []
    def __hash__(self):
        return self.index 
    def __eq__(self,other:'User'):
        return id(self) == id(other)