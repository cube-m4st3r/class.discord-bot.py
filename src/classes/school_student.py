from classes.person import Person
from classes.user import User


class School_Student(Person):
    def __init__(self, id=None):
        super().__init__()
        self._cursor = self._database_connection.cursor()

        if id is not None:
            self._id = id
            person, user = self.fill_school_student(id=id) 
            self._givenname = person.get_givenname()
            self._surname = person.get_surname()
            self._user = user
        else:
            pass

    def fill_school_student(self, id):
        sql = f"SELECT idperson, iddiscorduser FROM student WHERE idstudent={id}"
        self._cursor.execute(sql)
        result = self._cursor.fetchone()
        return Person(id=result[0]), User(id=result[1])
    
    def _add_school_student_to_database(self, idperson, iduser):
        sql = f"INSERT INTO student VALUES(null, {idperson}, {iduser})"
        self._cursor.execute(sql)
        self._database_connection.commit()

        sql = "SELECT LAST_INSERT_ID()"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]
    
    def set_id(self, id):
        self._id = id
