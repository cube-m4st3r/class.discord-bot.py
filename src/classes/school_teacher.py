from classes.person import Person

class School_Teacher(Person):
    def __init__(self, id=None):
        super().__init__()
        self._cursor = self._database_connection.cursor()
        
        if id is not None:
            self._id = id
            person = self.__fill_school_teacher(id)
            self._givenname = person._get_givenname()
            self._surname = person._get_surname()
        else: 
            pass
    
    def __fill_school_teacher(self, id):
        sql = f"SELECT idperson FROM teacher WHERE idteacher={id}"
        self._cursor.execute(sql)
        teacher_id = self._cursor.fetchone()[0]
        return Person(id=teacher_id)
    
    def _add_teacher_to_database(self, idperson):
        sql = f"INSERT INTO teacher VALUES (null, {idperson})"
        self._cursor.execute(sql)
        self._database_connection.commit()

        sql = "SELECT LAST_INSERT_ID()"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]

    def _retrieve_teacher_lessons_from_database(self):
        sql = f"SELECT l.idlesson FROM lesson l JOIN teacher t ON l.idteacher = t.idteacher AND t.idteacher={self._get_id()}"
        
        with self._database_connection.cursor() as cursor:
            cursor.execute(sql)
            idlessons = [idlesson[0] for idlesson in cursor.fetchall()]
        return idlessons

    def _delete_teacher_from_database(self):
        sql = f"DELETE FROM teacher WHERE idteacher={self._get_id()}"

        with self._cursor:
            self._cursor.execute(sql)
            self._database_connection.commit()
        
    def _retrieve_idteacher_list(self):
        sql = "SELECT idteacher FROM teacher"
        
        with self._cursor:
            self._cursor.execute(sql)
            idteacher_list = [idteacher[0] for idteacher in self._cursor.fetchall()]

        return idteacher_list

    def _get_id(self):
        return self._id
