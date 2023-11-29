from classes.database import Database
from classes.school_teacher import School_Teacher

class School_Lesson(Database):
    def __init__(self, id):
        self._id = id
        self._name = self.fill_school_lesson(id=id)[0]
        self._teacher = School_Teacher(id=self.fill_school_lesson(id=id)[1])

    def fill_school_lesson(self, id):
        sql = f"SELECT name, idteacher FROM lesson WHERE id={id}"
        self._cursor.execute(sql)
        return self._cursor.fetchall()