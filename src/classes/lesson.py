from database import Database

class School_Lesson(Database):
    def __init__(self, id):
        self._id = id
        self._name = ""
        self._teacher = ""
