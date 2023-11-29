from classes.database import Database
from classes.school_teacher import School_Teacher

class School_Lesson(Database):
    def __init__(self, id=None):
        super().__init__() 
        self._cursor = self._database_connection.cursor()

        if id is not None:
            lesson_data = self.fill_school_lesson(id)
            self._id = id
            self._name = lesson_data[0]
            self._teacher = School_Teacher(id=lesson_data[1])
        else:
            pass

    def fill_school_lesson(self, id):
        sql = f"SELECT name, idteacher FROM lesson WHERE idlesson={id}"
        self._cursor.execute(sql)
        return self._cursor.fetchone()
    
    def add_lesson_to_database(self, name, idteacher=None): # idteacher=None for post-MVP so lessons can be created w/o a teacher.
        # needs database update.
        sql = f"INSERT INTO lesson VALUES(null, '{name}', {idteacher})"
        self._cursor.execute(sql)
        self._database_connection.commit()

        sql = "SELECT LAST_INSERT_ID()"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]
    
    def retrieve_idlesson_list(self):
        sql = f"SELECT idlesson FROM lesson"
        self._cursor.execute(sql)

        idlesson_list = list()
        for idlesson in self._cursor.fetchall():
            idlesson_list.append(idlesson[0])
        
        return idlesson_list
    
    def _get_name(self):
        return self._name

    def _set_name(self, name):
        self._name = name

    def _get_id(self):
        return self._id
