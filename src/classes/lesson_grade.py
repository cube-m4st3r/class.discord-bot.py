from classes.database import Database
from classes.school_lesson import School_Lesson
from classes.school_student import School_Student

class Lesson_Grade(Database):
    def __init__(self, id=None):
        super().__init__()
        self._cursor = self._database_connection.cursor()

        if id is not None:
            self._id = id
            lesson_grade_data = self.__fill_lesson_grade(id=id)
            self._lesson = School_Lesson(id=lesson_grade_data[0])
            self._student = School_Student(id=lesson_grade_data[1])
            self._grade = lesson_grade_data[2]

    def __fill_lesson_grade(self, id):
        sql = f"SELECT idlesson, idstudent, grade FROM student_has_lesson WHERE idstudent_has_lesson={id}"
        self._cursor.execute(sql)
        return self._cursor.fetchone()
    
    def _add_grade_to_database(self, lesson, student, grade):
        sql = f"INSERT INTO student_has_lesson VALUES(null, {lesson._get_id()}, {student._get_id()}, {grade})"
        self._cursor.execute(sql)
        self._database_connection.commit()

        sql = "SELECT LAST_INSERT_ID()"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]
    
    def _retrieve_idlesson_grades_for_student(self, student):
        sql = f"SELECT idstudent_has_lesson FROM student_has_lesson WHERE idstudent={student._get_id()}"
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    
    def _get_grade(self):
        return self._grade
    
    def _set_grade(self, grade):
        self._grade = grade
    
    def _set_school_lesson(self, lesson):
        self._lesson = lesson

    def _get_school_lesson(self):
        return self._lesson
    
    def _get_school_student(self):
        return self._student

    def _set_school_student(self, student):
        self._student = student