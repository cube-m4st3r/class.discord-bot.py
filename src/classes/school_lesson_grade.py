from classes.database import Database

class Lesson_Grade(Database):
    def __init__(self, id):
        self._id = id
        