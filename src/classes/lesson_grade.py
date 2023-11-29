from classes.database import Database
from classes.school_lesson import School_Lesson

class Lesson_Grade(Database):
    def __init__(self, id):
        self._id = id
        self._lesson = School_Lesson()
        self._grade = self.fill_lesson_grade(id)

    def fill_lesson_grade(self, id):
        sql = f"SELECT FROM grade WHERE id={id}"
        self._cursor.execute(sql)
        return self._cursor.fetchone()