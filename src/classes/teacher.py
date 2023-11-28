from database import Database

class School_Teacher(Database):
    def __init__(self, id):
        self._id = id
        self._given_name = ""
        self._surname = ""