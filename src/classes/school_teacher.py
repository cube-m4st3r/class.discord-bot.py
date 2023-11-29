from classes.person import Person

class School_Teacher(Person):
    def __init__(self, id=None):
        super().__init__()
        self._cursor = self._database_connection.cursor()
        
        if id is not None:
            self._id = id
            person = self.fill_school_teacher(id)
            self._givenname = person.get_givenname()
            self._surname = person.get_surname()
        else: 
            pass
    
    def fill_school_teacher(self, id):
        sql = f"SELECT idperson FROM teacher WHERE idteacher={id}"
        self._cursor.execute(sql)
        teacher_id = self._cursor.fetchone()[0]
        return Person(id=teacher_id)
    
    def add_teacher_to_database(self, idperson):
        sql = f"INSERT INTO teacher VALUES(null, {idperson})"
        self._cursor.execute(sql)
        self._database_connection.commit()

        sql = "SELECT LAST_INSERT_ID()"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]

